import psycopg2
import pprint

conn_string = "host='91.234.168.44' dbname='postgres' user='postgres' password='postgres'"

class Task :
	def __init__(self , id , userId , title , content , startDate, endDate) :
		self.id = id
		self.userId = userId
		self.title = title
		self.content = content
		self.startDate = startDate
		self,endDate = endDate
	def __init__(self , tuplet) :
		self.id = tuplet[0]
		self.userId = tuplet[1]
		self.title = tuplet[2]
		self.content = tuplet[3]
		self.startDate = tuplet[4]
		self.endDate = tuplet[5]


def fetchTasksFromDb(offset , limit) :
	sqlQuery = "SELECT * FROM Tasks LIMIT %s OFFSET %s" % (limit, offset)
	connection = psycopg2.connect(conn_string)
	cursor = connection.cursor()
	cursor.execute(sqlQuery)
	records = cursor.fetchall()
	recordsLength = len(records)

	tasks = []

	for index in range(0 , recordsLength) :
		task = Task(records[index])
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
	return Task(record)

def updateTask(id , task) :
	sqlUpdate = "UPDATE Tasks SET userId=%s,title=\'%s\',content=\'%s\',startDate=\'%s\',endDate=\'%s\' WHERE id=%s" % (task.userId, task.title, task.content, task.startDate, task.endDate, id)
	print sqlUpdate
	connection = psycopg2.connect(conn_string)
	cursor = connection.cursor()
	cursor.execute(sqlUpdate)
	connection.close()

if __name__ == "__main__" :
	tasks = fetchTasksFromDb(0 , 10)
	oneTask = fetchTaskFromDb(tasks[1].id)
	oneTask.content = "Updated content34"
	updateTask(oneTask.id, oneTask)
	oneTask = fetchTaskFromDb(tasks[1].id)
	pprint.pprint(oneTask.content)
