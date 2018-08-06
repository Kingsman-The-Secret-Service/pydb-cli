from changeme.registrar import Registrar
from changeme.database import Database
import sys

class TestRegistrar(object):
    
    db = Database(
            hostname="localhost", 
            dbname="testdatabase", 
            username="kavi", 
            password="password"
        )
    tablename = "APPLICATION"
    
    def setRegisterArgument(self):
        sys.argv = [sys.argv[0]]
        sys.argv.append('register')
        sys.argv.append('--AppID')
        sys.argv.append('REGISTRAR')
        sys.argv.append('--AppName')
        sys.argv.append('REGISTRAR')

    def test_register(self):

        self.setRegisterArgument()
        Registrar()
        sql = """ SELECT * FROM {0} WHERE AppID = 'REGISTRAR' AND AppName = 'REGISTRAR' """.format(self.tablename)
        assert self.db.rawQuery(sql)['rowcount'] > 0

    def setUnregisterArgument(self):
        sys.argv = [sys.argv[0]]
        sys.argv.append('unregister')
        sys.argv.append('--AppID')
        sys.argv.append('REGISTRAR')
        sys.argv.append('--AppName')
        sys.argv.append('REGISTRAR')
    
    def test_unregister(self):
        self.setUnregisterArgument()
        Registrar()
        sql = """ SELECT * FROM {0} WHERE AppID = 'REGISTRAR' AND AppName = 'REGISTRAR' AND IsDeleted = 1""".format(self.tablename)
        assert self.db.rawQuery(sql)['rowcount'] > 0