import logging
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import threading
import keyboard
import asyncio
import sys
from tornado.options import define, options
from PIL import Image, ImageDraw
from pystray import Icon as icon, Menu as menu, MenuItem as item
import requests

define("port", default=8888, help="run on the given port", type=int)

closeThreads =  False
def start():
	releaseList = []
	pressList = []
	
	class Application(tornado.web.Application):
		def __init__(self):
			handlers = [(r"/keyboardSocket", KeyboardSocketHandler),(r".*", MainHandler)]
			super(Application, self).__init__(handlers)


	class MainHandler(tornado.web.RequestHandler):
		def get(self):
			global closeThreads
			if closeThreads:
				sys.exit()
			fileName = self.request.path
			if fileName == "/":
				fileName = "/index.html"
			contentType = ""
			if ".html" in fileName:
				contentType = 'text/html'
			if ".css" in fileName:
				contentType = 'text/css'
			if ".json" in fileName:
				contentType = 'application/json'
			if ".ico" in fileName:
				contentType = "image/x-icon"

			with open('.'+fileName, 'rb') as f:
				self.set_header('Content-Type', contentType)
				self.write(f.read())


	class KeyboardSocketHandler(tornado.websocket.WebSocketHandler):
		waiters = set()
		ws_connection = None
		def open(self):
			KeyboardSocketHandler.waiters.add(self)

		def on_close(self):
			KeyboardSocketHandler.waiters.remove(self)

		@classmethod
		def send_updates(cls, keypress):
			print("we received the send")
			for waiter in cls.waiters:
				try:
					waiter.write_message(keypress)
				except:
					''''''
	recorded = []
	def print_pressed_keys(e):
		if e.event_type == "down":
			if e.scan_code in recorded:
				return
			else:
				recorded.append(e.scan_code)
				packet = {'type':"press",'scan_code':e.scan_code,'value':e.name}
				asyncio.set_event_loop(asyncio.new_event_loop())
				KeyboardSocketHandler.send_updates(packet)
		else:
			if e.scan_code in recorded:
				del recorded[recorded.index(e.scan_code)]
			packet = {'type':"release",'scan_code':e.scan_code,'value':e.name}
			KeyboardSocketHandler.send_updates(packet)

	def keyboardWatcher():
		keyboard.hook(print_pressed_keys)
		keyboard.wait()

	def on_clicked(icon, item):
		global closeThreads
		closeThreads = True
		url = 'http://127.0.0.1:8888/index.html'
		x = requests.get(url)
		icon.stop()

	def makeIcon():
		image = Image.open("key.png") #Battery Status Full
		icon('KeyViewer', image,title="OBS KeyViewer", menu=menu(item('Exit',on_clicked))).run()

	def main():
		watcherThread = threading.Thread(target=keyboardWatcher)
		watcherThread.setDaemon(True)
		watcherThread.start()

		iconThread = threading.Thread(target=makeIcon)
		iconThread.setDaemon(True)
		iconThread.start()

		tornado.options.parse_command_line()
		app = Application()
		app.listen(options.port)
		tornado.ioloop.IOLoop.current().start()
		sys.exit()
	
	main()