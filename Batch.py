
class Batch:
    def __init__(self, name, total, present, contestants):
        self.name = name
        self.total = total
        self.present = present
        self.voted = 0
        self.votes = {}
        self.initializeVote(contestants)
        self.winner = ""
   
         
    
    def initializeVote(self,contestants):
        for contestant in contestants:
            self.votes[str(contestant)] = 0

    def vote(self,contestant):
        self.votes[contestant] += 1
        self.voted += 1

    def result(self):
        finalVotes = sorted(self.votes,reverse = True)
        self.winner = finalVotes[0]

    def cipher(self,string):
        alphanum = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 0123456789,"
        cipherText = ""
        for char in str(string):
            try:
                index = (alphanum.index(char)+13)%len(alphanum)
                cipherText += alphanum[index]
            except ValueError:
                cipherText += char
        return cipherText

    def decipher(self,string):
        alphanum = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz 0123456789,"
        plainText = ""
        for char in str(string):
            try:
                index = (alphanum.index(char)-13)%len(alphanum)
                plainText += alphanum[index]
            except ValueError:
                plainText += char
        return plainText
    
    def writeFile(self):
        output = open('data','a')
        content = self.name+','+str(self.total)+','+str(self.present)+','+str(self.voted)
        for contestant in self.votes:
            content += ','+contestant+":"+str(self.votes[contestant]) 
        encryContent = self.cipher(content)
        output.write(encryContent+'\n')

    def readFile(self,line):
        content = self.decipher(line)
        content = content.split(',')
        self.name = content[0]
        self.total = int(content[1])
        self.present = int(content[2])
        self.voted = int(content[3])
        for contestant in content[4:]:
            key,value = contestant.split(":")
            self.votes[key] = int(value)
        
"""
five = Batch("V A", 5, 5, ['a','b','c'])
five.vote('b')
five.vote('b')
five.vote('c')
five.vote('c')
five.vote('c')
five.result()
five.writeFile()

"""
