import urllib
from sqlalchemy import create_engine


def connect_to_database():
    params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                     "SERVER=DESKTOP-LSOCJD8\SQLEXPRESS;"
                                     "DATABASE=NCAA_Basketball;"
                                     "Trusted_Connection=yes")

    engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
    connection = engine.connect()
    return connection


def test_connection(connection):
    result = connection.execute("SELECT SYSTEM_USER AS me")
    row = result.fetchone()
    print(row['me'])


def run_main():
    connection = connect_to_database()
    test_connection(connection)


if __name__ == "__main__":
    run_main()
