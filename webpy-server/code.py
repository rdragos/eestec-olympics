import web
import datetime;
import sys

render = web.template.render('templates/')
urls = (
    '/login', 'login',
    '/', 'main_query',
    '/post_note', 'notes',
    '/terminal', 'terminal',
    '/collect_tasks', 'collect_tasks'
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

if __name__ == "__main__":
    sys.path.append("../");
    print sys.path
    app = web.application(urls, globals())
    app.run()
