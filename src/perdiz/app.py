import multiprocessing
from .response import Response
#from router import Rota

#import gunicorn.app.base
import ssl,secrets,string,json
#alphabet = string.ascii_letters + string.digits
#token = ''.join(secrets.choice(alphabet) for i in range(256))
#print(token)




def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1
class AppClass:
    __routerPost = {}
    __routerGet = {}
    __routerOther = None
    def __init__(self,environ,start_response):
        self.__environ = environ
        self.__res = Response()
        try:
            #print(environ)
            body_size = int(environ.get('CONTENT_LENGTH',0))
        except (ValueError):
            print("error: "+str(ValueError))
            body_size = 0
        body = environ["wsgi.input"].read(body_size)
        
        self.__header = {
            "method":environ["REQUEST_METHOD"],
            "path":environ["PATH_INFO"],
            "body":body,
            "body_length":body_size
        }
        for key,value in environ.items():
            pass
            #print(f"{key}: {value}")
        print("\n")
        #print(environ["REQUEST_METHOD"])
        self.__start = start_response
    @classmethod
    def post(cls,path):
        print(f"Veio no path post: {path}")
        def wrapper(func):
            cls.__routerPost[path] = func
        return wrapper
    @staticmethod
    def other():
        print(f"Veio no path other: ")
        
        def wrapper(func):
            AppClass._AppClass__routerOther = func
        return wrapper
    @classmethod
    def get(cls,path):
        print(f"Veio no path get: {path}")
        def wrapper(func):
            print(func)
            cls.__routerGet[path] = func
            return cls.__routerGet[path]
        return wrapper
    def __call__(self,*param_arg):
        print("Hello World CALL")
        def wrapper(environ,start_response):
            console.log("veio no wrapper")
            console.log(environ,start_response)
        return wrapper
    def get_headers():
        return (headers,status)

    def __iter__(self):
        #print("chama aqui")
        #print(self.__environ["RAW_URI"])
       #method = self.__environ["REQUEST_METHOD"]
        #path = self.__environ["RAW_URI"]
        #print(len(self.__routerPost))
        response = ""
        response_headers = ""
        for p,f in self.__routerPost.items():
            pass
            #print(p)
        match self.__header['method']:
            case "GET":
                if(self.__header['path']  in self.__routerGet):
                    response_headers, response= self.__routerGet[self.__header["path"]](self.__header,self.__res)
                    #response_headers = ('200 OK',[('Content-type','text/html')]) 
                elif self.__header['path'] == '/favicon.ico':
                    response_headers = ('204 No Content',[('Content-type','text/html')])
                    response = ''
                elif self.__routerOther!=None:
                    print("routerOther existe")
                    response_headers,response = self.__routerOther(self.__header,self.__res)
                else:
                    print("routerOther é None")
                    response_headers = ('404 Not Found',[('Content-type','text/html')])
                    response = '<h1>Error</h1>'
            case "POST":
                #print(self.__routerPost)
                if(self.__header["path"] in self.__routerPost):

                    response_headers,response = self.__routerPost[self.__header["path"]](self.__header,self.__res)
                else:
                    response_headers = ('404 Not Found',[('Content-type','plain/text')])
                    response = 'Erreiiii'
            case _:
                response_headers = ('405 Method Not Allowed',[('Content-type','plain/text')])
                response = "<H3> ERROR </H3>"
        #print(response_headers)
    #print(response)
        #headers.append(('version','HTTP/1.1'))
        status, headers = response_headers
        if status.startswith('204'):
            headers = [(key, value) for key, value in headers if key != 'Content-Length']
            self.__start(status,headers)
            yield b'' #para status 204, sem conteúdo
        else:
            print("aqui tambem")
            if isinstance(response, str):
                chunck = response.encode('utf-8')
                contentLength = str(len(response.encode('utf-8')))
            else:
                chunck = response
                contentLength = str(len(response))
            headers.append(('Content-Length',contentLength)) 
            
            self.__start(status,headers)
            #print("retornando")
            yield chunck

#class StandaloneApplication(gunicorn.app.base.BaseApplication):
#
#    def __init__(self, app, options=None,rodar=None,exit=None):
#        self.options = options or {}
#        self.application = app
#        self.exit = exit
#        rodar()
#        super().__init__()
#
#    def load_config(self):
#        config = {key: value for key, value in self.options.items()
#                  if key in self.cfg.settings and value is not None}
#        for key, value in config.items():
#            self.cfg.set(key.lower(), value)
#
#    def load(self):
#        return self.application
#    def on_exit(self,server):
#        print("foi chamado no FIM")
#        self.exit()
#    def run(self):
#        print("NO RUN ELE VEM")
#        try:
#            super().run()
#        finally:
#            self.on_exit(None)
