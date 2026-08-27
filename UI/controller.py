import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    # ---------- riempimento iniziale ----------

    def fillDDcategories(self):
        for c in self._model.getCategories():
            self._view._ddcategory.options.append(
                ft.dropdown.Option(key=c[0], text=c[1])
            )
        self._view.update_page()

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)

    # ---------- PUNTO 1 ----------

    def handleCreaGrafo(self, e):
        # validazione input
        categoria = self._view._ddcategory.value
        if categoria is None:
            self._view.create_alert("Selezionare una categoria")
            return
        start = self._view._dp1.value
        end = self._view._dp2.value
        if start is None or end is None:
            self._view.create_alert("Selezionare entrambe le date")
            return
        if start > end:
            self._view.create_alert("La data di inizio deve precedere la fine")
            return

        # delega al model
        self._model.buildGraph(int(categoria), start, end)

        # riempi i dropdown dei prodotti con i nodi del grafo (per il Punto 2)
        self._view._ddProdStart.options.clear()
        self._view._ddProdEnd.options.clear()
        for nodo in self._model.getNodi():
            self._view._ddProdStart.options.append(
                ft.dropdown.Option(key=nodo.product_id, text=str(nodo)))
            self._view._ddProdEnd.options.append(
                ft.dropdown.Option(key=nodo.product_id, text=str(nodo)))
        self._view._ddProdStart.value = None
        self._view._ddProdEnd.value = None

        # stampa risultati
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Date selezionate:"))
        self._view.txt_result.controls.append(ft.Text(f"Start date: {start.strftime('%Y-%m-%d')}"))
        self._view.txt_result.controls.append(ft.Text(f"End date: {end.strftime('%Y-%m-%d')}"))
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))
        self._view.update_page()

    def handleBestProdotti(self, e):
        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo")
            return

        best = self._model.getBestProdotti()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("I cinque prodotti più venduti sono:"))
        for nodo, score in best:
            self._view.txt_result.controls.append(ft.Text(f"{nodo} with score {score}"))
        self._view.update_page()

    # ---------- PUNTO 2 ----------

    def handleCercaCammino(self, e):
        # il grafo deve esistere
        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo")
            return

        # validazione lunghezza
        lunStr = self._view._txtInLun.value
        if lunStr is None or lunStr == "":
            self._view.create_alert("Inserire la lunghezza del cammino")
            return
        try:
            lun = int(lunStr)
        except ValueError:
            self._view.create_alert("La lunghezza deve essere un numero intero")
            return
        if lun <= 0:
            self._view.create_alert("La lunghezza deve essere positiva")
            return

        # validazione prodotti
        idStart = self._view._ddProdStart.value
        idEnd = self._view._ddProdEnd.value
        if idStart is None or idEnd is None:
            self._view.create_alert("Selezionare prodotto di partenza e di arrivo")
            return

        partenza = self._model.getProductById(int(idStart))
        arrivo = self._model.getProductById(int(idEnd))

        # ricerca del cammino ottimo
        path, score = self._model.getCamminoOttimo(partenza, arrivo, lun)

        # stampa risultati
        self._view.txt_result.controls.clear()
        if len(path) == 0:
            self._view.txt_result.controls.append(
                ft.Text("Nessun cammino trovato con i parametri selezionati"))
        else:
            self._view.txt_result.controls.append(
                ft.Text(f"Cammino trovato con peso totale {score}:"))
            for nodo in path:
                self._view.txt_result.controls.append(ft.Text(str(nodo)))
        self._view.update_page()