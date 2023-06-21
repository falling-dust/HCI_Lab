# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'asrInterface.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
import speech_recognition as sr
import win32api


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(314, 462)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);background-image: url('img/R-C.png');")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # gif动画
        self.voiceFig = QtWidgets.QLabel(self.centralwidget)
        self.voiceFig.setGeometry(QtCore.QRect(80, 50, 161, 121))
        self.voiceFig.setText("")
        self.gif = QMovie("icon/new-voice.gif")
        self.voiceFig.setMovie(self.gif)
        self.gif.start()
        self.voiceFig.setScaledContents(True)
        self.voiceFig.setObjectName("voiceFig")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # InteractiveText格式设定
        self.InteractiveText = QtWidgets.QTextEdit(MainWindow)
        self.InteractiveText.setGeometry(QtCore.QRect(60, 200, 200, 60))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.InteractiveText.setFont(font)
        self.InteractiveText.setStyleSheet("color: rgb(0, 117, 210);border: 0px ;border-radius: 8px;")

        self.InteractiveText.setReadOnly(True)
        self.InteractiveText.setObjectName("label")

        # 设置提示文本
        self.TipsText = QtWidgets.QTextEdit(MainWindow)
        self.TipsText.setGeometry(50, 360, 220, 80)
        self.TipsText.setReadOnly(True)
        self.TipsText.setStyleSheet("color: rgb(0, 117, 210);border: 0px ;font-size: 15px;border-radius: 8px;")
        self.TipsText.setFont(font)

        # 设置启动按钮
        self.button = QtWidgets.QPushButton('', MainWindow)
        self.button.setGeometry(135, 270, 50, 30)
        self.button.setObjectName('btn')
        self.button.setIcon(QtGui.QIcon('icon/phone'))
        self.button.setStyleSheet("border: 0px ;border-radius: 8px;")
        self.button.clicked.connect(self.recognize_speech_from_mic)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Voice Assistant"))
        tips_text = "Tips: You can click the button and do: 1. Enjoy music by saying \"Play music\" 2. Take some notes by saying \"Open Notepad\""
        self.InteractiveText.setText(_translate("MainWindow", "Please speak something."))
        self.TipsText.setText(tips_text)

    def recognize_speech_from_mic(self):
        self.InteractiveText.setText("Please speak something.")
        # 创建识别器和麦克风实例
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        print("调用成功")
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")

        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # adjust the recognizer sensitivity to ambient noise and record audio
        # from the microphone
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            print("尝试识别")
            try:
                # 可以选用以下两种方式的一种
                # 采用谷歌的API（需要科学上网，准确率更高）
                text = recognizer.recognize_google(audio, language='en-US')
                # 采用离线包（准确率太低了）
                # text = recognizer.recognize_sphinx(audio)

                # 显示输入的语音转化成的文字
                self.InteractiveText.setText("Text:" + text)
                print(text)

                if 'open notepad' in text or 'notepad' in text or 'open Notepad' in text:
                    self.open_notepad()
                elif 'play music' in text or 'music' or 'play' in text:
                    self.play_music()

            except sr.UnknownValueError:
                self.InteractiveText.setText('Unable to recognize speech.')
            except sr.RequestError as e:
                self.InteractiveText.setText('API unavailable')

    def play_music(self):
        print("Play music!!!")
        win32api.ShellExecute(0, 'open', 'E:\\project\\python_project\\lab1-asr\\music.mp3', '', '', 1)

    def open_notepad(self):
        print("Use notepad!!!")
        win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 1)
