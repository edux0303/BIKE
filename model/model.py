import itertools
from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap = {}
        self._bestPath = []
        self._bestScore = 0

    def buildGraph(self, categoria, start, end):
        self._grafo.clear()
        self._idMap = {}

        prodotti = DAO.getNodes(categoria)
        for p in prodotti:
            self._idMap[p.product_id] = p
        self._grafo.add_nodes_from(prodotti)

        vendite = DAO.getVendite(categoria, start, end)
        venduti = list(vendite.keys())
        for id1, id2 in itertools.combinations(venduti, 2):
            n1 = vendite[id1]
            n2 = vendite[id2]
            peso = n1 + n2
            if n1 > n2:
                self._grafo.add_edge(self._idMap[id1], self._idMap[id2], weight=peso)
            elif n2 > n1:
                self._grafo.add_edge(self._idMap[id2], self._idMap[id1], weight=peso)
            else:
                self._grafo.add_edge(self._idMap[id1], self._idMap[id2], weight=peso)
                self._grafo.add_edge(self._idMap[id2], self._idMap[id1], weight=peso)

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        return DAO.getCategories()

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getNodi(self):
        return list(self._grafo.nodes())

    def getProductById(self, idProdotto):
        return self._idMap[idProdotto]

    def getBestProdotti(self):
        best = []
        for nodo in self._grafo.nodes():
            pesoOut = 0
            for u, v, data in self._grafo.out_edges(nodo, data=True):
                pesoOut += data["weight"]
            pesoIn = 0
            for u, v, data in self._grafo.in_edges(nodo, data=True):
                pesoIn += data["weight"]
            best.append((nodo, pesoOut - pesoIn))
        best.sort(key=lambda x: x[1], reverse=True)
        return best[:5]

    # ---------- PUNTO 2: cammino ottimo ricorsivo ----------

    def getCamminoOttimo(self, partenza, arrivo, lun):
        self._bestPath = []
        self._bestScore = 0
        self._ricorsione([partenza], arrivo, lun)
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, arrivo, lun):
        ultimo = parziale[-1]

        # caso terminale: cammino di lun archi (= lun+1 nodi)
        if len(parziale) == lun + 1:
            if ultimo == arrivo:
                score = self._calcolaPeso(parziale)
                if score > self._bestScore:
                    self._bestScore = score
                    self._bestPath = list(parziale)
            return

        # caso ricorsivo: provo tutti i successori non ancora visitati
        for succ in self._grafo.successors(ultimo):
            if succ not in parziale:
                parziale.append(succ)
                self._ricorsione(parziale, arrivo, lun)
                parziale.pop()

    def _calcolaPeso(self, cammino):
        peso = 0
        for i in range(len(cammino) - 1):
            peso += self._grafo[cammino[i]][cammino[i + 1]]["weight"]
        return peso