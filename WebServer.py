from aiohttp import web
import socketio
import asyncio

#from pynput.keyboard import Key, Listener

import keyboard
import threading

def start():
	recorded = []
	def print_pressed_keys(e):
		if e.event_type == "down":
			if e.scan_code in recorded:
				return
			else:
				recorded.append(e.scan_code)
				packet = {'scan_code':e.scan_code,'value':e.name}
				asyncio.run(print_message("press",packet))
		else:
			if e.scan_code in recorded:
				del recorded[recorded.index(e.scan_code)]
			asyncio.run(print_message("release",str(e.scan_code)))

	def keyboardWatcher():
		keyboard.hook(print_pressed_keys)
		keyboard.wait()

	watcherThread = threading.Thread(target=keyboardWatcher)
	watcherThread.start()




	sio = socketio.AsyncServer()
	app = web.Application()
	sio.attach(app)

	async def index(request):
		fileName = request.path
		print(request.path)
		if fileName == "/":
			fileName = "/index.html"
		contentType = ""
		if ".html" in fileName:
			contentType = 'text/html'
		if ".css" in fileName:
			contentType = 'text/css'
		if ".json" in fileName:
			contentType = 'application/json'

		with open('.'+fileName) as f:
			return web.Response(text=f.read(), content_type=contentType)

	app.router.add_get('/', index)
	app.router.add_get('/generateKeyboard.html', index)
	app.router.add_get('/keyboard.json', index)
	app.router.add_get('/keyboardFull.json', index)
	app.router.add_get('/style.css', index)

	async def print_message(messageType, message):
		task = asyncio.create_task(
			sio.emit(messageType, message))
		await task
		


	@sio.on('message')
	async def received_message(sid, message):
		#This is always sending and receiving because there is some issue where the key presses get frozen and htis allows me to push them through
		await sio.emit('message', message[::-1])

	#def on_press(key):
	#	asyncio.run(print_message("press",str(key)))
		
	#def on_release(key):
	#	asyncio.run(print_message("release",str(key)))

	#listener = Listener(
	#	on_press=on_press,
	#	on_release=on_release)
	#listener.start()

	web.run_app(app)
start()
