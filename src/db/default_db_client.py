import psycopg2

class DefaultDbClient:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Connected to DB")
        except psycopg2.Error as e:
            print("Failed to connect to DB:", e)

    def disconnect(self):
        self.cursor.close()
        self.connection.close()
        print("Successful disconnect from database")

    def commit_transaction(self):
        self.connection.commit()

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()

            return self.fetch_data()
        except psycopg2.Error as e:
            print("Failed to execute query:", e)

            return []

    def fetch_data(self):
        if self.cursor.description is None:
            return None

        columns = [desc[0] for desc in self.cursor.description]
        results = self.cursor.fetchall()
        dict_results = [dict(zip(columns, row)) for row in results]

        return dict_results
