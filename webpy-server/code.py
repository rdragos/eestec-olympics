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
        from user_handler import fetchUserByEmail;
        foundUsers = fetchUsersByFirstNameOrLastNameOrEmail(searchedValue)

        if (len(foundUsers) == 0):
            return "No user was found!"

        responseString = "I found %s results!" % len(foundUsers)
        if (len(foundUsers) == 1):
            responseString = "I found one result!"

        for index in range(0 , len(foundUsers)) :
            responseString += "%s %s %s\n" % (foundUsers[index].firstName, foundUsers[index].lastName , foundUsers[index].email)
        return responseString
    else:
        return "I can't answer this!"

terminal_string = ""
first = 0
class terminal:
    def _process(self, question):
        return processQuestion()

    def GET(self):
        global terminal_string
        return render.terminal(terminal_string)

    def POST(self):
        global terminal_string
        global first
        for key in web.input():
            current_string = key
        if current_string.lower().find("clear") != -1:
            terminal_string = ""
            first = 0
        else :
            pos = current_string.find(terminal_string)
            current_string = current_string[pos + len(terminal_string) :]
            current_string.replace('\n', '');
            if current_string.endswith("\n"):
                terminal_string += current_string + self._process(current_string)
            else:
                if first != 0:
                    terminal_string += current_string + self._process(current_string) + "\n"
                else:
                    first = 1
                    terminal_string += current_string + "\n" + self._process(current_string) + "\n"
        return render.terminal(terminal_string)

class login:
    def GET(self):
        return render.login()
    def POST(self):
        from user_handler import fetchUserByEmail;
        data_str = ""
        for key in web.input():
            data_str += key
        credentials = data_str.split('\n');
        email = credentials[0]
        password = credentials[1]
        user = fetchUserByEmail(email)
        if user == None:
            print "Naspa"
        print email
        print password
        return render.mainpage()

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
