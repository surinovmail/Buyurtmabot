import sqlite3

class Database:
    def __init__(self,db_file):
        self.connection=sqlite3.connect(db_file)
        self.cursor=self.connection.cursor()
    
    def add_buyurtma(self,id,ism,viloyat,tuman,mahalla,raqam,joylashuv):
        with self.connection:
             return self.cursor.execute("INSERT INTO `Buyurtma` (`id`,`ism`,`viloyat`,`tuman`,`mahalla`,`raqam`,`joylashuv`) VALUES (?,?,?,?,?,?,?) ", (id,ism,viloyat,tuman,mahalla,raqam,joylashuv))

   