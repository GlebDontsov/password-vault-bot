import psycopg2
from config_data.config import Config


class DataBase:
    def __init__(self, dbconfig: Config):
        self.conn = psycopg2.connect(
            host=dbconfig.db.db_host,
            dbname=dbconfig.db.database,
            user=dbconfig.db.db_user,
            password=dbconfig.db.db_password
        )

    def existsUser(self, user_id):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id FROM users WHERE user_id = %s;", (str(user_id),))
                flag = bool(len(cur.fetchall()))
        return flag

    def addUser(self, user_id, first_name, last_name):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("INSERT INTO users (user_id, first_name, last_name)  VALUES (%s, %s, %s)",
                            (user_id, first_name, last_name))

    def delUser(self, user_id):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))

    def createTableServiceData(self, user_id):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("CREATE TABLE user_%s "
                            "(Id SERIAL PRIMARY KEY, "
                            "service_name CHARACTER VARYING(50), "
                            "login CHARACTER VARYING(50), "
                            "encrypted_password TEXT);", (user_id,))

    def existsServiceData(self, user_id, service_name):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id FROM user_%s WHERE service_name = %s", (user_id, service_name.lower()))
                flag = bool(len(cur.fetchall()))
        return flag

    def setServiceData(self, user_id, service_name, login, password):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("INSERT INTO user_%s "
                            "(service_name, login, encrypted_password)  "
                            "VALUES (%s, %s, %s)",
                            (user_id, service_name, login, password))

    def updateServiceData(self, user_id, service_name, login, password):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("UPDATE user_%s SET login = %s, encrypted_password = %s "
                            "WHERE service_name = %s;",
                            (user_id, login, password, service_name))

    def getServiceData(self, user_id, service_name):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT login, encrypted_password "
                            "FROM user_%s "
                            "WHERE service_name = %s",
                            (user_id, service_name.lower()))
                return cur.fetchone()

    def delServiceData(self, user_id, service_name):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM user_%s "
                            "WHERE service_name = %s;", (user_id, service_name.lower()))

    def getServices(self, user_id):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT service_name FROM user_%s;",
                            (user_id,))
                return cur.fetchall()
