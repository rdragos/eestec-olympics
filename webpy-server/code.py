import web
import datetime;
import sys

render = web.template.render('templates/')
urls = (
    '/login', 'login',
    '/', 'main_query',
    '/post_note', 'notes',
    '/terminal', 'terminal'
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

        responseString = "I found %s results!" % len(foundUsers)
        if (len(foundUsers) == 1):
            responseString = "I found one result!"

        for index in range(0 , len(foundUsers)) :
            responseString += "%s %s %s\n" % (foundUsers[index].firstName, foundUsers[index].lastName , foundUsers[index].email)
        return responseString
    else:
        return "I can't answer this!"

class terminal:
    string = ""
    def _process(self, question):
        resp = processQuestion(question)
        print resp
        return resp

    def GET(self):
        return render.terminal("")

    def POST(self):
        global terminal_string
        global first
        current_string=""
        for key in web.input():
            current_string = key
        current_string.replace('\n', '');
        if current_string.endswith("\n"):
             render.terminal(
                     string = current_string + self._process(current_string))
        else:
            return render.terminal(current_string +  "\n" + self._process(current_string) + "\n")

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
        global logged_in
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
            raise web.seeother('/')

class main_query:
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
