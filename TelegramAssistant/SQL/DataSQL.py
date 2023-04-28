import sqlite3


from datetime import datetime



class AdminBase:
    def __init__(self,sql,cursor):
        self.sql = sql
        self.cursot = cursor

    def AddDataBase(self,login,password,root):
        try:
            self.cursor.execute(f"INSERT INTO Accounts VALUES (?,?,?)",(login,password,root))
            self.sql.commit()
            return True
        except:
            return False

    def DataBaseList(self):
        account_list = []
        self.cursor.execute("SELECT * FROM Accounts")
        for text in self.cursor.fetchall():
            account_list.append(list(text))
        return account_list

    def RemoveAccount(self,Login,Password):
        Login = ("".join(str(Login))).strip()
        Password = ("".join(str(Password))).strip()
        query = "DELETE FROM Accounts WHERE Login = '{}' AND Password = '{}'".format(Login, Password)
        self.cursor.execute(query)
        self.sql.commit()

class UsersBase:
    def __init__(self,sql,cursor):
        self.sql = sql
        self.cursot = cursor
    
    def LeaveAccount(self,ID):
        ID = ("".join(str(ID))).strip()
        self.cursor.execute("DELETE FROM Users WHERE ID = '{}'".format(ID))
        self.sql.commit()

class DataBase(AdminBase,UsersBase):
    def __init__(self):
        self.sql = sqlite3.connect('Database.db')
        self.cursor = self.sql.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
            Login TEXT,
            Password TEXT,
            Root TEXT,
            ID TEXT,
            Time TEXT
        )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Accounts(
            Login TEXT,
            Password TEXT,
            Root TEXT
        )""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS UsersLog(
            Login TEXT,
            Password TEXT,
            Root TEXT,
            ID TEXT,
            Time TEXT
        )""")

        self.sql.commit()

    def CheckUser(self,ID):
        ID = ''.join(str(ID))
        self.cursor.execute(f"SELECT Login FROM Users WHERE ID = '{ID}'")
        if self.cursor.fetchone() is None:
            return True
        else:
            return False
        
    def LoginUser(self,Login):
        Login = ''.join(str(Login))
        self.cursor.execute(f"SELECT Login FROM Accounts WHERE Login = '{Login}'")
        if self.cursor.fetchone() is None:
            return True
        else:
            return False
        
    def LoginPassword(self,Login,Password):
        Login = ''.join(str(Login))
        Password = ''.join(str(Password))
        self.cursor.execute(f"SELECT Password FROM Accounts WHERE Login = '{Login}'")
        if Password == ''.join(self.cursor.fetchone()):
            return True
        else:
            return False
        
    def LoginAccount(self,Login,Password,ID,Time):
        datetime_object = datetime.fromtimestamp(Time)
        Login = ''.join(str(Login))
        Password = ''.join(str(Password))
        ID = ''.join(str(ID))
        Time = ''.join(str(datetime_object.strftime("%Y-%m-%d %H:%M:%S")))
        self.cursor.execute(f"SELECT Root FROM Accounts WHERE Login = '{Login}'")
        Root = ''.join(self.cursor.fetchone())
        self.cursor.execute(f"INSERT INTO Users VALUES (?,?,?,?,?)",(Login,Password,Root,ID,Time))
        self.sql.commit()
        self.cursor.execute(f"INSERT INTO UsersLog VALUES (?,?,?,?,?)",(Login,Password,Root,ID,Time))
        self.sql.commit()
        return Root

    def RegisterUser(self,ID):
        ID = ''.join(str(ID))
        self.cursor.execute(f"SELECT Login,Root FROM Users WHERE ID = '{ID}'")
        base = self.cursor.fetchone()
        return "".join(base[0]),"".join(base[-1])



