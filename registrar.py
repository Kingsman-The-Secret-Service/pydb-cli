import sys, argparse, logging, datetime
from database import Database

class Registrar():

    db = Database(
            hostname="localhost", 
            dbname="testdatabase", 
            username="kavi", 
            password="password"
        )
    tablename = "APPLICATION"

    description = """
---------------------------------------------------------
Application Registrar 
=====================
Example:
1) To Register
    python {0} register --AppID="123ABC" --AppName="QNAP"
    python {0} register --AppID "123ABC" --AppName "QNAP"
    python {0} register -id="123ABC" -n="QNAP"
    python {0} register -id "123ABC" -n "QNAP"
2) To Unregister
    python {0} unregister --AppID="123ABC" --AppName="QNAP"
    python {0} unregister --AppID "123ABC" --AppName "QNAP"
    python {0} unregister -id="123ABC" -n="QNAP"
    python {0} unregister -id "123ABC" -n "QNAP"
---------------------------------------------------------
""".format(sys.argv[0])

    def __init__(self):
        parser = argparse.ArgumentParser(description=self.description, formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('action', choices= ['register', 'unregister'], action = "store", default = 'register', help="Action to register | deregister your Application ")
        parser.add_argument('-id', '--AppID', required=True, action = "store", help="ID of the Application")
        parser.add_argument('-n', '--AppName', required=True, action = "store", help="Name of the Application")
        arg = parser.parse_args()

        self.AppID = arg.AppID
        self.AppName = arg.AppName

        if arg.action == 'register':
            self.register()
        elif arg.action == 'unregister':
            self.unregister()
           
    def register(self):
        
        logging.info("Start to Register App ID: {0}, App Name: {1}".format(self.AppID, self.AppName))

        data = {
            "AppID" :  self.AppID,
            "AppName": self.AppName,
        }

        if self.db.insert(self.tablename, **data):
            logging.info("Registered App ID: {0}, App Name: {1}".format(self.AppID, self.AppName))
            return True

        logging.critical("Failed to Register App ID: {0}, App Name: {1}".format(self.AppID, self.AppName))
        return False    

    def unregister(self):

        logging.info("Start to Unregister App ID: {0}, App Name: {1}".format(self.AppID, self.AppName))

        where = "AppID = '{0}' AND AppName = '{1}'".format(self.AppID, self.AppName)
        data = {
            "UnregisterdDate": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "IsDeleted" :  1,
        }

        if self.db.update(self.tablename, where = where, **data):
            logging.info("Unregistered App ID: {0}, App Name: {1}".format(self.AppID, self.AppName))
            return True
        
        logging.critical("Failed to unregistered App ID: {0}, App Name: {1}".format(self.AppID, self.AppName))
        return False