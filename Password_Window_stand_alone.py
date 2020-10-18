""" it'll return true(correct pw entered) or nothing(pw incorrect) """


import sys

from PySide2.QtWidgets import (
	QApplication, QDialog, QVBoxLayout, QLabel, QWidget,
	QPushButton, QLineEdit, QMainWindow, QStackedLayout,
	QGroupBox, QHBoxLayout, QSizePolicy
	)
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QGuiApplication, QKeySequence

class PasswordWindow(QDialog):
	def __init__(self):
		super().__init__()
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.set_window_position_on_screen()


		self.close_button = QPushButton("x")
		self.close_button.setObjectName("close")
		self.close_button.setFixedSize(30,30)
		self.close_button.pressed.connect(self.window_closed)

		self.pw_label = QLabel("Enter admin password")
		self.pw_label.setObjectName("label")

		self.pw_line = QLineEdit()
		self.pw_line.setObjectName("line")
		self.pw_line.setEchoMode(QLineEdit.Password)

		self.pw_button = QPushButton("Enter")
		self.pw_button.setObjectName("btn")
		self.pw_button.setFixedSize(120,30)
		self.pw_button.setShortcut(QKeySequence(Qt.Key_Return))
		self.pw_button.clicked.connect(self.password_check)

		spacer = QWidget()
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

		#-------------- layout management ------------
		global_layout = QVBoxLayout()
		h_layout = QHBoxLayout()
		h_layout_bottom = QHBoxLayout()
		h_layout.addWidget(spacer)
		h_layout.addWidget(self.close_button)
		global_layout.addLayout(h_layout)
		global_layout.addWidget(self.pw_label)
		global_layout.addWidget(self.pw_line)
		h_layout_bottom.addWidget(spacer)
		h_layout_bottom.addWidget(self.pw_button)
		h_layout_bottom.addWidget(spacer)
		global_layout.addLayout(h_layout_bottom)
		#=============================================

		#------------------- style -------------------
		style = "QDialog{border: 1px solid black}"
		style += "QLabel#label{margin-left:20px; font-size:15px; qproperty-alignment:AlignBottom}"
		style += "QLineEdit#line{margin-left:20px; margin-right:20px; qproperty-alignment:AlignBottom}"

		self.setStyleSheet(style)
		#============================================

		self.setLayout(global_layout)
		self.pw_line.setFocus()


	def password_check(self):
		text = self.pw_line.text()
		pw = "password"   # accepted pw
		if text == pw:
			self.accept()


	def window_closed(self):
		self.reject()

	def set_window_position_on_screen(self):
		screen_size = QGuiApplication.primaryScreen().availableGeometry()
		screen_width = screen_size.width()
		screen_height = screen_size.height()
		window_width = screen_width /5
		window_height = screen_height /5
		w_position_left = (screen_width * 0.80)-100    # x
		w_position_top = screen_height * 0.80    # y

		self.setGeometry(w_position_left, w_position_top, window_width, window_height)
		


class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setFixedSize(400,400)



app = QApplication(sys.argv)

pw_window = PasswordWindow()
w = MainWindow()
value = None
if pw_window.exec_() == QDialog.Accepted:
	w.show()
	value = True
print(value)

app.exec_()

