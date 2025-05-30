#from .webSocketRouter import SocketRouter
from .app import AppClass as router
from .newServer import Server
import asyncio

def connect(socket=None,msg=None):
    print("connect")
def disconnect(socket):
    print("disconnect")
#socketRouter = SocketRouter(connect,disconnect)
async def main(IP,PORT,io,callback):
    print("Main()")
    global socketRouter
    server = Server(IP,PORT,router,io)
    server_task = asyncio.to_thread(server.run)
    #server_update = asyncio.to_thread(callback)
    #await asyncio.gather(callback)
    #socketRouter = SocketRouter(callback,disconnect)
    taskCallback = asyncio.create_task(callback())
    await asyncio.gather(server_task)
    await taskCallback
     
async def start(ip="0.0.0.0",port=8080,io=None,callback=None):
    
#if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        print("não tem loop rodando")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    if not loop.is_running():
        try:
            loop.run_until_complete(main(ip,port,io,callback))
        except KeyboardInterrupt:
            print("Loop interrompido pelo usuário")
        except Exception as e:
            print(f"Erro ao tentar rodar o loop: {e}")
    else:
        print("Loop de eventos já está rodando, criando tarefa.")
        #await main(ip,port,callback)
        task = loop.create_task(main(ip,port,io,callback))
        await task
