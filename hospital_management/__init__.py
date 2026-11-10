import pymysql

# Enable PyMySQL as MySQLdb for Django MySQL driver compatibility
try:
    pymysql.install_as_MySQLdb()
except Exception:
    pass

