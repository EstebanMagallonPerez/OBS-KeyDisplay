from aiohttp import web
import socketio
import asyncio
import keyboard
import threading
import os

def start():
	sio = socketio.AsyncServer()
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

	async def index(request):
		fileName = request.path
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

	async def print_message(messageType, message):
		task = asyncio.create_task(
			sio.emit(messageType, message))
		await task

	@sio.on('message')
	async def received_message(sid, message):
		await sio.emit('message', message[::-1])

	watcherThread = threading.Thread(target=keyboardWatcher)
	watcherThread.start()

	app = web.Application()
	sio.attach(app)

	app.router.add_get('/', index)
	app.router.add_get('/generateKeyboard.html', index)
	for file in os.listdir("./"):
		if file.endswith(".json"):
			app.router.add_get('/'+file, index)
	web.run_app(app)
start()
