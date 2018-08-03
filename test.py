import database

# CONNECT
db = database.Database(hostname="localhost", dbname="testdatabase", username="kavi", password="password")

sql = """CREATE TABLE APPLICATION (
            id INT NOT NULL AUTO_INCREMENT, 
            name  CHAR(20) NOT NULL,
            metadata VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL,
            PRIMARY KEY ( id ),
            UNIQUE KEY name (name))"""
    
db.rawQuery(sql)

tablename = "APPLICATION"

# INSERT
# kwargs
data = {"name": "whatsapp", "metadata": "messaging, chatting", "url": "http://web.whatsapp.com"}
db.insert(tablename, **data)

data = {"name": "amazon", "metadata": "shopping, retailer", "url": "http://amazon.com"}
db.insert(tablename, **data)

data = {"name": "chrome", "metadata": "browser, google", "url": "http://google.com"}
db.insert(tablename, **data)

# DELETE
deleteCondition="name = %s"
db.delete(tablename, deleteCondition, "chrome")

