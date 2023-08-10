import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

user = config['DB']['USER'] 
pwd = config['DB']['PASSWORD'] 
host = config['DB']['HOST']
database = config['DB']['DATABASE']  

config = {
  'user': user,
  'password': pwd,
  'host': host,
  'database': database,
  'charset': 'utf8mb4', 
  'collation': 'utf8mb4_general_ci',
  'raise_on_warnings': True

}


class dbConnect: 
    def __init__(self):
        try:
            self.mydb = mysql.connector.connect(**config)
            print("Connected to MySQL server!")
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL server: {err}")
            exit(1)
       
        self.c = self.mydb.cursor()
    

    def insertItemName(self, itemName):    
        self.c.execute("INSERT INTO item_name_list (name) VALUES(?)", (itemName, ))
    
    def insertRecipe(self, code, key, count):
        self.c.execute("INSERT INTO recipe_list VALUES(?, ?, ?)", (code,key,count, ))
            
    def getItemCode(self, itemName):
        sql = "SELECT code FROM item_name_list where name=%s"
        self.c.execute(sql, (itemName, ))
        return self.c.fetchone()

    def getRecipe(self, code):
        self.c.execute("SELECT ingredient, count FROM recipe_list where code=?", (code,))
        result = self.c.fetchall()
        return result

    def createTable(self):
        # 테이블 생성 
        self.c.execute("CREATE TABLE IF NOT EXISTS item_name_list \
            (name String , code INTEGER PRIMARY KEY autoincrement)")
        self.c.execute("CREATE TABLE IF NOT EXISTS recipe_list \
            (code integer, ingredient String, count integer)")
    
    def closeDB(self):
        self.c.close()
