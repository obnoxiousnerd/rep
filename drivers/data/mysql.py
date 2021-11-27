from driver_class import DataDriver
import mysql.connector
from mysql.connector import errorcode
from getpass import getpass


class MySQLDataDriver(DataDriver):
    def load(self):
        mysql_config = {
            "connect": {
                "host": self.config.get("host") or "localhost",
                "port": self.config.get("port") or 3306,
                "username": self.config.get("username"),
                "database": self.config.get("database"),
            },
            "table": self.config.get("table"),
        }
        # Bulk check all properties. If any one is absent, tell user to
        # configure them.
        if None in mysql_config or None in mysql_config["connect"]:
            self.logger.fatal(
                "One or more required properties are missing in the configuration. "
                + "Please make sure you have specified "
                + "the host, port, database and username properties in the configuration file."
            )

        password = getpass("Enter the password for your MySQL account: ")
        mysql_config["connect"]["password"] = password

        try:
            # The connect function accepts keyword arguments
            # so passing an dict with the arguments also works.
            cnx = mysql.connector.connect(**mysql_config["connect"])
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.logger.fatal(
                    "Access to the database was denied. "
                    + "Please double check your credentials."
                )
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.logger.fatal("Database does not exist")
            else:
                self.logger.fatal(
                    "An error occured while connecting to the database: %s", err
                )
            exit(1)
        cur = cnx.cursor(dictionary=True)

        # Use the first word as the table name because attacks where
        # key is set to something like `students WHERE 1=1` can be
        # prevented.
        query = f"SELECT * FROM {mysql_config['table'].split()[0]};"
        self.logger.info(query)
        cur.execute(query)
        data = [row for row in cur]

        cnx.close()
        return data
