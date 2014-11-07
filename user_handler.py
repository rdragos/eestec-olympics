import psycopg2
import psycopg2.extras
import pprint

conn_string = "host='91.234.168.44' dbname='postgres' user='postgres' password='postgres'"

class User : 
	def __init__(self, id, email, password, firstName, lastName):
		self.id = id
		self.email = email
		self.password = password
		self.firstName = firstName
		self.lastName = lastName

def fetchUserById(id):
	sqlQuery = "SELECT * FROM Users WHERE Id = %s" % id
	connection = psycopg2.connect(conn_string)
	cursor = connection.cursor()
	cursor.execute(sqlQuery)
	record = cursor.fetchone()

	if (record == None) :
		return None

	connection.close()
	return User(record[0],record[1],record[2],record[3],record[4])

def fetchUserByEmail(email):
	sqlQuery = "SELECT * FROM Users WHERE Email = \'%s\'" % email
	connection = psycopg2.connect(conn_string)
	cursor = connection.cursor()
	cursor.execute(sqlQuery)
	record = cursor.fetchone()

	if (record == None) :
		return None

	connection.close()
	return User(record[0],record[1],record[2],record[3],record[4])

def createUser(user):
	sqlInsert = "INSERT INTO Users (email, password, firstName, lastName) " +\
				"VALUES (\'%s\', \'%s\', \'%s\', \'%s\')" % (user.email, user.password, user.firstName, user.lastName) +\
				"RETURNING Id"
	connection = psycopg2.connect(conn_string)
	cursor = connection.cursor()
	cursor.execute(sqlInsert)
	returnedId = cursor.fetchone()
	connection.commit()
	connection.close()
	return returnedId[0]

def updateUser(id , user) :
	sqlUpdate = "UPDATE Users SET email=\'%s\',password=\'%s\',firstName=\'%s\',lastName=\'%s\' WHERE id=%s" % (user.email, user.password, user.firstName, user.lastName, id)
	connection = psycopg2.connect(conn_string)
	cursor = connection.cursor()
	cursor.execute(sqlUpdate)
	connection.commit()
	connection.close()

if __name__ == "__main__" :
	newUser = User(0 , "sarpele200@yahoo.com" , "mihai" , "Mihai" , "Catalin")
	newUser.id = createUser(newUser)
	fetchUserById(newUser.id)
	fetchUserByEmail(newUser.email)
	newUser.firstName = "Botezatu"
	updateUser(newUser.id, newUser)
