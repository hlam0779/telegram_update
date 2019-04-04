import sqlite3

class DBManager():

    def __init__(self, SQL_SERVER):

        # DATABASE (db.sqlite3)
        self.SQL_SERVER = SQL_SERVER
        # 'users' table
        self.SQL_USERS = 'users'
        self.USER_ID = 'user_id'
        

        # Try creating tables if not existed
        try:
            conn = sqlite3.connect(self.SQL_SERVER)
            c = conn.cursor()
            c.execute(f'CREATE TABLE IF NOT EXISTS {self.SQL_USERS} ({self.USER_ID} INTEGER PRIMARY KEY )')
            conn.commit()
            conn.close()
        except FileNotFoundError:
            f = open(self.SQL_SERVER,'w+')
            f.close()
            conn = sqlite3.connect(self.SQL_SERVER)
            c = conn.cursor()
            c.execute(f'CREATE TABLE IF NOT EXISTS {self.SQL_USERS} ({self.USER_ID} INTEGER PRIMARY KEY )')
            conn.commit()
            conn.close()
        except Exception as e:
            print("Error in opening: "+str(e))

    

    def add(self, user_id):

        # First try of connecting sqlite database
        try:
            conn = sqlite3.connect(self.SQL_SERVER)
            c = conn.cursor()
            c.execute(f'CREATE TABLE IF NOT EXISTS {self.SQL_USERS} ({self.USER_ID} INTEGER PRIMARY KEY )')
            
        except FileNotFoundError:
            f = open(self.SQL_SERVER,'w+')
            f.close()
            conn = sqlite3.connect(self.SQL_SERVER)
            c = conn.cursor()
            c.execute(f'CREATE TABLE IF NOT EXISTS {self.SQL_USERS} ({self.USER_ID} INTEGER PRIMARY KEY )')
            
        except Exception as e:
            print("Error in opening: "+str(e))
            return False
        # Add the search input of a specific user to the database
        try:
            c.execute(f'INSERT INTO {self.SQL_USERS} VALUES ({user_id})')
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Error in adding, ignoring: "+str(e))
            return False
        return False

    def is_existed(self, user_id):
        # First try of connecting sqlite database
        try:
            conn = sqlite3.connect(self.SQL_SERVER)
            c = conn.cursor()
            c.execute(f'CREATE TABLE IF NOT EXISTS {self.SQL_USERS} ({self.USER_ID} INTEGER PRIMARY KEY )')
            
        except FileNotFoundError:
            f = open(self.SQL_SERVER,'w+')
            f.close()
            conn = sqlite3.connect(self.SQL_SERVER)
            c = conn.cursor()
            c.execute(f'CREATE TABLE IF NOT EXISTS {self.SQL_USERS} ({self.USER_ID} INTEGER PRIMARY KEY )')
            
        except Exception as e:
            print("Error in opening: "+str(e))
            return False
        # Check if the specific user exists
        try:
            c.execute(f'SELECT EXISTS (SELECT {self.USER_ID} from {self.SQL_USERS} WHERE {self.USER_ID} = {user_id})')
            is_existed = c.fetchone()[0]
            conn.commit()
            conn.close()
            return is_existed
        except Exception as e:
            print(e)
            return False

    def delete(self, user_id):
        # First try of connecting sqlite database
        try:
            conn = sqlite3.connect(self.SQL_SERVER)
            c = conn.cursor()
            c.execute(f'CREATE TABLE IF NOT EXISTS {self.SQL_USERS} ({self.USER_ID} INTEGER PRIMARY KEY )')
            
        except FileNotFoundError:
            f = open(self.SQL_SERVER,'w+')
            f.close()
            conn = sqlite3.connect(self.SQL_SERVER)
            c = conn.cursor()
            c.execute(f'CREATE TABLE IF NOT EXISTS {self.SQL_USERS} ({self.USER_ID} INTEGER PRIMARY KEY )')
            
        except Exception as e:
            print("Error in opening: "+str(e))
            return False
        # Check if the specific user exists
        try:
            c.execute(f'DELETE FROM {self.SQL_USERS} WHERE {self.USER_ID} = {user_id}')
            conn.commit()
            conn.close()
        except Exception as e:
            print(e)
            return False

    def user_list(self):
        try:
            conn = sqlite3.connect(self.SQL_SERVER)
            c = conn.cursor()
            c.execute(f'CREATE TABLE IF NOT EXISTS {self.SQL_USERS} ({self.USER_ID} INTEGER PRIMARY KEY )')
            
        except FileNotFoundError:
            f = open(self.SQL_SERVER,'w+')
            f.close()
            conn = sqlite3.connect(self.SQL_SERVER)
            c = conn.cursor()
            c.execute(f'CREATE TABLE IF NOT EXISTS {self.SQL_USERS} ({self.USER_ID} INTEGER PRIMARY KEY )')
            
        except Exception as e:
            print("Error in opening: "+str(e))
            return False
        # Check if the specific user exists
        try:
            c.execute(f'SELECT {self.USER_ID} FROM {self.SQL_USERS}')
            users = c.fetchall()
            conn.commit()
            conn.close()
            return users
        except Exception as e:
            print(e)
            return False
