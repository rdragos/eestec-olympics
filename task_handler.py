import psycopg2
import psycopg2.extras
import pprint
import json
conn_string = "host='91.234.168.44' dbname='postgres' user='postgres' password='postgres'"

class Task :
    def __init__(self , id , userId , title , content , startDate, endDate, completed = False) :
        self.id = id
        self.userId = userId
        self.title = title
        self.content = content
        self.startDate = startDate
        self.endDate = endDate
        self.completed = completed
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

def fetchTasksFromDb(offset , limit) :
    sqlQuery = "SELECT * FROM Tasks LIMIT %s OFFSET %s" % (limit, offset)
    connection = psycopg2.connect(conn_string)
    cursor = connection.cursor()
    cursor.execute(sqlQuery)
    records = cursor.fetchall()
    recordsLength = len(records)

    tasks = []

    for index in range(0 , recordsLength) :
        task = Task(records[index][0], records[index][1], records[index][2], records[index][3], records[index][4], records[index][5], records[index][6])
        tasks.append(task)
    connection.close()
    return tasks

def fetchTasksOfUser(userId):
    sqlQuery = "SELECT Tasks.* FROM Users Join Tasks On Tasks.UserId = Users.Id where Users.id = %s" % userId
    connection = psycopg2.connect(conn_string)
    cursor = connection.cursor()
    cursor.execute(sqlQuery)
    record = cursor.fetchall();
    if (record == None):
        return None
    tasks = []
    for r in record:
        tasks.append(Task(r[0],r[1],r[2],r[3],r[4],r[5],r[6]))
    return tasks

def fetchTaskFromDb(id) :
    sqlQuery = "SELECT * FROM Tasks WHERE Id = %s" % id
    connection = psycopg2.connect(conn_string)
    cursor = connection.cursor()
    cursor.execute(sqlQuery)
    record = cursor.fetchone()

    if (record == None) :
        return None

    connection.close()
    return Task(record[0],record[1],record[2],record[3],record[4],record[5],record[6])

def createTask(task) :
    sqlInsert = "INSERT INTO Tasks (userId, title, content, startDate, endDate, completed) " +\
                "VALUES (%s,\'%s\', \'%s\', \'%s\', \'%s\' , %s)" % (task.userId, task.title, task.content, task.startDate, task.endDate , task.completed) +\
                "RETURNING Id"
    connection = psycopg2.connect(conn_string)
    cursor = connection.cursor()
    cursor.execute(sqlInsert)
    returnedId = cursor.fetchone()
    connection.commit()
    connection.close()
    return returnedId[0]

def updateTask(id , task) :
    sqlUpdate = "UPDATE Tasks SET userId=%s,title=\'%s\',content=\'%s\',startDate=\'%s\',endDate=\'%s\',completed=%s WHERE id=%s" % (task.userId, task.title, task.content, task.startDate, task.endDate, task.completed, id)
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
