import threading,types
class SocketClient():
    def __init__(self,con,client):
        self._con= con
        self._id = id(con)
        self._client = client
        self._timeout = 0
        self._retryTimes = 0
        self._connected = True
        self.me = dict()
        self.room = "global"
        self._socketClient = None
        self._emitter = None
        self._emitterAsync = None
        self._on = None
        self._findAction = None
        self._buscarSession = None
        self._car = None 
        self._conectado = None
        self._disconnect = None
        self._join = None
        self._leave = None
        self.actions = {}
        self._act = None
        #threading.Thread.__init__(self)
        #self.name = name

    #def run(self):
        # Defina o comportamento da thread quando ela for iniciada
        #print(f"Thread {self.name} está executando")
    def add_action(self,actionName,method):
        print("adicionando o action")
        self.actions[actionName]=types.MethodType(method,self)
        #self.actions.append(types.MethodType(action,self))
    def set_on_method(self,method):
        print(f"nome do method {method.__name__}")
        if method.__name__=="on":
            #self._on = method
            self._on = types.MethodType(method,self)
        elif method.__name__=="join":
            self.join = types.MethodType(method,self)
        elif method.__name__=="leave":
            self.leave = types.MethodType(method,self)
        elif method.__name__=="emitter":
            self.emitter= types.MethodType(method,self)
        elif method.__name__=="emitterAsync":
            self.emitterAsync= types.MethodType(method,self)
        elif method.__name__=="findAction":
            self._findAction= types.MethodType(method,self)
            #self._findAction = method
        elif method.__name__=="buscarSession":
            #self._buscarSession = method
            self._buscarSession= types.MethodType(method,self)
        elif method.__name__=="conectado":
            #self._conectado = method
            self._conectado = types.MethodType(method,self)
        elif method.__name__=="disconnect":
            print("setou o disconnect")
            self._disconnect = types.MethodType(method,self)
        else:
            self._act = types.MethodType(method,self)
    def findAction(self,action):
        self._findAction(action)
    def buscarSession(self,login,senha):
        self._buscarSession(login,senha)
    def on(self,actionName,callback):
        self._on(actionName,callback)
    #def conectado(self,con,client):
    #    self._conectado(con,client)
    def emitter(self,action,data):
        self._emitter(action,data)
    def join(self,room):
        self._join(room)
    def leave(self):
        self._leave()
    def conectado(self):
        C = threading.Thread(target=self._conectado,)
        C.start()
    def disconnect(self):
        print("TA VINDO NO DICONNECT")
        try:
            self._disconnect()
        except Exception as e:
            print(e)
        print("Mas o _disconnect nunca eh chamado")
 
        #self._conectado(con,client)
