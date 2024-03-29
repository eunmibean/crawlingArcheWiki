import mysql.connector
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

user = config['DB']['USER'] 
pwd = config['DB']['PASSWORD'] 
host = config['DB']['HOST']
port = config['DB']['PORT']
database = config['DB']['DATABASE']  


config = {
  'user': user,
  'password': pwd,
  'host': host,
  'port' : port,
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
    

    def insert_item_name(self, itemName):   
        self.c.execute("INSERT INTO item_name_list (name) VALUES(%s)", (itemName, ))
        self.mydb.commit()

    
    def insert_recipe(self, code, key, count):
        self.c.execute("INSERT INTO recipe_list VALUES(%s, %s, %s)", (code,key,count, ))
        self.mydb.commit()
            
    def get_item_code(self, itemName):
        sql = "SELECT code FROM item_name_list where name=%s"
        self.c.execute(sql, (itemName, ))
        return self.c.fetchone()

    def get_recipe(self, code):
        self.c.execute("SELECT ingredient, count FROM recipe_list where code=%s", (code,))
        result = self.c.fetchall()
        return result

    def create_table(self):
        # 테이블 생성 
        self.c.execute("CREATE TABLE IF NOT EXISTS item_name_list \
            (name String , code INTEGER PRIMARY KEY autoincrement)")
        self.c.execute("CREATE TABLE IF NOT EXISTS recipe_list \
            (code integer, ingredient String, count integer)")
    
    def close_db(self):
        self.c.close()
