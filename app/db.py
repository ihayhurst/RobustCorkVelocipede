import vertica_python
import configparser

config = configparser.ConfigParser()
config.read("/app/config.ini")


def dbGetConn():
    dbhost = config["DATABASE"]["HOST"]
    dbport = config["DATABASE"]["PORT"]
    dbname = config["DATABASE"]["NAME"]
    dbuser = config["DATABASE"]["USER"]
    dbpw = config["DATABASE"]["PASSWORD"]
    conn_str = f"vertica://{dbuser}:{dbpw}@{dbhost}:{dbport}/{dbname}?connection_load_balance=True&connection_timeout=300&"
    conn = vertica_python.connect(dsn=conn_str)
    return conn


def getData(sql):
    try:
        conn = dbGetConn()
    except vertica_python.errors.QueryCanceled as e:
        (obj,) = e.args
        message = f"Context: {obj.context}\ Message: {obj.message}"
        print(message)
        return message, 101
    else:
        curr = conn.cursor()
        curr.execute(sql)
        data = curr.iterate()
        jsonData = [
            dict(zip([key[0] for key in curr.description], row)) for row in data
        ]
        curr.close()
        conn.close()
        return jsonData if jsonData else None
