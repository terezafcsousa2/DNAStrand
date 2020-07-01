
#!/usr/bin/env python
# coding: UTF-8
#
## @DNAStrandInterface
#
#   @author Terezinha Freire Carvalho de Sousa - 19113050038
#   @since 10/05/2020

from tkinter import *
from tkinter.ttk import *
from tkinter.font import Font
from random import randint

class DNAStrandInterface: 
    ## Valid DNA symbols.
    symbols = 'atcg'
    complSymbols = {
        'a':'t',
        't':'a',
        'c':'g',
        'g':'c'
    }
    def __init__(self, master = None, data1 = "", data2 = ""): 
        
        self.master = master 
        
        self.canResize = 0
        self.helpIsOpen = False

        #text fonts
        self.font = Font(family="Courier", size=22)
        self.widthOfChar = self.font.measure("a")
        self.heightOfChar = self.font.metrics("linespace")


        self.fontHelp = Font(family="Courier", size=12)
        self.widthOfCharHelp = self.fontHelp.measure("a")
        self.heightOfCharHelp = self.fontHelp.metrics("linespace")

        
        self.canvas = Canvas(master)
        self.recenter()
        
        self.dnaMoving = False

        self.x = 0
        self.y = 0
        
        self.getData()
        self.movement() 


    #initial scene to choose method of input data   
    def getData(self):
        self.buttonFile = Button(self.master, text = "Get data from file", command = self.getDataFile)
        self.buttonType = Button(self.master, text = "Type data", command = self.getDataType)
        
        self.buttonFile.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.buttonType.place(relx=0.5, rely=0.6, anchor=CENTER)
        self.canvas.pack()

    #destroys initial scene
    def destroyInitMenu(self):  
        self.buttonFile.destroy()    
        self.buttonType.destroy()

    #get input from file
    #generates error if the path is invalid    
    def getEntryFileData(self):
        path = self.entryFile.get() 
        
        try:
            with open(path, 'r') as f:
                data1 = f.readline()
                if(len(data1) >= 1 and data1[len(data1)-1]=='\n'):
                    data1 = data1[:-1]
                data2 = f.readline()
                if(len(data2) >= 1 and data2[len(data2)-1]=='\n'):
                    data2 = data2[:-1]
                f.close()
                self.destroyDataFile()
                self.setData(data1, data2)
        except IOError as e:
            print("Invalid path")
            self.canvas.destroy()
            exit()

    #destroys data file scene
    def destroyDataFile(self):        
        self.entryFile.destroy()
        self.labelFile.destroy()
        self.buttonGetDataFile.destroy()    
    
    #creates data file scene
    def getDataFile(self):            
        self.destroyInitMenu()
        txt1 = "Path: "
        self.labelFile = Label(master, text=txt1, font = self.font)
        self.entryFile = Entry(self.master) 
        self.buttonGetDataFile = Button(self.master, text = "ENTER", command=self.getEntryFileData)
        
        self.buttonGetDataFile.place(relx=0.5, rely=0.7, anchor=CENTER)
        self.labelFile.place(relx=0.4, rely=0.5, anchor=CENTER)
        self.entryFile.place(relx=0.6, rely=0.5, anchor=CENTER)
        
    #creates data type scene
    def getDataType(self):            
        self.destroyInitMenu()
        txt1 = "DNA strand 1: "
        self.labelDna1 = Label(master, text=txt1, font = self.font)
        txt2 = "DNA strand 2: "
        self.labelDna2 = Label(master, text=txt2, font = self.font)
        self.entryDna1 = Entry(self.master) 
        self.entryDna2 = Entry(self.master) 
        self.buttonGetDataType = Button(self.master, text = "ENTER", command=self.getEntryData)
        self.labelDna1.place(relx=0.4, rely=0.2, anchor=CENTER)
        self.entryDna1.place(relx=0.7, rely=0.2, anchor=CENTER)
        self.labelDna2.place(relx=0.4, rely=0.4, anchor=CENTER)
        self.entryDna2.place(relx=0.7, rely=0.4, anchor=CENTER)
        self.buttonGetDataType.place(relx=0.5, rely=0.7, anchor=CENTER)
        self.canvas.pack()


    #destroys data type scene
    def destroyDataType(self):
        self.entryDna1.destroy()
        self.labelDna1.destroy()
        self.entryDna2.destroy()
        self.labelDna2.destroy()
        self.buttonGetDataType.destroy()

    #gets input from typing
    def getEntryData(self):
        data1 = self.entryDna1.get()
        data2 = self.entryDna2.get()
        self.destroyDataType()
        self.setData(data1, data2)

    #test if given data is valid
    def isValid(self, data):
        if(data == ""):
            return False
        valid = True
        for i in (data):
            flag = False
            for j in(self.symbols):
                if (i == j):
                    flag = True
                    break
            if flag == False:
                valid = False
                break
        return valid

    #generates error if given data is invalid
    def validateData(self, data1, data2):
        try:
            if self.isValid(data1) == False:
                raise ValueError('invalid givenData strand1')
            if self.isValid(data2) == False:
                raise ValueError('invalid givenData strand2')
        except ValueError as error:
                print(str(error))
                self.canvas.destroy()
                exit()


    #sets data1 and data2 and creates dna moving scene
    def setData(self, data1, data2):

        self.canResize = 0
        self.data1 = data1.replace('A','a').replace('T','t').replace('G','g').replace('C','c')
        self.data2 = data2.replace('A','a').replace('T','t').replace('G','g').replace('C','c')
        self.validateData(self.data1, self.data2)
        self.reset()

        #creates strands with the given data
        self.strand1 = self.canvas.create_text( 
                        self.center['x'], self.center['y'], text = self.data1, font = self.font )
        self.strand2 = self.canvas.create_text( 
                        self.center['x'] + self.x, self.center['y'] + self.y + self.widthOfChar, text = self.data2, font = self.font)
        
        #creates help message
        self.helpMSG = self.canvas.create_text( 
                         10 + len("h - help")*self.widthOfCharHelp/2.0, 10, text = "h - help", font = self.fontHelp, fill="red")
        self.helpList = ["Shift-L - shuffle", "Escape - exit", "m - got to position", "    of maximum matches", "right key - move right", "left key - move left", "upper key - move up", "down key - move down", "Tab - reset"] 
        self.helpPosX = [ 0, 0, 0, 0,(25*self.widthOfCharHelp), (25*self.widthOfCharHelp), (25*self.widthOfCharHelp), (25*self.widthOfCharHelp), (25*self.widthOfCharHelp)]
        self.helpPosY = [ 1, 2, 3, 4, 0, 1, 2, 3, 4]
        self.helpTexts = []
        for i in range(len(self.helpList)):
            self.helpTexts.append(self.canvas.create_text( 
                         10 + len(self.helpList[i])*self.widthOfCharHelp/2.0 + self.helpPosX[i], 10 + self.heightOfCharHelp*self.helpPosY[i] , text = "", font = self.fontHelp))

        
        self.recenter() 
        self.canvas.config(width=2560, height=1536)
        self.canvas.pack()
        self.dnaMoving = True
        
        


    #deals with help message
    def help(self, event):

        if(self.dnaMoving):
            msg =""
            if(self.helpIsOpen == True):
                msg = "h - help"
                for i in range(len(self.helpList)):
                    self.canvas.itemconfig(self.helpTexts[i], text = "")
            else:
                msg = "h - close help"
                for i in range(len(self.helpList)):
                    self.canvas.itemconfig(self.helpTexts[i], text = self.helpList[i])
                
            self.canvas.itemconfig(self.helpMSG, text = msg)
            self.canvas.coords(self.helpMSG, 10 + len(msg)*self.widthOfCharHelp/2.0, 10)           
            self.helpIsOpen = not self.helpIsOpen


        

    #recenters components
    def recenter(self):
        self.canvas.pack()
        self.center = {'y' : self.canvas.winfo_height()/2.0, 'x' : self.canvas.winfo_width()/2.0}
        
    #resizes window
    def resize(self, event):
        self.width = event.width  
        self.height = event.height
        
        if(self.canResize >= 1):
            self.canvas.config(width=self.width, height=self.height)
            self.canvas.pack()
            self.canResize = 0
        else:
            self.canResize += 1
        
    #sets strand2 relative position to the starting position
    def reset(self):
        self.x = (len(self.data2) - len(self.data1))*self.widthOfChar/(2.0)
        self.y = self.heightOfChar

    def callReset(self, event):
        if(self.dnaMoving):
            self.reset()

    
    #deals with the strands movements
    def movement(self):
        self.recenter()
        if(self.dnaMoving):
            self.canvas.coords(self.strand1, self.center['x'], self.center['y'])
            self.canvas.coords(self.strand2, self.center['x'] + self.x, self.center['y'] + self.y)
            
            x_strand2 = self.canvas.coords(self.strand2)[0] 
            y_strand2 = self.canvas.coords(self.strand2)[1]

            width_strand2 = len(self.data2)*self.widthOfChar
            height_strand2 = self.heightOfChar

            if(x_strand2 + width_strand2/2 <= 0 or x_strand2 - width_strand2/2 >= self.canvas.winfo_width()):
                self.reset()
            elif(y_strand2 + height_strand2/2 <= 0 or y_strand2 - height_strand2/2 >= self.canvas.winfo_height()):
                self.reset()
            
            self.matches()
  
        self.canvas.after(100, self.movement) 
    
    def left(self, event): 
        self.x += -5
        self.y += 0
    
    def right(self, event): 
        self.x += 5
        self.y += 0
    
    def up(self, event): 
        self.x += 0
        self.y += -5
    
 
    def down(self, event): 
        self.x += 0
        self.y += 5


    #returns if math of c1 and c2 is valid
    def charMatch(self, c1, c2):
        match = False
        if c1 in self.symbols:
            if c2 == self.complSymbols[c1]:
                match = True

        # If c1 is in the complement symbols dictionary and c2 is equal to the complement of c1 the match is valid
 
        return match
    
    def findMatchesWithRightShift(self, shift):       
        myStrand = self.data2
        otherStrand = self.data1

        mat = [False]*len(myStrand)
        
        myIndex = shift # right shift the other is equal to left shift myself
        otherIndex = 0

        # iterates through the letters of the strands testing matches
        i = 0
        while(otherIndex + i < len(otherStrand) and myIndex + i < len(myStrand)):
            c1 = otherStrand[otherIndex + i]
            c2 = myStrand[myIndex + i] 
            if (self.charMatch(c1, c2)== True):
                mat[myIndex + i] = True
            i+=1

        # iterates through the mat array inserting each modified character at its corresponding position in the matches string
        
        matches = ''
        for i in range(len(mat)):
            if (mat[i]==False):
                matches += (myStrand[i]).lower()
            else:
                matches += myStrand[i].upper()
        return matches
    
    def findMatchesWithLeftShift(self, shift):       
        myStrand = self.data2
        otherStrand = self.data1

        mat = [False]*len(myStrand)
        
        myIndex = 0
        otherIndex = shift

        # iterates through the letters of the strands testing matches
        i = 0
        while(otherIndex + i < len(otherStrand) and myIndex + i < len(myStrand)):
            c1 = otherStrand[otherIndex + i]
            c2 = myStrand[myIndex + i] 
            if (self.charMatch(c1, c2) == True):
                mat[myIndex + i] = True
            i+=1

        # iterates through the mat array inserting each modified character at its corresponding position in the matches string
        
        matches = ''
        for i in range(len(mat)):
            if (mat[i]==False):
                matches += (myStrand[i]).lower()
            else:
                matches += myStrand[i].upper()
        return matches
    
    def countMatchesWithRightShift(self, shift):       
        myStrand = self.data2
        otherStrand = self.data1

        count = 0
        
        myIndex = shift # right shift the other is equal to left shift myself
        otherIndex = 0

        # iterates through the letters of the strands testing matches
        i = 0
        while(otherIndex + i < len(otherStrand) and myIndex + i < len(myStrand)):
            c1 = otherStrand[otherIndex + i]
            c2 = myStrand[myIndex + i] 
            if (self.charMatch(c1, c2)== True):
                count += 1
            i+=1

        return count
    
    def countMatchesWithLeftShift(self, shift):       
        myStrand = self.data2
        otherStrand = self.data1

        count = 0
        
        myIndex = 0
        otherIndex = shift

        # iterates through the letters of the strands testing matches
        i = 0
        while(otherIndex + i < len(otherStrand) and myIndex + i < len(myStrand)):
            c1 = otherStrand[otherIndex + i]
            c2 = myStrand[myIndex + i] 
            if (self.charMatch(c1, c2) == True):
                count += 1
            i+=1

        return count

    def findMaxPossibleMatches(self, event):
        if(self.dnaMoving):
            countMax = -1
            posMax = -1

            limitShiftLeft = len(self.data1) - 1
            limitShiftRight = len(self.data2) - 1

            for shift in range(limitShiftLeft):
                matches = self.countMatchesWithLeftShift(shift)
                if (matches > countMax):
                    countMax = matches
                    posMax = shift

            for shift in range(limitShiftRight):
                matches = self.countMatchesWithRightShift(shift)
                if (matches> countMax):
                    countMax = matches
                    posMax = -shift
            
            self.reset()
            self.x += posMax*self.widthOfChar
            
        
    

    # tests matches and indicates them with uppercase letters
    def matches(self):
        self.canvas.pack()
        ini_x_strand2 = self.center['x'] + (len(self.data2) - len(self.data1))*self.widthOfChar/(2.0)
        x_strand2 = self.canvas.coords(self.strand2)[0]

        if(x_strand2 >= ini_x_strand2):
            shift = (int) (x_strand2 - ini_x_strand2) // self.widthOfChar
            self.canvas.itemconfig(self.strand2, text = self.findMatchesWithLeftShift(shift))
        else:
            shift = (int) (ini_x_strand2 - x_strand2) // self.widthOfChar
            self.canvas.itemconfig(self.strand2, text = self.findMatchesWithRightShift(shift))
    
    #shuffles letters of strand2
    def shuffle(self, event):
        if(self.dnaMoving):
            newData = list(self.data2)
            for i in range(0,len(newData) - 1):
                j = randint(i+1, len(newData)-1)
                newData[i], newData[j] = newData[j], newData[i]
            self.data2 = ''.join(newData)
            self.canvas.itemconfig(self.strand2, text = self.data2)
        
    #exits application
    def quit(self, event):
        self.canvas.destroy()
        exit()


        



if __name__ == "__main__": 

    master = Tk() 
    master.title("DNAStrandInterface - Terezinha - Matr.: 19113050038") 
    dnaInter = DNAStrandInterface(master,"AGAGCAT","TCAT") 

    master.bind("<KeyPress-Left>", lambda e: dnaInter.left(e)) 
    master.bind("<KeyPress-Right>", lambda e: dnaInter.right(e)) 
    master.bind("<KeyPress-Up>", lambda e: dnaInter.up(e)) 
    master.bind("<KeyPress-Down>", lambda e: dnaInter.down(e))
    master.bind("<KeyPress-Tab>", lambda e: dnaInter.callReset(e))
    master.bind("<Shift-KeyPress-L>", lambda e: dnaInter.shuffle(e)) 
    master.bind("<Configure>", lambda e: dnaInter.resize(e)) 
    master.bind("<KeyPress-Escape>", lambda e: dnaInter.quit(e))
    master.bind("<KeyPress-h>", lambda e: dnaInter.help(e))
    master.bind("<KeyPress-m>", lambda e: dnaInter.findMaxPossibleMatches(e))
    master.geometry("600x400",)
     
    mainloop() 
