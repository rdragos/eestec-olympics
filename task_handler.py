import psycopg2
import psycopg2.extras
import pprint

conn_string = "host='91.234.168.44' dbname='postgres' user='postgres' password='postgres'"

class Task :
	def __init__(self , id , userId , title , content , startDate, endDate) :
		self.id = id
		self.userId = userId
		self.title = title
		self.content = content
		self.startDate = startDate
		self.endDate = endDate

def fetchTasksFromDb(offset , limit) :
	sqlQuery = "SELECT * FROM Tasks LIMIT %s OFFSET %s" % (limit, offset)
	connection = psycopg2.connect(conn_string)
	cursor = connection.cursor()
	cursor.execute(sqlQuery)
	records = cursor.fetchall()
	recordsLength = len(records)
	
	tasks = []

	for index in range(0 , recordsLength) :
		task = Task(records[index][0], records[index][1], records[index][2], records[index][3], records[index][4], records[index][5])
		tasks.append(task)
	connection.close()
	return tasks

def fetchTaskFromDb(id) :
	sqlQuery = "SELECT * FROM Tasks WHERE Id = %s" % id
	connection = psycopg2.connect(conn_string)
	cursor = connection.cursor()
	cursor.execute(sqlQuery)
	record = cursor.fetchone()
	connection.close()
	return Task(record[0],record[1],record[2],record[3],record[4],record[5])

def createTask(task) :
	sqlInsert = "INSERT INTO Tasks (userId, title, content, startDate, endDate) " +\
				"VALUES (%s,\'%s\', \'%s\', \'%s\', \'%s\')" % (task.userId, task.title, task.content, task.startDate, task.endDate) +\
				"RETURNING Id"
	connection = psycopg2.connect(conn_string)
	cursor = connection.cursor()
	cursor.execute(sqlInsert)
	returnedId = cursor.fetchone()
	connection.commit()
	connection.close()
	return returnedId[0]

def updateTask(id , task) :
	sqlUpdate = "UPDATE Tasks SET userId=%s,title=\'%s\',content=\'%s\',startDate=\'%s\',endDate=\'%s\' WHERE id=%s" % (task.userId, task.title, task.content, task.startDate, task.endDate, id)
	connection = psycopg2.connect(conn_string)
	cursor = connection.cursor()
	cursor.execute(sqlUpdate)
	connection.commit()
	connection.close()

def deleteTask(id) :
	sqlDelete = "DELETE FROM Tasks WHERE id=%s" % id
	connection = psycopg2.connect(conn_string)
	cursor = connection.cursor()
	cursor.execute(sqlDelete)
	connection.commit()
	connection.close()

if __name__ == "__main__" :
	newTask = Task(0 , 7 , "Py newTask" , "Test" , '01.01.2009' , '02.01.2009')
	newTask.id = createTask(newTask)
	fetchTasksFromDb(0 , 10)
	deleteTask(newTask.id)
