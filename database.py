import MySQLdb, json, logging


class Database(object):

    __instance   = None
    __host       = None
    __user       = None
    __password   = None
    __database   = None
    __session    = None
    __connection = None
    
    def __init__(self, filename = None, 
                        hostname = None, 
                        dbname = None, 
                        username = None, 
                        password = None, 
                        port =3306):
        
        if filename: // TODO
            data = FileReader(filename)['db_info']
            self.hostname = data["hostname"]
            self.dbname = data["dbname"]
            self.username = data["username"]
            self.password = data["password"]
        else:
            self.hostname = hostname
            self.dbname = dbname
            self.username = username
            self.password = password
            self.port = port

    def __open(self):
        try:
            connection = MySQLdb.connect(self.hostname,  self.username, self.password, self.dbname)
            self.__connection = connection
            self.__session = connection.cursor()
        except MySQLdb.Error as e:
            logging.critical("MySQL connection failure, Exception: %s" % str(e))
            exit()
    
    def __close(self):
        self.__session.close()
        self.__connection.close()

    def rawQuery(self, sql):

        logging.info(sql)

        self.__open()
        try:
            self.__session.execute(sql)
        except Exception as e:
            logging.critical("Failed to execute sql query, Exception: %s" % str(e))
            self.__connection.rollback()
        else:
            self.__connection.commit()
        finally:
            self.__close()

    def insert(self, tablename, **kwargs):

        values = None
        query = "INSERT INTO %s" % tablename

        if kwargs:
            columns =  kwargs.keys()
            columnData = ",".join(["`%s`"] * len(columns)) %  tuple (columns)
            values = tuple(kwargs.values())
            valueData = ",".join(["%s"]*len(values))
            query += "(" + columnData + ") VALUES (" + valueData + ")"

        self.__open()
        try:
            self.__session.execute(query, values)
        except Exception as e:
            logging.critical("Failed to insert data, Exception: %s" % str(e))
            self.__connection.rollback()
        else:
            self.__connection.commit()
        finally:
            self.__close()


    def delete(self, tablename, where=None, *args):
        
        query = "DELETE FROM %s" % tablename
        values = tuple(args)
        deletedRows = None

        if where:
            query += ' WHERE %s' % where
        

        logging.info(query)

        self.__open()
        try:
            self.__session.execute(query, values)
        except Exception as e:
            logging.critical("Failed to delete data, Exception: %s" % str(e))
            self.__connection.rollback()
        else:
            self.__connection.commit()
            deletedRows = self.__session.rowcount
        finally:
            self.__close()

        return deletedRows


class FileReader(object):

    pass
        