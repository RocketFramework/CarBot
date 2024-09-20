import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QFrame, QLabel, QVBoxLayout, QWidget, QTextBrowser
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
import Artificial_Intelligence
from Artificial_Intelligence import Greeting



class Chat_Box(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("ExploreBGT - 40X")
        self.setGeometry(100, 100, 500, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QVBoxLayout(self.centralWidget)

        self.message_display = QTextBrowser(self)
        self.layout.addWidget(self.message_display)

        self.message_display.setStyleSheet("background-color: #e1f3fc; color: #000000; border: 1px solid #000080; border-radius: 20px; padding: 10px;")
        
        self.Back_Text = QLineEdit(self)
        self.layout.addWidget(self.Back_Text)
        self.Back_Text.setPlaceholderText(" Message ExploreBGT")
        self.Back_Text.setStyleSheet("QLineEdit { border: 1px solid #dedede; border-radius: 20px; padding: 10px; }")

        self.horizontal_line = QFrame(self)
        self.layout.addWidget(self.horizontal_line)
        self.horizontal_line.setFrameShape(QFrame.HLine)
        self.horizontal_line.setStyleSheet("QFrame { background-color: #000000; border: 1px solid #000000; }")


        self.time_label = QLabel(self)
        self.layout.addWidget(self.time_label)
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        

        self.date_label = QLabel(self)
        self.layout.addWidget(self.date_label)
        self.date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


        self.timer = QTimer(self)
        self.timer.timeout.connect(self.Update_Date_And_Time)
        self.timer.start(1000)


        self.adjust_position()
        self.Back_Text.returnPressed.connect(self.Action_Text)


        self.user_messages = []

    
    def adjust_position(self):
        width, height = self.width(), self.height()
        text_width, text_height = self.Back_Text.width(), self.Back_Text.height()
        x = width - text_width - 20
        y = 40
        
        self.Back_Text.setGeometry(x, y, text_width, text_height)


    def resizeEvent(self, event):
        if event.size().width() > 700 or event.size().height() > 600:
            self.setFixedSize(500, 600)
            print("Unable to expand beyond 600x700")
            
        else:
            super().resizeEvent(event)


        self.time_label.move(self.width() - 200, 10)
        self.date_label.move(self.width() - 200, 30)
        self.message_display.setGeometry(0, 60, self.width(), self.height() - 100)
        self.horizontal_line.setGeometry(0, 50, self.width(), 2)
        self.adjust_position()


    def showEvent(self, event):
        self.adjust_position()
        self.time_label.move(self.width() - 200, 10)
        self.date_label.move(self.width() - 200, 30)
        super().showEvent(event)


    def Action_Text(self):
        user_text = self.Back_Text.text()
        self.user_messages.append(user_text)
        self.update_display(user_text)
        self.Back_Text.clear()
        self.Output_Text(user_text, Greeting)
        
        return user_text


    def update_display(self, user_text):
        user_text = user_text.lower()
        
        
        self.message_display.clear()
        for message in self.user_messages:
            answer = Artificial_Intelligence.Intelligent_Output(user_text)
            self.message_display.append(f"<div style=''>You: {message}</div>")
            self.message_display.append(f"<div style=''>ExploreBGT: {answer}</div>")
            self.message_display.append(f"<div style=''> </div>")
           
            
            
    def Output_Text(self, message, Greeting):
        
        words = message.split()
        for i, word in enumerate(words, 1):
            print(f"word{i} = {word}")
        print(f"Total Sentence = {message}")
        print(f"Output Given = {Greeting}")
        print()


    def Update_Date_And_Time(self):
        current_time = QTime.currentTime()
        display_time = current_time.toString("hh:mm:ss AP")
        self.time_label.setText(display_time)

        current_date = QDate.currentDate()
        display_date = current_date.toString(Qt.DefaultLocaleLongDate)
        self.date_label.setText(display_date)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Chat_Box()
    window.show()
    sys.exit(app.exec_())
