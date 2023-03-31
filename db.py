import sqlite3


class Serializer:
    pass


class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("base1.db", check_same_thread=False)
        self.cur = self.connection.cursor()

    def __del__(self):
        self.cur.close()
        self.connection.close()
        print("Succesfully closed the connection to Databse!")

    def drop_table(self, name='wallet'):
        self.connection.execute(f"DROP TABLE {name}")
        print(f"Succesfully dropped the {name} table!")

    def generic_create_record(self, tname: str, column_values: dict):
        keys = tuple(column_values.keys())
        values = tuple(column_values.values())
        query = f"INSERT INTO {tname} {keys} VALUES ("
        for i in range(len(keys)-1):
            query += '?, '
        query += '?)'
        self.connection.execute(query, values)
        self.connection.commit()
        print("Succesfully pushed new transaction to database!", query)
        print(values)

    def display_table(self, name='wallet'):
        response = self.connection.execute(f"SELECT * FROM {name}").fetchall()
        return response

    def edit_value(self, name, values: dict, condition: tuple):

        query = f"UPDATE {name} SET "
        for key in values:
            query += f"{key}=?, "

        # Make query string a list to delete last comma that causes SyntaxError
        nquery = list(query)
        # Get rid of a comma following the last item
        nquery.pop(-2)
        nquery = ''.join(nquery)
        
        nquery += f"WHERE {condition[0]}=?"
        vals = list(values.values())
        vals.append(condition[-1])
        vals = tuple(vals)

        self.connection.execute(nquery, vals)
        self.connection.commit()

    def show_tables(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = self.cur.fetchall()

        # wyświetlenie listy tabel
        for table in tables:
            print(table[0])

    def create_table(self, name: str, values_dict: dict) -> None:
        """Create generic table in sqlite3"""

        # CREATE TABLE wallet (publickey TEXT PRIMARY KEY, privkey TEXT UNIQUE, address TEXT UNIQUE, amount FLOAT)
        query = f"CREATE TABLE {name} (id INTEGER PRIMARY KEY"

        for key, value in values_dict.items():
            query += ', '
            query += key.strip('\' ')
            query += ' ' + value.strip('\'') + ' '
        query += ")"    
        print(query)

        self.cur.execute(query)

        print("SUCCESFULLY CREATED THE TABLE!")
    # drop_wallet_table()
    # create_wallet_table()
    # insert_values("ADAS", 12573)
    # print(display_table())

    # create_table("transactions", {"buyer": "text", "seller": "text", "amount": "text"})

    def get_all_records_from_table(self, name):
        query = f"SELECT * FROM {name}"
        response =  self.cur.execute(query).fetchall()
        return response

    def clear_table(self, name):
        query = f'DELETE FROM {name}'
        self.cur.execute(query)
        self.connection.commit()
        print('succesfuly cleared')

    # def get_table_data(self, table_name, condition={}):
    #     query = f"SELECT * FROM {table_name}"
    #     if condition is {}:
    #         self.cur.execute(query)
    #     else:
    #         for key, value in condition.items():
    #             query += f" WHERE {key}={value}"
    #         self.cur.execute(query)

    #     rows = self.cur.fetchall()
    #     col_names = [i[0] for i in self.cur.description]
    #     result = []
    #     for row in rows:
    #         row_dict = dict(zip(col_names, row))
    #         result.append(row_dict)

    #     return result
    
    def get_table_data(self, table_name, condition={}):

        cur = self.connection.cursor()
        query = f"SELECT * FROM {table_name}"
        if condition:
            query += " WHERE " + " AND ".join(f"{k}={v}" for k, v in condition.items())

        cur.execute(query)
        rows = cur.fetchall()

        col_names = [i[0] for i in cur.description]
        result = []
        for row in rows:
            row_dict = dict(zip(col_names, row))
            result.append(row_dict)
    
        return result


    def execute_query(self, query):
        self.cur.execute(query)
        self.connection.commit()

    def is_pushed(self, name, query_obj):
        response = self.cur.execute(f"SELECT * FROM {name} WHERE {query_obj[0]}={query_obj[1]}").fetchall()
        if len(response) > 0:
            return True
        return False



def create_trigger():
    db = sqlite3.connect("base.db")
    def my_function():
        print("New lottery added!")
    db.create_function("my_function", 0, my_function)
    query = '''CREATE TRIGGER IF NOT EXISTS nowy_rekord_trigger
             AFTER INSERT ON loteria
             BEGIN
                 SELECT my_function();
             END'''
    db.execute(query)
    
    db.close()
# dbase = Database()