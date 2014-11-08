import web
import datetime
import sys
import json

render = web.template.render('templates/')
urls = (
    '/login_page', 'login_page',
    '/mainpage', 'mainpage',
    '/post_note', 'notes',
    '/terminal', 'terminal',
    '/bot' , 'bot',
    '/users' , 'users',
    '/login' , 'login'
)

def processQuestion(question):
    questionLowered = question.lower()
    if questionLowered.find("what is time?") != -1:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    if questionLowered.find("who is") != -1:
        index = questionLowered.find("who is") + len("who is") + 1
        searchedValue = question[index:]
        from user_handler import fetchUsersByFirstNameOrLastNameOrEmail;
        foundUsers = fetchUsersByFirstNameOrLastNameOrEmail(searchedValue)

        if (len(foundUsers) == 0):
            return "No user was found!\n\n"

        responseString = "I found %s results!\n" % len(foundUsers)
        if (len(foundUsers) == 1):
            responseString = "I found one result!\n"

        for index in range(0 , len(foundUsers) - 1) :
            responseString += "%s %s %s\n" % (foundUsers[index].firstName, foundUsers[index].lastName , foundUsers[index].email)
        responseString += "%s %s %s" % (foundUsers[len(foundUsers) - 1].firstName, foundUsers[ len(foundUsers) - 1].lastName , foundUsers[ len(foundUsers) - 1].email)
        return responseString
    else:
        return "I can't answer this!"

class terminal:
    def GET(self):
        return render.terminal()

def getCompletedTasksPercent(userId):
    from task_handler import fetchTasksOfUser
    tasks = fetchTasksOfUser(userId)
    completed = 0
    total = 0
    for task in tasks:
        if task.completed:
            completed = completed + 1
        total = total + 1
    return (completed / total)

class login_page:
    def GET(self):
        return render.login()

    def POST(self):
        from user_handler import fetchUserByEmail;
        data_str = ""
        for key in web.input():
            data_str += key
        credentials = data_str.split('\n')
        email = credentials[0]
        password = credentials[1]
        user = fetchUserByEmail(email)
        if user == None:
            raise Exception("The user doesn't exist")
        else:
            if password != user.password:
                raise Exception("Password is incorrect")
        return "OK"

class bot:
    def GET(self):
        terminal_string = web.input()
        return processQuestion(terminal_string.question)

class login:
    def GET(self):
        from user_handler import fetchUserByEmail;
        webInput = web.input()
        if ("email" in webInput and "password" in webInput):
            email = webInput.email
            password = webInput.password
            user = fetchUserByEmail(email)
            if user == None:
                return "BAD"
            else:
                if password != user.password:
                    return "BAD"
            return "OK"
        else:
            return "BAD"

class users:
    def GET(self):
        user_data = web.input()
        if ("id" in user_data.keys()) :
            from user_handler import fetchUserById;
            user = fetchUserById(user_data.id)
            if user == None:
                raise Exception("The user doesn't exist")
            user.password = "*****"
            return json.dumps(user.__dict__)

        if ("email" in user_data.keys()) :
            from user_handler import fetchUserByEmail;
            user = fetchUserByEmail(user_data.email)
            if user == None:
                raise Exception("The user doesn't exist")
            user.password = "*****"
            return json.dumps(user.__dict__)

        raise Exception("Missing id parameter")

class mainpage:
    def GET(self):
        return render.mainpage()
    def POST(self):
        pass

class collect_tasks:
    def GET(self):
        from task_handler import fetchTasksFromDb
        alltasks = fetchTasksFromDb(0, 2)
        return render.collect_tasks([x.__dict__ for x in alltasks])

class notes:
    def GET(self):
        return render.post_note()
    def POST(self):
        print(web.input())
        print("Post it")

class alter_task:
    def POST(self):
        print(web.input())
        from task_handler import updateTask
        from task_handler import fetchTaskFromDb
        updateTask(web.input().id, web.input())
        print(fetchTaskFromDb(web.input().id).content)
class create_new_task:
     def POST(self):
        from task_handler import createTask
        createTask(web.input())
if __name__ == "__main__":
    sys.path.append("../");
    print sys.path
    app = web.application(urls, globals())
    app.run()
