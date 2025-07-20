import os,io
from multipart import MultipartParser
from .response import Response

#import gunicorn.app.base
import ssl,secrets,string,json
alphabet = string.ascii_letters + string.digits



#def number_of_workers():
#    return (multiprocessing.cpu_count() * 2) + 1
class AppClass:
    __routerPost = {}
    __routerGet = {}
    __routerOther = None
    __staticsPaths = dict()
    __staticsFiles = dict()
    __staticsPathsUpload = dict()
    __max_size = 128_000 #max size bytes

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
        
        for key,value in environ.items():
            pass
            #print(f"{key}: {value}")
        self.__header = {
            "method":environ["REQUEST_METHOD"],
            "path":environ["PATH_INFO"],
            "body":body,
            "body_length":body_size,
            "content-type":environ.get("CONTENT_TYPE",None)
        }
        print("\n")
        #print(environ["REQUEST_METHOD"])
        self.__start = start_response
    @classmethod
    def setMaxSize(cls,size):
        cls.__max_size = size
    @staticmethod
    def generateId():
        token = ''.join(secrets.choice(alphabet) for i in range(16))
        return token
    def upload_file(self,theFullPath) -> tuple:
        print("/FTP - File upload endpoint hit")
        print(f"the path {theFullPath}");

        try:
            # 1. Validação dos headers
            content_type = self.__header.get("content-type", "")
            content_length = int(self.__header.get("body_length", 0))
            body_raw = self.__header.get("body", b"")
    
            print(f"Debug - Content-Type: {content_type}")
            print(f"Debug - Content-Length: {content_length}")
            print(f"Debug - Body length received: {len(body_raw)} bytes")
    
            # Verificação básica do content-type
            if not content_type.startswith("multipart/form-data"):
                return self.__res.error("Content-Type must be multipart/form-data")
    
            # Extrai o boundary do content-type
            boundary = None
            for part in content_type.split(";"):
                part = part.strip()
                if part.startswith("boundary="):
                    boundary = part[9:]  # Remove 'boundary='
                    # Se o boundary estiver entre aspas
                    if boundary.startswith('"') and boundary.endswith('"'):
                        boundary = boundary[1:-1]
                    break
    
            if not boundary:
                return self.__res.error("Missing boundary in Content-Type")
    
            # Verificação do tamanho do conteúdo
            if len(body_raw) != content_length:
                return self.__res.error(f"Content length mismatch. Expected {content_length}, got {len(body_raw)}")
    
            # 2. Processamento do conteúdo multipart
            try:
                stream = io.BytesIO(body_raw)
                # Garante que o boundary está no formato correto
                boundary = boundary.encode('ascii')
    
                parser = MultipartParser(stream, boundary)
    
                fields = {}
                files = {}
    
                # Lê todas as partes antes de processar
                parts = list(parser)
                if not parts:
                    return self.__res.error("No parts found in multipart data")
    
                for part in parts:
                    if part.filename:
                        # Lê o conteúdo imediatamente (o parser pode fechar o stream)
                        file_content = part.raw.read() if hasattr(part.raw, 'read') else part.raw
                        files[part.name] = {
                            'filename': part.filename,
                            'content': file_content
                        }
                    else:
                        fields[part.name] = part.value
    
            except Exception as e:
                return self.__res.error(f"Multipart parsing failed: {str(e)}")
    
            # 3. Validação do arquivo recebido
            if 'file' not in files:
                return self.__res.error('Missing file in upload')
    
            file_info = files['file']
            filename = file_info['filename']
            file_content = file_info['content']
    
            # 4. Salvamento do arquivo
            try:
                # Previne path traversal
                filename = os.path.basename(filename)
                local_path = os.path.join(theFullPath, filename)
    
                with open(local_path, 'wb') as f:
                    if isinstance(file_content, bytes):
                        f.write(file_content)
                    else:
                        f.write(file_content.read() if hasattr(file_content, 'read') else file_content)
    
                print(f"Debug - File saved successfully: {local_path}")
                return self.__res.text("File uploaded successfully")
    
            except Exception as e:
                return self.__res.error(f"Failed to save file: {str(e)}")
    
        except Exception as e:
            return self.__res.error(f"Unexpected error: {str(e)}")

    def downloadHtml(self):
        # 1. Extração e validação do caminho
        fullPath = self.__header['path'].split("/")
        with open(fullPath[1]) as file:
            pass

    def download_file(self):
        try:
            # 1. Extração e validação do caminho
            fullPath = self.__header['path'].split("/")

            print(fullPath)
            # Verifica se o path tem formato correto: ["", "download", "arquivo.ext"]
            if len(fullPath) < 3:
                return self.__res.error("Invalid path format")
        
            filename = fullPath[2]
            if not filename:  # Verifica se o nome do arquivo não está vazio
                return self.__res.error("Empty filename")
        
            print(f"full path {fullPath}")
            print(f"filename {filename}")
        
            # 2. Validação do diretório base
            base_key = "/" + fullPath[1] +"/"
            if base_key not in self.__staticsPaths:
                return self.__res.error("Invalid resource path")
        
            filepath = os.path.join(self.__staticsPaths[base_key], filename)
            print(f"filepath {filepath}")
        
            # 3. Verificação de segurança do caminho
            # Previne directory traversal (ex: tentativas de acessar ../arquivos)
            resolved_path = os.path.abspath(filepath)
            base_dir = os.path.abspath(self.__staticsPaths[base_key])
            
            if not resolved_path.startswith(base_dir):
                return self.__res.error("Access denied: invalid path")
        
            # 4. Verificação do arquivo
            print(resolved_path)
            if not os.path.exists(resolved_path):
                return self.__res.error("File not found")
        
            if not os.path.isfile(resolved_path):
                return self.__res.error("Path is not a file")
        
            # 5. Determinação do tipo MIME
            _, ext = os.path.splitext(filename)
            ext = ext.lower()
            
            # 6. Leitura do arquivo
            with open(resolved_path, 'rb') as f:
                file_content = f.read()
        
            # 7. Roteamento por extensão
            handlers = {
                '.png': self.__res.png,
                '.jpg': self.__res.jpg,
                '.jpeg': self.__res.jpeg,
                '.gif': self.__res.gif,
                '.html': lambda c: self.__res.html(c.decode('utf-8')),
                '.css': lambda c: self.__res.css(c.decode('utf-8')),
                '.js': lambda c: self.__res.js(c.decode('utf-8'))
            }
        
            handler = handlers.get(ext, lambda c: self.__res.other(c, filename))
            return handler(file_content)

        except PermissionError:
            return self.__res.error("Permission denied")
        except IOError as e:
            return self.__res.error(f"I/O error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return self.__res.error("Internal server error")    
    @classmethod
    def post(cls,path):
        #print(f"Veio no path post: {path}")
        def wrapper(func):
            cls.__routerPost[path] = func
        return wrapper
    @staticmethod
    def other():
        #print(f"Veio no path other: ")
        
        def wrapper(func):
            AppClass._AppClass__routerOther = func
        return wrapper
    @classmethod
    def get(cls,path):
        #print(f"Veio no path get: {path}")
        def wrapper(func):
            cls.__routerGet[path] = func
            return cls.__routerGet[path]
        return wrapper
    @classmethod
    def static(cls,path,fullPath):
        print(f"Veio no path static: {path}")
        cls.__staticsPaths[path] = fullPath
    @classmethod
    def staticFile(cls,path,fullPath):
        print(f"Veio no path staticFile: {path} {fullPath}")
        cls.__staticsFiles[path] = fullPath
        print(cls.__staticsFiles)

    @classmethod
    def staticUpload(cls,path,fullPath):
        print(f"veio no path staticUpload: {path}")
        cls.__staticsPathsUpload[path] = fullPath
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
        
        if(self.__header["body_length"]>self.__max_size):
            response_headers,response = self.__res.tooLarge()
            status, headers = response_headers
            print("mensagem é grande demais e por isso será boqueada")
            print(self.__header["body_length"],self.__max_size)
            self.__start(status,headers)
            yield response
            return

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
                elif any(self.__header['path'].startswith(prefix) for prefix in self.__staticsPaths):
                    print("o endereço é static")
                    try:
                        response_headers, response = self.download_file()
                    except Exception as e:
                        print(e)
                elif any(self.__header['path'].endswith(prefix) for prefix in self.__staticsFiles):
                    print("o endereço é staticFiles")
                    try:
                        response_headers, response = self.download_file()
                    except Exception as e:
                        print(e)
   
                elif self.__routerOther!=None:
                    print("routerOther existe")
                    response_headers,response = self.__routerOther(self.__header,self.__res)
                else:
                    print("routerOther é None")
                    response_headers = ('404 Not Found',[('Content-type','text/html')])
                    response = '<h1>Error</h1>'
            case "POST":
                print(self.__header["path"])
                if(self.__header["path"] in self.__routerPost):

                    response_headers,response = self.__routerPost[self.__header["path"]](self.__header,self.__res)
                elif any(self.__header['path'].startswith(prefix) for prefix in self.__staticsPathsUpload):
                    print("o endereço é static no upload")
                    matched_prefix = next(
                        (prefix for prefix in self.__staticsPathsUpload 
                         if self.__header['path'].startswith(prefix)),
                        None
                    )
                    if matched_prefix:
                        try:
                            response_headers, response = self.upload_file(self.__staticsPathsUpload[matched_prefix])  # Passa o prefix como argumento
                        except Exception as e:
                            print(e)
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
