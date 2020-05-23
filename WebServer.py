from aiohttp import web
import socketio
import asyncio

from pynput.keyboard import Key, Listener
import threading



# creates a new Async Socket IO Server
sio = socketio.AsyncServer()
# Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
# instance
sio.attach(app)

async def index(request):
    with open('./index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

app.router.add_get('/', index)




async def print_message(messageType, message):
    #print("Socket ID: " , sid)
    #print(message)
    # await a successful emit of our reversed message
    # back to the clientddddddddd
    task = asyncio.create_task(
        sio.emit(messageType, message))
    await task
    


@sio.on('message')
async def received_message(sid, message):
    print("Socket ID: " , sid)
    print(message)
    # await a successful emit of our reversed message
    # back to the client
    await sio.emit('message', message[::-1])

def on_press(key):
    asyncio.run(print_message("press",str(key)))
    
def on_release(key):
    asyncio.run(print_message("release",str(key)))


#def keyReader(name):
#    print("in thread")
#    with Listener(on_press=on_press) as listener:
#        listener.join()
#    with Listener(on_press=on_press) as listener:
#        listener.join()
listener = Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

#keyReaderThread = threading.Thread(target=keyReader, args=(1,))
#keyReaderThread.start()










# We kick off our server
if __name__ == '__main__':
    web.run_app(app)
