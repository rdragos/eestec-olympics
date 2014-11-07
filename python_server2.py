import BaseHTTPServer
import time
import sys

HOST_NAME = '172.20.24.146' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.

def get_fields (request_string):
    request_string = request_string[1:]
    pairs = request_string.split('&')
    ret = {}
    for i in range(0, len(pairs)):
       pair_fields = pairs[i].split('=')
       if len(pair_fields) == 2:
           ret[pair_fields[0]] = pair_fields[1]
    return ret

class RedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        print get_fields(s.path)
        s.send_response(200)
    def do_GET(s):
        s.do_HEAD()

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), RedirectHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
