from drivers.data.csv import CSVDataDriver
from drivers.data.mysql import MySQLDataDriver
from drivers.email.smtp import SMTPMailDriver

data_drivers = {"csv": CSVDataDriver, "mysql": MySQLDataDriver}
email_drivers = {"smtp": SMTPMailDriver}