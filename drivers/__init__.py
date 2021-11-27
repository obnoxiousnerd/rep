from drivers.data.csv import CSVDataDriver
from drivers.data.mysql import MySQLDataDriver

data_drivers = {"csv": CSVDataDriver, "mysql": MySQLDataDriver}
