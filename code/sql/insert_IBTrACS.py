import pymysql


class MSSQL(object):
    instance = None
    def __init__(self, host: str = '127.0.0.1', port: int = 3306, user: str = 'root',
                 pwd: str = '123456', database: str = 'tropicalcyclone', charset: str = 'utf8') -> None:
        """
        database operation class
        :param host: the database server host name
        :param port: the database server port number
        :param user: the database server user name
        :param pwd: the database server key
        :param database: the database name
        :param charset: the encode of the database server
        """
        self._conn = pymysql.connect(host=host, port=port, user=user, passwd=pwd, db=database, charset=charset)
        self._cur = self._conn.cursor()

    @classmethod

    def get_instance(cls):
        """
        get a class instance just only one.
        :return:the class instance
        """
        if cls.instance:
            return cls.instance
        else:
            cls.instance = MSSQL()
            return cls.instance

    def insert_user_2_db(self, data):
        sql = "INSERT INTO IBTrACS(ShortHand_Id,SEASON, BASIN, NAME, ISO_TIME, YEAR, MONTH, DAY, HOUR, LAT, LON, WMO_WIND, WMO_PRES, DIST2LAND) VALUES " \
                  "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self._cur.execute(sql, data)
        self._conn.commit()

if __name__ == '__main__':
    my = MSSQL()
    import pandas as pd

    df = pd.read_csv('pull_download.csv',header=None)
    for i in df.index[1:]:
        data = []
        data.append(str(df.at[i,1]))
        data.append(str(df.at[i,2]))
        data.append(str(df.at[i,3]))
        data.append(str(df.at[i,4]))
        data.append(str(df.at[i,5]))
        data.append(str(df.at[i,6]))
        data.append(str(df.at[i,7]))
        data.append(str(df.at[i,8]))
        data.append(str(df.at[i,9]))
        data.append(str(df.at[i,10]))
        data.append(str(df.at[i,11]))
        data.append(str(df.at[i,12]))
        data.append(str(df.at[i,13]))
        data.append(str(df.at[i,14]))
        my.insert_user_2_db(tuple(data))
    print("successfully")