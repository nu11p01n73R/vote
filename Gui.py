import sys
from PyQt4 import Qt,QtGui,QtCore
from Batch import Batch


class Gui(Qt.QWidget):
    def __init__(self,args):
        super(Gui,self).__init__()
        self.layout = QtGui.QGridLayout()
        #self.mainPage()i
        self.batches = []
        self.genObjs()
        self.selectPage()
        self.resize(300,300)
        self.setLayout(self.layout)
        self.show()
    
    def genObjs(self):
        try:
            inputFile = open("data","r")
        except IOError:
            temp = open("data","w")
            temp.close()
            inputFile = open("data","r")
        for line in inputFile:
            batch = Batch("",0,0,[])
            batch.readFile(line)
            self.batches.append(batch)


    def removeAll(self):
        for i in reversed(range(self.layout.count())): 
            self.layout.itemAt(i).widget().deleteLater()
    
    
    def getList(self):
        res = []
        for batch in self.batches:
            res.append(batch.name)
        return res

    def selectPage(self):
        self.removeAll()
        self.editFlag = False
        self.classList = QtGui.QListWidget()
        items = self.getList()
        self.classList.addItems(items)
        add = QtGui.QPushButton("Add class")
        edit = QtGui.QPushButton("Edit class")
        result = QtGui.QPushButton("View Result")
        vote = QtGui.QPushButton("Start Voting")

        add.clicked.connect(self.adminPage)
        edit.clicked.connect(self.edit)
        result.clicked.connect(self.result)
        vote.clicked.connect(self.vote)

        self.layout.addWidget(self.classList,0,1)
        self.layout.addWidget(add,3,1)
        self.layout.addWidget(edit,3,2)
        self.layout.addWidget(result,4,1)
        self.layout.addWidget(vote,4,2)

    def adminPage(self):
        self.removeAll()
        
        label = QtGui.QLabel("Class")
        labelTotal = QtGui.QLabel("Total Students")
        labelPre = QtGui.QLabel("Present")
        labelCont = QtGui.QLabel("No. of Contestents")

        self.textName = QtGui.QLineEdit()
        self.textTotal = QtGui.QLineEdit()
        self.textPresent = QtGui.QLineEdit()
        self.cont = QtGui.QLineEdit()
        add = QtGui.QPushButton("Done",None)
        add.clicked.connect(self.addCont)

        self.layout.addWidget(label,0,0)
        self.layout.addWidget(self.textName,0,1)
        self.layout.addWidget(labelTotal,1,0)
        self.layout.addWidget(self.textTotal,1,1)
        self.layout.addWidget(labelPre,2,0)
        self.layout.addWidget(self.textPresent,2,1)
        self.layout.addWidget(labelCont,3,0)
        self.layout.addWidget(self.cont,3,1)
        self.layout.addWidget(add,4,1)
        #self.setLayout(self.vlayout)

    def addCont(self):
        self.name = self.textName.text()
        self.total = int(self.textTotal.text())
        self.pre = int(self.textPresent.text())
        self.removeAll()
        no = int(self.cont.text())
        self.contestants = []
        for i in range(no):
            cont = QtGui.QLineEdit()
            self.layout.addWidget(cont,i,1)
            self.contestants.append(cont)
        done = QtGui.QPushButton("Done",None)
        self.layout.addWidget(done,i+1,1)
        done.clicked.connect(self.addClass)
    
    def addClass(self):
        tempList = []
        for cont in self.contestants:
            tempList.append(cont.text())
        if self.editFlag == True:
            for index,batch in enumerate(self.batches):
                if batch.name == self.name:
                    self.batches.pop(index)
        new = Batch(self.name,self.total,self.pre,tempList)
        self.batches.append(new)
        self.removeAll()

        msg = QtGui.QLabel("Batch added successfully")
        done = QtGui.QPushButton("Done",None)
    
        done.clicked.connect(self.selectPage)
        
        self.layout.addWidget(msg,2,1)
        self.layout.addWidget(done,3,1)
        
        flush = open("data","w")
        flush.write('')
        flush.close()
        for batch in self.batches:
            batch.writeFile()
    
    def edit(self):
        self.editFlag = True
        self.adminPage()

    def result(self):
        name = self.classList.currentItem().text()

        self.removeAll()
   
        nameLabel = QtGui.QLabel()
        contLabel = QtGui.QLabel()

        totalLabel = QtGui.QLabel()
        totalContLabel = QtGui.QLabel()

        votedLabel = QtGui.QLabel("No. students voted")
        votedContLabel = QtGui.QLabel()

        preLabel = QtGui.QLabel()
        preContLabel = QtGui.QLabel()

        contsLabel = []
        voteLabel = []

        winnerLabel = QtGui.QLabel("Winner")
        winnerName = QtGui.QLabel()

        for batch in self.batches:
            if batch.name == name:
                nameLabel.setText("Name")
                contLabel.setText(batch.name)
                self.layout.addWidget(nameLabel,3,1)
                self.layout.addWidget(contLabel,3,2)

                totalLabel.setText("Total Students")
                totalContLabel.setText(str(batch.total))
                self.layout.addWidget(totalLabel,4,1)
                self.layout.addWidget(totalContLabel,4,2)
                
                preLabel.setText("Present")
                preContLabel.setText(str(batch.present))
                self.layout.addWidget(preLabel,5,1)
                self.layout.addWidget(preContLabel,5,2)

                votedContLabel.setText(str(batch.voted))
                self.layout.addWidget(votedLabel,6,1)
                self.layout.addWidget(votedContLabel,6,2)

                winnerName.setText(batch.winner)
                self.layout.addWidget(winnerLabel,7,1)
                self.layout.addWidget(winnerName,7,2)
        
                for cont in batch.votes:
                    label = QtGui.QLabel(cont)
                    vote = QtGui.QLabel(str(batch.votes[cont]))
                    contsLabel.append(label)
                    voteLabel.append(vote)

                for i,cont in enumerate(contsLabel):
                    self.layout.addWidget(cont,8+i,1)
                    self.layout.addWidget(voteLabel[i],8+i,2)
                
        done = QtGui.QPushButton("Done",None)
        done.clicked.connect(self.selectPage)
        self.layout.addWidget(done,9+i,2)
    
    def vote(self):
        try:
            name  = self.classList.currentItem().text()
            for batch in self.batches:
                if batch.name == name:
                    self.votingBatch = batch
                    break
        except RuntimeError:
            pass

        self.removeAll()
        print batch.votes 
        if self.votingBatch.present > self.votingBatch.voted:
            contList = []
            for i,contestant in enumerate(self.votingBatch.votes):
                button = QtGui.QPushButton(contestant,None)
                contList.append(button)
                self.layout.addWidget(button,1+i,2)
        
            for button in contList:
                button.clicked.connect(self.incrVote)

        else:
            self.finishVote()

    def incrVote(self):
        button = self.sender()
        contestant = button.text()
        self.votingBatch.vote(str(contestant))
        self.removeAll()
        
        if self.votingBatch.voted >= self.votingBatch.present:
            self.votingBatch.result()
            self.finishVote()
        else:
            self.counter()
    
    def counter(self):
        self.lcd = QtGui.QLCDNumber()
        self.timer = QtCore.QTimer()
        self.count = 10 
        self.lcd.display(self.count)
        self.layout.addWidget(self.lcd)
        self.timer.timeout.connect(self.updateLCD)
        self.timer.start(1000)
        #self.vote()
    
    def updateLCD(self):
        self.count -= 1
        if self.count >= 0:
            self.lcd.display(self.count)
        else:
            self.timer.stop()
            self.vote()

    def finishVote(self):
        self.removeAll()
        flush = open("data","w")
        flush.write('')
        flush.close()
        for batch in self.batches:
            batch.writeFile()

        msg = QtGui.QLabel("Voting completed successfully!!!")
        self.layout.addWidget(msg,2,1)
        done = QtGui.QPushButton("Done",None)
        done.clicked.connect(self.selectPage)
        self.layout.addWidget(done,3,1)

app = QtGui.QApplication(sys.argv)
gui = Gui(sys.argv)
app.exec_()
