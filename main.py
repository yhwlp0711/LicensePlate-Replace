import sys
from PyQt5 import QtWidgets
from MainMenu import MainWidget

if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  main = MainWidget()
  main.show()
  sys.exit(app.exec_())
