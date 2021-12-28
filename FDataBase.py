import math, time, sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('error while reading from db')
        return []

    def addUser(self, username, password, email, role):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, ?, ?)", (username, password, email, role, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("error while adding into database" + str(e))
            return False

        return True

