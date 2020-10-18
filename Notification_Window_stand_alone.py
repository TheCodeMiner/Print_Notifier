


import sys
import json
import time


from PySide2.QtWidgets import (
	QApplication, QWidget, QLabel,QVBoxLayout, QDialog
	)
from PySide2.QtCore import (
	Qt, QTimer, QRect, QPropertyAnimation, QSize, Property
	)
from PySide2.QtGui import (
	QPalette, QGuiApplication, QColor
	)

class NotificationWindow(QDialog):
	""" the notification window as QDialog """
	def __init__(self):
		super().__init__()
		# make window to stay on top of all windows + make the window framesless to set translucent available
		self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
		#self.setAttribute(Qt.WA_TranslucentBackground, True) # or set stylesheet with "background:transparent"
		#self.setAttribute(Qt.WA_DeleteOnClose)

		self.message_gruss = ""
		self.message_farbdruck_de = ""
		self.message_farbdruck_en = ""
		self.message_check_de = ""
		self.message_check_en = ""
		self.message_last_de = ""
		self.font_size = 12
		self.animation = None
		self.open_messages_file()


		global_layout = QVBoxLayout()

		#>>> labels
		self.label_gruss = QLabel(self.message_gruss)
		self.label_gruss.setObjectName("gruss")
		self.label_farbdruck_de = QLabel(self.message_farbdruck_de)
		self.label_farbdruck_de.setObjectName("farbdruck")
		self.label_farbdruck_en = QLabel(self.message_farbdruck_en)
		self.label_farbdruck_en.setObjectName("color")
		self.label_check_de = QLabel(self.message_check_de)
		self.label_check_de.setObjectName("check_de")
		self.label_check_en = QLabel(self.message_check_en)
		self.label_check_en.setObjectName("check_en")
		self.label_last_de = QLabel(self.message_last_de)
		self.label_last_de.setObjectName("last")

		for widget in self.label_gruss, self.label_farbdruck_de, self.label_farbdruck_en, self.label_check_de, self.label_check_en, self.label_last_de:
			widget.setWordWrap(True)
			
		#>>> layout managment	
		global_layout.addWidget(self.label_gruss)
		global_layout.addWidget(self.label_farbdruck_de)
		global_layout.addWidget(self.label_farbdruck_en)
		global_layout.addWidget(self.label_check_de)
		global_layout.addWidget(self.label_check_en)
		global_layout.addWidget(self.label_last_de)

		#>>> style
		# background
		font = self.label_farbdruck_de.font()
		font.setPointSize(self.font_size)

		self.label_farbdruck_de.setFont(font)
		self.label_check_de.setFont(font)
		font.setPointSize((self.font_size)*1.3)
		self.label_gruss.setFont(font)
		font.setPointSize((self.font_size)*0.8)
		self.label_last_de.setFont(font)
		self.label_farbdruck_en.setFont(font)
		self.label_check_en.setFont(font)

		style = "QDialog{margin: 6 px}"
		style += "QDialog{background-color: qlineargradient(x1:0 y1:0, x2:0 y2:1, stop:1 rgb(20,104,150), stop:0 rgb(24,156,195))}"
		style += "QDialog{padding: 50px}"
		#style += "QDialog{border: 4px solid rgb(226,0,122); border-top-left-radius:4px; border-bottom-left-radius:4px}"

		style += "QLabel{margin-left:16px}"
		style += "QLabel{color:rgb(255,237,0) ; font-family:Helvetica}"

		style += "QLabel#gruss{qproperty-alignment:AlignVCenter}"
		style += "QLabel#farbdruck, QLabel#check_de, QLabel#last{ border-top: 1px solid qlineargradient(x1:0 y1:0, x2:1 y2:0, stop:0 rgb(25,155,195), stop:0.05 rgb(255,237,0), stop:1 rgb(25,155,195)); qproperty-alignment:AlignBottom AlignLeft ; padding-top: 25}"
		style += "QLabel#color, QLabel#check_en{qproperty-alignment:AlignTop AlignLeft; color: lightgray}"
		style += "QLabel#last{qproperty-alignment:AlignLeft AlignBottom}"

		self.setStyleSheet(style)

		self.setLayout(global_layout)
		self.do_animation()



	def getBackColor(self):
		return self.palette().color(QPalette.Window)

	def setBackColor(self, color):
		pal = self.palette()
		pal.setColor(QPalette.Window, color)
		self.setPalette(pal)

	backcolor = Property(QColor, getBackColor, setBackColor)   # ;) keep its indent like this


	def do_animation(self):
		""" defining the position of the window on the screen """

		self.animation = QPropertyAnimation(self, b"geometry")
		self.animation.setDuration(180)

		screen_size = QGuiApplication.primaryScreen().availableGeometry()
		screen_width = screen_size.width()
		screen_height = screen_size.height()
		window_width = screen_width /3
		window_height = screen_height /3
		w_position_left = screen_width * 0.67    # x
		w_position_top = screen_height * 0.33    # y

		self.animation.setStartValue(QRect(screen_width, w_position_top, window_width, window_height))
		self.animation.setEndValue(QRect(w_position_left, w_position_top, window_width, window_height))
		self.show()
		self.animation.start()
		self.blink_animation_run()

	def blink_animation_run(self):
		self.blink_animation = QPropertyAnimation(self, b"backcolor")
		self.blink_animation.setStartValue(QColor(226,0,122))
		self.blink_animation.setKeyValueAt(0.5, QColor(255,237,0))
		self.blink_animation.setEndValue(QColor(226,0,122))
		self.blink_animation.setDuration(700)
		self.blink_animation.setLoopCount(4)
		self.blink_animation.start()


	def open_messages_file(self):
		try:
			with open("messages.json", encoding='UTF-8') as f:
				content = json.load(f)
				print(content)
				self.message_gruss = content[0] 
				self.message_farbdruck_de = content[1]   
				self.message_farbdruck_en = content[2]
				self.message_check_de = content[3]
				self.message_check_en = content[4]
				self.message_last_de = content[5]
				self.font_size = content[6]

		except Exception:
			pass


app = QApplication(sys.argv)
w = NotificationWindow()
w.show()
app.exec_()

