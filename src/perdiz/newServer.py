from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler


class Server:
    def __init__(self, host='0.0.0.0', port="5000",AppClass=None,socketRouter=None):
        self.host = host
        self.port = port
        self.AppClass = AppClass
        if(socketRouter is not None):
            self.socketRouter = socketRouter
            self.server = WSGIServer((self.host, self.port), self.simple_app, handler_class=WebSocketHandler)
        else:
            self.server = WSGIServer((self.host, self.port), self.simple_app) 
    
    def handle_http(self,environ, start_response):
        """Lógica simples para responder a requisições HTTP."""
        start_response("200 OK", [("Content-Type", "text/plain")])
        return [b"Hello from custom Gevent HTTP server"]
    
    def handle_websocket(self,ws):
        """Lógica simples para lidar com conexões WebSocket."""
        print("vindo aqui no websocket")
        if(self.socketRouter is not None):
            self.socketRouter.conectado(ws)
    
    def simple_app(self,environ, start_response):
        """Mecanismo simples para separar WebSocket de HTTP."""
        if environ["PATH_INFO"] == "/ws":
            ws = environ.get("wsgi.websocket")
            if ws:
                self.handle_websocket(ws)
            return []
        else:
            app_instance = self.AppClass(environ, start_response)
            return app_instance.__iter__()#handle_http(environ, start_response)
    def run(self):
        print(f"Servidor rodando na porta {self.port}...")
        print(f"Servidor rodando no ip: {self.host}...")
        self.server.serve_forever()


#if __name__ == "__main__":
#    server = WSGIServer(('0.0.0.0', 8000), simple_app, handler_class=WebSocketHandler)
#    print("Servidor rodando na porta 8000...")
#    server.serve_forever()

