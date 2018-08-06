import datetime
from changeme.database import Database

class TestDatabase(object):

    db = Database(
            hostname="localhost", 
            dbname="testdatabase", 
            username="kavi", 
            password="password"
        )
    tablename = "APPLICATION"

    def test_rawQueryDropTable(self):

        sql = """ DROP TABLE IF EXISTS `{0}`""".format(self.tablename)

        assert self.db.rawQuery(sql)['commit'] == True
    
    def test_rawQueryCreateTable(self):

        sql = """CREATE TABLE {0} (
            `id` INT NOT NULL AUTO_INCREMENT, 
            `AppID`  VARCHAR(255) NOT NULL,
            `AppName` VARCHAR(255) NOT NULL,
            `RegisteredDate` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `UnregisterdDate` TIMESTAMP NULL,
            `IsDeleted` BOOLEAN NOT NULL DEFAULT 0,
            PRIMARY KEY ( id ),
            UNIQUE KEY name (AppID))""".format(self.tablename)
    
        assert self.db.rawQuery(sql)['commit'] == True

    def test_rawQueryCreateTableFails(self):

        sql = """CREATE TABLE {0} (
            `id` INT NOT NULL AUTO_INCREMENT, 
            `AppID`  VARCHAR(255) NOT NULL,
            `AppName` VARCHAR(255) NOT NULL,
            `RegisteredDate` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            `UnregisterdDate` TIMESTAMP NULL,
            `IsDeleted` BOOLEAN NOT NULL DEFAULT 0,
            PRIMARY KEY ( id ),
            UNIQUE KEY name (AppID))""".format(self.tablename)
    
        assert self.db.rawQuery(sql)['commit'] == False

    def test_insertValidData(self):
        data = { "AppID" : "ABCD", "AppName": "QNAP"}
        assert self.db.insert(self.tablename, **data) > 0
    
    def test_insertExistData(self):
        data = { "AppID" : "ABCD", "AppName": "QNAP"}
        assert self.db.insert(self.tablename, **data) == None
    
    def test_updateValidData(self):
        data = { "AppID" : "WXYZ", "AppName": "MSYS"}
        self.db.insert(self.tablename, **data)

        where = "AppID = 'WXYZ' AND AppName = 'MSYS'"
        data = {
            "UnregisterdDate": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "IsDeleted" :  1,
        }
        assert self.db.update(self.tablename, where = where, **data) > 0

    def test_updateInValidData(self):

        where = "AppID = 'XXXX' AND AppName = 'XXXX'"
        data = {
            "UnregisterdDate": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "IsDeleted" :  1,
        }
        assert self.db.update(self.tablename, where = where, **data) == 0

    def test_deleteValidData(self):
        where = "AppID = %s"
        assert self.db.delete(self.tablename, where, "WXYZ" ) > 0
    
    def test_deleteInValidData(self):
        where = "AppID = %s"
        assert self.db.delete(self.tablename, where, "XXXX" ) == 0
