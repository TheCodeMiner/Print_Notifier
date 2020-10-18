

import win32process
import wmi
import ctypes
import ctypes.wintypes
import time

from PySide2.QtWidgets import (
	QApplication
	)
	
from PySide2.QtCore import (
	Qt, QTimer, QRunnable, QObject, Signal, 	# worker
	)

import sys

class Thread_Worker (QRunnable):
	""" handles windows process current app running focused """
	def __init__(self):
		super().__init__()
		self.signals = WorkerSignals()
		self.name = ""
		self.loop = True
		
	#@Slot()
	def run(self):
		try:
			self.c = wmi.WMI()
			self.name = ""
			while self.loop:
				self.name = self.all_apps_running()
				
				self.signals.result.emit(self.name)
				self.signals.finished.emit()
				time.sleep(0.7)  # to lower cpu usage 

		except Exception as e:
			pass   # when closing we will get error, but it will stop program anyway


	def all_apps_running(self):
		""" looks throgh wind32processes to find all Foreground running apps """
		try:
			hwnd = ctypes.windll.user32.GetForegroundWindow()
			_, pid = win32process.GetWindowThreadProcessId(hwnd)
			exe = ""
			for p in self.c.query('SELECT Name FROM Win32_Process WHERE ProcessId = %s' % str(pid)):
				exe = p.Name
				print("Foreground app name: ",exe)
				break
		except:
			return None
		else:
			return exe


class WorkerSignals(QObject):
	""" custom signals of Thread_Worker """
	finished = Signal()
	error = Signal(str)
	result = Signal(str)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	thread = Thread_Worker()
	thread.run()
	app.exec_()

			