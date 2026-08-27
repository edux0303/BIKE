from database.DB_connect import DBConnect
from model.products import Product

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last


    @staticmethod
    def getCategories():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (c.category_name) as nome, c.category_id as id from categories c order by c.category_name"

        cursor.execute(query)

        for row in cursor:
            results.append((row["id"],row["nome"]))



        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodes(categoria):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT p.product_id , p.product_name , p.model_year "
                 "from products p"
                 " WHERE p.category_id = %s")

        cursor.execute(query,(categoria,))

        for row in cursor:
            results.append(Product(**row))


        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getVendite(categoria,start,end):

        conn = DBConnect.get_connection()

        results = {}

        cursor = conn.cursor(dictionary=True)
        query = ("SELECT oi.product_id AS id, COUNT(DISTINCT oi.order_id) AS num "
         "FROM order_items oi, orders o, products p "
         "WHERE o.order_id = oi.order_id "
         "AND p.product_id = oi.product_id "
         "AND p.category_id = %s "
         "AND o.order_date BETWEEN %s AND %s "
         "GROUP BY oi.product_id")

        cursor.execute(query,(categoria,start,end))
        for row in cursor:
            results[row["id"]]=row["num"]
        cursor.close()
        conn.close()
        return results