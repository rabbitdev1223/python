import mysql.connector
class Conn:
    def __init__(self):
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'port': '3306',
            'database': 'Tarragon'
        }
        self.conn = mysql.connector.connect(**config)
        self.cursor = self.conn.cursor()
