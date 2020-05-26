from aiohttp import web
import socketio
import asyncio
import keyboard
import threading
import os
import pystray
import sys
from PIL import Image, ImageDraw
from pystray import Icon as icon, Menu as menu, MenuItem as item


closeThreads = False
def start():
	sio = socketio.AsyncServer()
	recorded = []

	def on_clicked(icon, item):
		global closeThreads
		closeThreads = True
		icon.stop()

	def makeIcon():
		image = Image.open("key.png") #Battery Status Full
		icon('KeyViewer', image,title="OBS KeyViewer", menu=menu(item('Exit',on_clicked))).run()
		

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
		if closeThreads:
			sys.exit()
		await sio.emit('message', message[::-1])

	app = web.Application()
	sio.attach(app)

	app.router.add_get('/', index)
	app.router.add_get('/generateKeyboard.html', index)
	for file in os.listdir("./keyboards"):
		if file.endswith(".json"):
			app.router.add_get('/keyboards/'+file, index)
	for file in os.listdir("./css"):
		if file.endswith(".css"):
			app.router.add_get('/css/'+file, index)
	for file in os.listdir("./scripts"):
		if file.endswith(".js"):
			app.router.add_get('/scripts/'+file, index)

	watcherThread = threading.Thread(target=keyboardWatcher)
	watcherThread.setDaemon(True)
	watcherThread.start()

	iconThread = threading.Thread(target=makeIcon)
	iconThread.setDaemon(True)
	iconThread.start()

	web.run_app(app)
	sys.exit()

start()
