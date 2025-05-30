import asyncio
import queue,traceback
from .socketClient import SocketClient
import json
from .room import Room
queue_message = queue.Queue()

#import socket
#from websockets.asyncio.server import serve
#from geventwebsocket.websocket import WebSocket  # Importação corrigida



class SocketRouter:
    __start_server = None
    session = dict()
    _rooms = dict()
    _rooms["global"] = Room("global")
    def __init__(self,connect,disconnect):
        self.__ip =  None
        self.__port = None
        self.connect = connect
        #self.disconnect = disconnect
    async def run(self):
        pass

    async def emitterAsync(self,self_instance,path,msg):
        fullMsg = {"on":path,"msg":msg}
        data = json.dumps(fullMsg)
        try:
            print(self_instance._con)
            print(data)
            print(type(self_instance._con))
            if self_instance._con is not None:
                await self_instance._con.send(data)
        except Exception as e:
            print(e)
            await self_instance._con.close()
    def pushDataToRoom(self_instance,path,data):
        print(path)
        self_instance._rooms[path].push(data)

    async def roomBroadcast(self_instance):
       for key in self_instance._rooms:
            try:
                #print("loucura de key é essa?")
                print(key)
                #print("que key estranha é essa?")
                room = self_instance._rooms[key]
                #print(room)
                room.broadcast()
            except Exception as e:
                print("veio no erro")
                print(e)

    async def broadcaster(self_instance,path,msg):
        print("broadcaster")
        print(self_instance._rooms)
        fullMsg = {"on":path,"msg":msg}
        data = json.dumps(fullMsg)
        try:
            for key in list(self_instance.session):
                socket = self_instance.session[key]
                try:
                    socket._con.send(data)
                    print("mensagem enviada")
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    print("Cliente desconectado.")
                    try:
                        socket.disconnect()
                    except Exception as e:
                        print(e)
                        traceback.print_exc()

        except Exception as e:
            print("veio no erro maximo")
            traceback.print_exc()
            print(e)
    def emitter(self,self_instance,path,msg):
        fullMsg = {"on":path,"msg":msg}
        data = json.dumps(fullMsg)
        try:
            self_instance._con.send(data)
        except Exception as e:
            print(f"no emmiter: {e}")
            self_instance._con.close()
            del self.session[self_instance._id]
            #self_instance.disconnect()
            #raise Exception("Usuário desconectou")
            
    def conectado(self,webSocket):
        try:
            #print("Veio no Conectado")
            socket = SocketClient(webSocket,"/")
            socket.set_on_method(self.on)
            socket.set_on_method(self.emitter)
            socket.set_on_method(self.emitterAsync)
            socket.set_on_method(self.findAction)
            socket.set_on_method(self.conectado)
            socket.set_on_method(self.leave)
            socket.set_on_method(self.join)
            socket.set_on_method(self.disconnect)
            #print(webSocket)
            #print(path)
            
            self._rooms["global"].join(socket)
            self.connect(socket=socket)
            self.session[socket._id]=socket
            running = True
            while running:
                try:
                    msg = webSocket.receive()
                    if msg == None:
                        continue
                    msg = json.loads(msg)
                    action = msg["action"]
                    if(action=="ping"):
                        self.ping(socket)
                        continue
                    fullMsg = msg["msg"]
                    print(action)
                    print(msg)
                    socket.findAction(action)
                    if(socket._act!=None):
                        socket._act(fullMsg)
                    else:
                        print("não achou o act")
                except Exception as e:
                    print(f"no conectado: {e}")
                    print(e)
                    traceback.print_exc()
                    running=False
                    webSocket.close()
               # finally:
               #     webSocket.close()
               #     running=False
            #await socket.conectado()
        except Exception as e:
            print(e)
            traceback.print_exc()
    def findAction(self,self_instance,act):
        print("findAction")
        try:
            if act:
                self_instance._act = self_instance.actions[act]
        except Exception as e:
            print(e)
        return
           # for row in self_instance.actions:
           #     if(row.__name__==act):
           #         self_instance._act = row
           #         return
    def on(self,self_instance=None,actionName="on",callback=None):
#        for a in self_instance.actions:
#            if(a.__name__==actionName):
#                return False
#        self_instance.actions.append(actionName)
#        print("adicionado no on")
        self_instance.add_action(actionName,callback)

    def disconnect(self,self_instance):
        print("disconnect socket")
        print(self)
        print(self_instance)
        try:
            del self.session[self_instance._id]
        except Exception as error:
            print("erro ao deletar o self.session")
            print(str(error))
            traceback.print_exc()
    def ping(self,socket):
        socket.emitter("ping","")

    def getRoom(self,room):
        if room in self._rooms:
            return self._rooms[room]
        else:
            return self.newRoom(room)
    def newRoom(self,roomName):
        room = Room(roomName)
        self._rooms[roomName] = room
        return room

    def join(self,self_instance,room):
        print(self,self_instance)
        self._rooms[self_instance.room].leave(self_instance)
        if room not in self._rooms:
            self._rooms[room] = Room(room)
        self._rooms[room].join(self_instance)
        self_instance.room = room
    def leave(self,self_instance):
        self._rooms[self_instance.room].leave(self_instance)
        self._rooms["global"].join(self_instance)
        self.self_instance.room = "global"
    def close(self):
        self.running=False
        #for socket in self.session:
            #socket.disconnect()
            #socket.close()
        #self.__start_server.close()

#socketRouter = SocketRouter()
