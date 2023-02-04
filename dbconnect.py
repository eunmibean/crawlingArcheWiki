import sqlite3

class dbConnect: 
    def __init__(self):

        # DB 생성 (오토 커밋)
        conn = sqlite3.connect("test.db", isolation_level=None)

        # 커서 획득
        self.c = conn.cursor()

    def insertItemName(self, itemName):    
        self.c.execute("INSERT INTO item_name_list (name) VALUES(?)", (itemName, ))
    
    # def insertRecipe(self, dict, code):
    #     for key in dict.keys():
    #         count = dict.get(key)
    #         self.c.execute(f"INSERT INTO recipe_list VALUES({code},{key},{count} )")

    def insertRecipe(self, code, key, count):
        self.c.execute("INSERT INTO recipe_list VALUES(?, ?, ?)", (code,key,count, ))
            
    def getItemCode(self, itemName):
        self.c.execute("SELECT code FROM item_name_list where name=?", (itemName,))
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
    

    