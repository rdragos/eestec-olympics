import web
import datetime
import sys
import json

render = web.template.render('templates/')
urls = (
    '/login', 'login',
    '/mainpage', 'mainpage',
    '/post_note', 'notes',
    '/terminal', 'terminal',
    '/bot' , 'bot',
    '/users' , 'users'
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
            return "No user was found!"

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

class bot:
    def GET(self):
        terminal_string = web.input()
        return processQuestion(terminal_string.question)

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

class login:
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

class notes:
    def GET(self):
        return render.post_note()
    def POST(self):
        print(web.input())
        print("Post it")

if __name__ == "__main__":
    sys.path.append("../");
    print sys.path
    app = web.application(urls, globals())
    app.run()
