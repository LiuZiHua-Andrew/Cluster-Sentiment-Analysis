#-*- coding:utf-8 -*-
import BasicHttpServer
import sys,os

#if path is not exit
class case_no_file:

    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        return ServerException("{} not found",format(handler.path))

class case_existing_file:

    def test(self,handler):
        return os.path.isfile(handler.full_path)

    def act(self,handler):
        return handler.handle_file(handler.full_path)

class case_always_fail:

    def test(self, handler):
        return True

    def act(self, handler):
        return ServerException("Unknow object {}".format(handler.path))

class case_directory_index:

    def index_path(self,handler):
        # join index.html with http://localhost:8080/
        return os.path.join(handler.full_path,"index.html")

    def test(self, handler):
        return os.path.isdir(handler.full_path) and os.path.isfile(self.index_path(handler))

    def act(self,handler):
        return handler.handle_file(self.index_path(handler))


class RequestHandler(BasicHttpServer.CGIHTTPRequestHandler):

    Cases = [case_no_file,
             case_existing_file,
             case_directory_index,
             case_always_fail]

    full_path = ""

    #handling a GET request
    def do_GET(self):
        try:
            #complete path
            self.full_path = os.getcwd()+self.path

            for case in self.Cases:
                #Assign as an object of case class
                handler = case()
                if handler.test(self):
                    handler.act(self)
                    break

        except Exception as msg:
            self.handle_error(msg)

    def handle_file(self, full_path):
        try:
            with open(full_path, 'rb') as reader:

                content = reader.read()

            self.send_content(content,status=200)

        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(self.path, msg)
            self.handle_error(msg)

    def send_content(self,page,status):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()
        self.wfile.write(page)

   #Error Response Page
    Error_Page = """\
                <html>
                <body>
                <h1>Error: {status}</h1>
                <h2>Error accessing {path}</h2>
                <p>{msg}</p>
                </body>
                </html>
                """

    def handle_error(self, msg):
        content = self.Error_Page.format(status=404,path=self.path, msg=msg)
        self.send_content(content.encode(),status=404)

#SERVER EXCEPTION CLASS
class ServerException(Exception):
    pass




if __name__ == '__main__':
    serverAddress = ('localhost',8080)
    server = BasicHttpServer.HTTPServer(serverAddress,RequestHandler)
    server.serve_forever()