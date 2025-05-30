import json
class Room:
    def __init__(self,roomName):
        self.roomName = roomName
        self.sockets = {}
        self.blocked = False
        self.typing_timeout = None
        self.dataSet = dict()
        self.data = []
        self.dataTemp = []
        self.version = 0
        self.owner = None
        self.lastChanges = list()
        self.socketsFullText = list() #usuarios que pediram o texto na ultima versao
    def sendToThen(self,socketMe,path,msg):

        print("sendToRoom")
        if(len(msg)==0):
            print("Não há dados a serem enviados")
            return False
        print(msg)
        fullMsg = {"on":path,"msg":msg}

        print(fullMsg)
        try:
            data = json.dumps(fullMsg)
        except Exception as e:
            print("não conseguiu enviar nada por erro no dumps") 
            print(e)
        for key in list(self.sockets):

            socket = self.sockets[key]
            if(socketMe!=socket):
                try:
                    socket._con.send(data)
                except Exception as e:

                    print(e)
                    del self.sockets[key]
    def sendToAll(self,path,data):
        print("veio no sendAll")
        fullMsg = {"on":path,"msg":data}
        try:
            data = json.dumps(fullMsg)
        except Exception as e:
            print("não conseguiu enviar nada por erro no dumps") 
            print(e)
        for key in list(self.sockets):
            socket = self.sockets[key]
            try:
                socket._con.send(data)
            except Exception as e:
                print(e)
                del self.sockets[key]
        
    def broadcast(self):
        print("veio no broadcast")
        if(len(self.data)==0):
            print("Não há dados a serem enviados")
            if(len(self.dataTemp)!=0):
                self.data = self.dataTemp
            else:
                return False
        fullMsg = {"on":self.roomName,"msg":self.data}
        try:
            data = json.dumps(fullMsg)
        except Exception as e:
            print("não conseguiu enviar nada por erro no dumps") 
            print(e)
        for key in self.sockets:
            socket = self.sockets[key]
            try:
                socket._con.send(data)
            except Exception as e:
                print(e)
        self.data = self.dataTemp
        self.dataTemp = []
    def join(self,socket):
        self.sockets[socket._id] = socket
    def leave(self,socket):
        if socket._id in self.sockets:
            del self.sockets[socket._id]
        if socket in self.socketsFullText:
            del self.socketsFullText[socket._id]
    def block(self):
        self.blocked = True
    def unblock(self):
        self.blocked = False
    def push(self,data):
        self.dataTemp.append(data)
