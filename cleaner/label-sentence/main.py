import label
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
from PyQt5 import QtCore
import sys
import os
import json
import logging
import time

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class Label(QWidget):
    def __init__(self,is_cs=True):
        super().__init__()
        self.MainWindow = QMainWindow()
        self.ui = label.Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.actionOpen.triggered.connect(self.openFile)
        self.ui.actionRollBack.triggered.connect(self.rollBack)
        self.ui.MethodButton.clicked.connect(self.method)
        self.ui.ProblemButton.clicked.connect(self.problem)
        self.ui.OtherButton.clicked.connect(self.other)
        self.ui.BackgroundButton.clicked.connect(self.background)
        self.ui.ResultButton.clicked.connect(self.result)
        self.ui.NextButton.clicked.connect(self.next)
        self.last = 0
        self.filename = ''
        self.savePath = ''
        self.dirname = ''
        # self.previousPaper = {}
        self.button_0 = False  # background 0
        self.button_1 = False  # problem 1
        self.button_2 = False  # method 2
        self.button_3 = False  # result 3
        self.button_4 = False  # other 4
        self.button_5 = False  # Next skip
        self.is_roll_back = False
        self.is_cs = is_cs


        self.ui.MethodButton.setEnabled(False)
        self.ui.ProblemButton.setEnabled(False)
        self.ui.OtherButton.setEnabled(False)
        self.ui.BackgroundButton.setEnabled(False)
        self.ui.ResultButton.setEnabled(False)
        self.ui.NextButton.setEnabled(False)
        self.ui.actionRollBack.setEnabled(False)


    def openFile(self):
        if self.is_cs:
            openfile_name = QFileDialog.getExistingDirectory(self,"Select dictionary",r'F:\Dataset\json_v2')
            self.filename = openfile_name
        else:
            openfile_name = QFileDialog.getOpenFileName(self, "Select Files", './', "Text files(*.txt)")
            self.filename = openfile_name[0]

        start_time = time.time()
        while (True):
            QtCore.QCoreApplication.processEvents()
            if self.filename != '':
                break
            elif time.time()-start_time>5:
                self.ui.PathText.setPlainText("You select none!")
                start_time = time.time()

        self.ui.PathText.setPlainText(os.path.basename(self.filename))
        self.ui.MethodButton.setEnabled(True)
        self.ui.ProblemButton.setEnabled(True)
        self.ui.OtherButton.setEnabled(True)
        self.ui.BackgroundButton.setEnabled(True)
        self.ui.ResultButton.setEnabled(True)
        self.ui.NextButton.setEnabled(True)
        self.ui.actionRollBack.setEnabled(True)
        if self.is_cs:
            self.start_cs()
        else:
            self.start_arxiv()


    def start_cs(self):
        name = os.path.basename(self.filename)
        self.savePath = './data/' + name
        if not os.path.exists(self.savePath):
            os.makedirs(self.savePath)
        if os.path.exists('log.txt'):
            with open('log.txt') as log:
                logs = log.readlines()
                for i in range(len(logs)-1,-1,-1):
                    if name in logs[i]:
                        self.last = int(logs[i].split()[1])
                        break
        self.ui.DoneText.setPlainText("Done: %d" % self.last)
        files = self.iter_files()
        for i in range(self.last): next(files)
        for file in files:
            paper = json.load(open(file))
            paper = {"abstract_text":paper['paper']['abstract'],"category":paper['paper']['category'],
                     "article_id":paper['paper']['id']}
            while (True):
                if self.label(paper):
                    break
                else:
                    self.label(paper)
            self.last += 1
            self.ui.DoneText.setPlainText("Done: %d" % self.last)

            # self.previousPaper = paper
            logger.info(" %s %d" % (name,self.last))


    def start_arxiv(self):
        name = os.path.basename(self.filename)
        self.ui.PathText.setPlainText(name)
        self.savePath = './data/' + name[:-4]
        if not os.path.exists(self.savePath):
            os.makedirs(self.savePath)
        if os.path.exists('log.txt'):
            with open('log.txt') as log:
                logs = log.readlines()
                for i in range(len(logs)-1,-1,-1):
                    if name[:-4] in logs[i]:
                        self.last = int(logs[i].split()[1])
                        break

        self.ui.DoneText.setPlainText("Done: %d" % self.last)

        lines = self.read_text_file()
        for i in range(self.last): next(lines)

        for paper in lines:
            paper = json.loads(paper)
            while (True):
                if self.label(paper):
                    break
                else:
                    self.label(paper)
            self.last += 1
            self.ui.DoneText.setPlainText("Done: %d" % self.last)

            # self.previousPaper = paper
            logger.info(" %s %d" % (name[:-4],self.last))


    def label(self, paper):

        self.ui.IdText.setPlainText(paper['article_id'])
        labels = []
        for sentence in paper['abstract_text']:
            self.ui.SentenceText.setPlainText(sentence)
            while (True):
                QtCore.QCoreApplication.processEvents()
                if self.button_0:
                    self.button_0 = False
                    labels.append(0)
                    break
                elif self.button_1:
                    self.button_1 = False
                    labels.append(1)
                    break
                elif self.button_2:
                    self.button_2 = False
                    labels.append(2)
                    break
                elif self.button_3:
                    self.button_3 = False
                    labels.append(3)
                    break
                elif self.button_4:
                    self.button_4 = False
                    labels.append(4)
                    break
                elif self.is_roll_back:
                    self.is_roll_back = False
                    return False
                elif self.button_5:
                    self.button_5 = False
                    return True
        with open(self.savePath+'/'+paper['article_id'], 'w') as f:
            paper["labels"] = labels
            f.write(json.dumps(paper))
        return True

    def iter_files(self):
        """Walk through all files located under a root path."""
        if os.path.isfile(self.filename):
            yield self.filename
        elif os.path.isdir(self.filename):
            for dirpath, _, filenames in os.walk(self.filename):
                for f in filenames:
                    yield os.path.join(dirpath, f)
        else:
            raise RuntimeError('Path %s is invalid' % self.filename)

    def read_text_file(self):
        with open(self.filename, "r") as f:
            for line in f:
                yield line

    def next(self):
        # skip curren abstract
        self.button_5 =  True
    def rollBack(self):
        # roll back
        self.is_roll_back = True

    def background(self):
        # background 0
        self.button_0 = True

    def problem(self):
        # problem 1
        self.button_1 = True

    def method(self):
        # method 2
        self.button_2 = True

    def result(self):
        # result 3
        self.button_3 = True

    def other(self):
        # other 4
        self.button_4 = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Label = Label()
    Label.MainWindow.show()
    sys.exit(app.exec_())
