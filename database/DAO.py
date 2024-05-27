from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllRetailers():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                        from go_retailers"""
        cursor.execute(query)
        for row in cursor:
            result.append(
                Retailer(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnessioni(country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select gr.Retailer_code as cod1, gr2.Retailer_code as cod2
from go_retailers gr, go_retailers gr2 
where gr.Country= %s and gr2.Country = %s and gr2.Retailer_code <> gr.Retailer_code;"""
        cursor.execute(query, (country, country) )
        for row in cursor:
            result.append((row["cod1"], row["cod2"]))
        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getPesi(v1, v2, year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT count(distinct gds.Product_number) as peso
                    FROM go_sales.go_daily_sales gds, go_sales.go_daily_sales gds2
                    where gds2.Product_number  = gds.Product_number and gds.Retailer_code =%s and gds2.Retailer_code = %s and year (gds2.`Date`) = %s
                    and year (gds.`Date`) = %s
"""
        cursor.execute(query, (v1.Retailer_code, v2.Retailer_code, year, year, ))
        for row in cursor:
            result.append(row["peso"])
        cursor.close()
        conn.close()
        return result[0]
