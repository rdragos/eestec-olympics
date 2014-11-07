import web
import datetime;
from gluon import *;

render = web.template.render('templates/')
urls = (
    '/login', 'login',
    '/', 'main_query',
    '/post_note', 'notes',
    '/terminal', 'terminal'
)

terminal_string = ""
first = 0
class terminal:
    def _process(self, question):
        question = question.lower()
        if question.find("cat e ceasul?") != -1:
            return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        else:
            return "Nu pot raspunde la aceasta intrebare!"

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
        data_str = ""
        for key in web.input():
            data_str += key
        credentials = data_str.split('\n');
        email = credentials[0]
        password = credentials[1]
        user = fetchUserByEmail(email)
        print email
        print password
        if user != None:
            return render.main_query()

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
    app = web.application(urls, globals())
    app.run()
