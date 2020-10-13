import sys
import random
from enum import IntEnum
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtGui import *
from PyQt5.QtCore import *

step = 0

class WinForm(QMainWindow):
    def __init__(self, parent=None):
        super(WinForm, self).__init__(parent)
        #layout = QVBoxLayout()
        self.resize(600, 600)
        self.setWindowTitle('图片华容道')

        palette1 = QPalette()
        palette1.setColor(self.backgroundRole(), QColor(192, 253, 123))
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('background4.jpg')))
        self.setPalette(palette1)

        self.label = QLabel(self)
        self.label.setGeometry(170, 0, 400, 200)
        self.label.setText("图片华容道")
        self.setStyleSheet("QLabel{color:rgb(0,205,205,255);font-size:50px;font-weight:bold;font-family:Arial;}")
        self.button1 = QPushButton('开始游戏φ(≧ω≦*)♪', self)
        self.button1.setGeometry(220, 150, 150, 100)
        self.button1.setStyleSheet("QPushButton{color:black}"
                                  "QPushButton:hover{color:red}"
                                  "QPushButton{background-color:rgb(78,255,255)}"
                                  "QPushButton{border:2px}"
                                  "QPushButton{border-radius:10px}"
                                  "QPushButton{padding:2px 4px}")
        #self.button1.setStyleSheet(
            #'''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')

        #self.button1.move(100, 100)
        self.button1.clicked.connect(self.onButtonClick)
        #layout.addWidget(self.button1)

        self.button2 = QPushButton('历史得分(^з^)-☆', self)
        self.button2.setGeometry(220, 300, 150, 100)
        self.button2.setStyleSheet("QPushButton{color:black}"
                                  "QPushButton:hover{color:red}"
                                  "QPushButton{background-color:rgb(78,255,255)}"
                                  "QPushButton{border:2px}"
                                  "QPushButton{border-radius:10px}"
                                  "QPushButton{padding:2px 4px}")
        self.button2.clicked.connect(self.onButtonClick2)
        #layout.addWidget(self.button2)

        # main_frame = QWidget()
        # main_frame.setLayout(layout)
        # self.setCentralWidget(main_frame)
        self.button4 = QPushButton('按下按钮\n离开软工实践o(╥﹏╥)o', self)
        self.button4.setGeometry(220, 450, 150, 100)
        self.button4.setStyleSheet("QPushButton{color:black}"
                                   "QPushButton:hover{color:red}"
                                   "QPushButton{background-color:rgb(78,255,255)}"
                                   "QPushButton{border:2px}"
                                   "QPushButton{border-radius:10px}"
                                   "QPushButton{padding:2px 4px}")
        self.button4.clicked.connect(self.close)

    def onButtonClick(self):
        self.close()
        self.s = NumberHuaRong()
        self.s.show()

    def onButtonClick2(self):
        self.close()
        self.s = Grade()
        self.s.show()

class Grade(QMainWindow):
    def __init__(self, parent=None):
        super(Grade, self).__init__(parent)
        self.resize(600, 600)
        self.setWindowTitle('历史得分')

        palette1 = QPalette()
        palette1.setColor(self.backgroundRole(), QColor(192, 253, 123))
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('background4.jpg')))
        self.setPalette(palette1)
        self.label = QLabel(self)

        self.label.setGeometry(200, 0, 400, 200)
        self.label.setText("历史得分")
        self.setStyleSheet("QLabel{color:rgb(0,205,205,255);font-size:50px;font-weight:bold;font-family:Arial;}")

        self.label = QLabel(self)
        self.label.setGeometry(270, 50, 300, 300)
        with open("score.txt", "r", encoding="utf-8") as fp:
            scores = fp.readlines()
            ls = []  # 只保留前15个记录
            for score in scores:
                ls.append(int(score.replace('\n', '')))
            ls = sorted(ls)
            finalstr = ' 步数\n'
            if len(ls) >= 15:
                for i in range(15):
                    if i < 9:
                        finalstr += (str(i + 1) + '.' + "  " + str(ls[i]) + '\n')
                    else:
                        finalstr += (str(i + 1) + '.' + " " + str(ls[i]) + '\n')
            else:
                for i in range(len(ls)):
                    if i < 9:
                        finalstr += (str(i + 1) + '.' + "  " + str(ls[i]) + '\n')
                    else:
                        finalstr += (str(i + 1) + '.' + " " + str(ls[i]) + '\n')
            self.label.setText(finalstr)
            self.label.setStyleSheet("QLabel{color:rgb(0,0,0,255);font-size:20px;font-weight:bold;font-family:楷体;}")

        self.button3 = QPushButton('返回主页面︿(￣︶￣)︿', self)
        self.button3.setGeometry(50, 450, 150, 100)
        self.button3.setStyleSheet("QPushButton{color:black}"
                                   "QPushButton:hover{color:red}"
                                   "QPushButton{background-color:rgb(78,255,255)}"
                                   "QPushButton{border:2px}"
                                   "QPushButton{border-radius:10px}"
                                   "QPushButton{padding:2px 4px}")
        self.button3.clicked.connect(self.comeback)

        self.button5 = QPushButton('再来一把┗|｀O′|┛ ', self)
        self.button5.setGeometry(405, 450, 150, 100)
        self.button5.setStyleSheet("QPushButton{color:black}"
                                   "QPushButton:hover{color:red}"
                                   "QPushButton{background-color:rgb(78,255,255)}"
                                   "QPushButton{border:2px}"
                                   "QPushButton{border-radius:10px}"
                                   "QPushButton{padding:2px 4px}")
        self.button5.clicked.connect(self.playagain)

    def comeback(self):
        self.hide()
        self.f = WinForm()
        self.f.show()

    def playagain(self):
        self.close()
        self.s = NumberHuaRong()
        self.s.show()

class Direction(IntEnum):


    # 用枚举类表示方向

    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class NumberHuaRong(QWidget):
    """ 华容道主体 """
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.zero_row = 0
        self.zero_column = 0
        self.gltMain = QGridLayout()
        self.initUI()

    def initUI(self):
        # 设置方块间隔
        self.onInit()
        self.gltMain.setSpacing(5)
        self.gltMain.setContentsMargins(0,0,0,0)
        # 设置布局
        self.setLayout(self.gltMain)
        # 设置宽和高
        self.setFixedSize(650, 650)
        # 设置标题
        self.setWindowTitle('数字华容道')
        # 设置背景颜色
        #self.setStyleSheet("background-color:gray;")
        palette1 = QPalette()
        palette1.setColor(self.backgroundRole(), QColor(192, 253, 123))
        palette1.setBrush(self.backgroundRole(), QBrush(QPixmap('background4.jpg')))
        self.setPalette(palette1)
        self.show()

    # 初始化布局
    def onInit(self):
        # 产生顺序数组
        self.score = 0
        self.numbers = list(range(1,10))
        self.a = random.randint(0,8)
        self.numbers[self.a] = 0
        # 将数字添加到二维数组
        self.blocks.clear()
        for row in range(3):
            self.blocks.append([])
            for column in range(3):
                temp = self.numbers[row * 3 + column]

                if temp == 0:
                    self.zero_row = row
                    self.zero_column = column
                self.blocks[row].append(temp)

        # # 打乱数组
        for i in range(500):
            random_num = random.randint(0, 3)
            self.move(Direction(random_num))

        self.updatePanel()

    # 检测按键
    def keyPressEvent(self, event):
        key = event.key()
        if(key == Qt.Key_Up or key == Qt.Key_W):
            self.move(Direction.UP)
            self.score += 1
        if(key == Qt.Key_Down or key == Qt.Key_S):
            self.move(Direction.DOWN)
            self.score += 1
        if(key == Qt.Key_Left or key == Qt.Key_A):
            self.move(Direction.LEFT)
            self.score += 1
        if(key == Qt.Key_Right or key == Qt.Key_D):
            self.move(Direction.RIGHT)
            self.score += 1
        self.updatePanel()
        if self.checkResult():
            if QMessageBox.Ok == QMessageBox.information(self, '挑战结果', '恭喜您完成挑战(๑•̀ㅂ•́)و✧！'):
                with open("score.txt","a+",encoding="utf-8") as fp:
                    fp.write(str(self.score)+'\n')
                self.onInit()

    # 方块移动算法
    def move(self, direction):
        if(direction == Direction.DOWN): # 上
            if self.zero_row != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row + 1][self.zero_column]
                self.blocks[self.zero_row + 1][self.zero_column] = 0
                self.zero_row += 1
        if(direction == Direction.UP): # 下
            if self.zero_row != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row - 1][self.zero_column]
                self.blocks[self.zero_row - 1][self.zero_column] = 0
                self.zero_row -= 1
        if(direction == Direction.RIGHT): # 左
            if self.zero_column != 2:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column + 1]
                self.blocks[self.zero_row][self.zero_column + 1] = 0
                self.zero_column += 1
        if(direction == Direction.LEFT):   # 右
            if self.zero_column != 0:
                self.blocks[self.zero_row][self.zero_column] = self.blocks[self.zero_row][self.zero_column - 1]
                self.blocks[self.zero_row][self.zero_column - 1] = 0
                self.zero_column -= 1

    def updatePanel(self):
        for row in range(3):
            for column in range(3):
                self.gltMain.addWidget(Block(self.blocks[row][column]), row, column)

        self.setLayout(self.gltMain)

    # 检测是否完成
    def checkResult(self):
        if self.blocks[self.a//3][self.a%3] != 0:
            return False

        for row in range(3):
            for column in range(3):
                # 运行到此处说名最右下角已经为0，pass即可
                if row == self.a//3 and column == self.a%3:
                    pass
                # 值是否对应
                elif self.blocks[row][column] != row * 3 + column + 1:
                    return False

        return True


class Block(QLabel):

    """ 数字方块 """

    def __init__(self, number):
        super().__init__()

        self.number = number
        self.setFixedSize(200, 200)

        # 设置字体
        font = QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.setFont(font)

        # 设置字体颜色
        pa = QPalette()
        pa.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(pa)
        # 设置文字位置
        self.setAlignment(Qt.AlignCenter)
        # 设置背景颜色\圆角和文本内容
        if self.number == 0:
            self.setStyleSheet("background-color:white") # border-image:url(./bc.gif);
        # if self.number == 2:
        #     self.setStyleSheet("border - image: url(./2.png);background-color:white")
        # if self.number == 3:
        #     self.setStyleSheet("border - image: url(./3.png);background-color:white")
        # if self.number == 4:
        #     self.setStyleSheet("border - image: url(./4.png);background-color:white")
        # if self.number == 5:
        #     self.setStyleSheet("border - image: url(./5.png);background-color:white")
        # if self.number == 6:
        #     self.setStyleSheet("border - image: url(./6.png);background-color:white")
        # if self.number == 7:
        #     self.setStyleSheet("border - image: url(./7.png);background-color:white")
        # if self.number == 8:
        #     self.setStyleSheet("border - image: url(./8.png);background-color:white")
        # if self.number == 9:
        #     self.setStyleSheet("border - image: url(./9.png);background-color:white")
        else:
            # self.setStyleSheet("background-color:red")
            # self.setText(str(self.number))
            if self.number == 1:
                self.setStyleSheet("border-image:url(./1.jpg);background-color:white")
            if self.number == 2:
                self.setStyleSheet("border-image:url(./2.jpg);background-color:white")
            if self.number == 3:
                self.setStyleSheet("border-image:url(./3.jpg);background-color:white")
            if self.number == 4:
                self.setStyleSheet("border-image:url(./4.jpg);background-color:white")
            if self.number == 5:
                self.setStyleSheet("border-image:url(./5.jpg);background-color:white")
            if self.number == 6:
                self.setStyleSheet("border-image:url(./6.jpg);background-color:white")
            if self.number == 7:
                self.setStyleSheet("border-image:url(./7.jpg);background-color:white")
            if self.number == 8:
                self.setStyleSheet("border-image:url(./8.jpg);background-color:white")
            if self.number == 9:
                self.setStyleSheet("border-image:url(./9.jpg);background-color:white")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = WinForm()
    form.show()
    #ex = NumberHuaRong()
    sys.exit(app.exec_())
