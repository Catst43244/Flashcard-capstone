import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import pandas as pd
import random as ra
from playsound import playsound
import threading
def playSoundFun():
    playsound("walking-on-a-wooden-floor-32056.mp3")
def gameOverSound():
    playsound("fuzzy-jumpscare-80560.mp3")
class cards:
    MISSED_COUNTER_WARNING_SOUND = 2
    MISSED_COUNTER_GAME_OVER = 4
    def __init__(self):
        #problem: there are repeats in the summury screen
        self.remove = []
        self.missed = []
        self.data = pd.read_excel('database.xlsx')
        self.termsLeft = self.data['TERMS'].values.tolist()      
        self.POS = ra.randrange(0,len(self.data))
        self.card = self.data.iloc[self.POS]
        self.cardTerm = str(self.card.loc["TERMS"])
        self.cardDef = str(self.card.loc["DEF"])
        self.buttons = True
        #problem: have a var that takes the input into true and false 
        self.missedCounter = 0
        self.GAMEOVER = False
        self.playWarningSoundThread = threading.Thread(target=playSoundFun, name="Playsound")
        self.playGameOverSoundThread = threading.Thread(target=gameOverSound, name="Playsound")
        self.playWarningSoundThread.daemon = True
        self.playGameOverSoundThread.daemon = True
    def rerun(self,knownCard = False):
        if knownCard == True:
            self.remove.append(self.POS)
        if knownCard == False:
            if self.POS != self.missed:
                self.missed.append(self.POS)
            self.missedCounter += 1
            match self.missedCounter:
                case cards.MISSED_COUNTER_WARNING_SOUND:
                    self.playWarningSoundThread.start()
                    print("Playsound")
                case cards.MISSED_COUNTER_GAME_OVER:
                    self.playGameOverSoundThread.start()
                    print("GAME OVER")
                    self.GAMEOVER = True
                    self.buttons = False
        self.lastPOS = self.POS
        self.POS = ra.randrange(0,len(self.termsLeft))
        if self.POS in self.remove:
            while self.POS in self.remove:
                self.POS = ra.randrange(0,len(self.termsLeft))
                if len(self.remove) >= len(self.termsLeft):
                    self.buttons = False
                    break
        if self.POS == self.lastPOS:
            self.rerun()
            pass
        self.card = self.data.iloc[self.POS]
        self.cardTerm = str(self.card.loc["TERMS"])
        self.cardDef = str(self.card.loc["DEF"])
        pass
    
    pass
'''
class FlashcardsUiApp:
    def __init__(self, master = None):
                #USE THIS LATER. it removes buttons OwO
        #self.filpCardButton.place_forget()
        # from cards
        self.c = cards()
        self.cardText = self.c.cardTerm
        
        #-----
        self.flashcards = tk.Tk() if master is None else tk.Toplevel(master)
        self.flashcards.configure(
            height=200,
            relief="flat",
            takefocus=True,
            width=200)
        #unused code ;(

        self.flashcards.bind('<Left>', self.left_key)
        self.flashcards.bind('<Right>', self.right_key)
        self.flashcards.bind('<KeyRelease-Down>',self.down_key)

        self.knowButton = ttk.Button(self.flashcards)
        self.knowButton.configure(text='know', width=50)
        self.knowButton.grid(column=0, ipady=20, row=1, sticky="w")
        self.knowButton.configure(command=self.KnowBu)
        self.notKnowButton = ttk.Button(self.flashcards)
        self.notKnowButton.configure(text="don't know", width=50)
        self.notKnowButton.grid(column=0, ipady=20, row=1, sticky="e")
        self.notKnowButton.configure(command=self.notKnowBu)
        self.filpCardButton = ttk.Button(self.flashcards)
        self.filpCardButton.configure(text='filp card')
        self.filpCardButton.grid(column=0, ipady=20, row=1, sticky="n")
        self.filpCardButton.configure(command=self.filpCardBu)
        
        self.viewedCard = tk.Text(self.flashcards)
        self.viewedCard.configure(
            font="{Arial} 20 {}",
            height=10,
            relief="flat",
            takefocus=False,
            width=50,)
        self.setText(self.c.cardTerm)
        self.viewedCard.grid(column=0, row=0)


        # Main widget
        self.mainwindow = self.flashcards

'''


class Ui:
    def __init__(self, root, master = None):
        self.c = cards()
        self.cardText = self.c.cardTerm
        #setting title
        root.title("undefined")
        #setting window size
        width=1200
        height=700
        self.root = tk.Tk() if master is None else tk.Toplevel(master)
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        root.configure(bg = "#4e4f4f")

        self.knowButton=tk.Button(root)
        self.knowButton["anchor"] = "center"
        self.knowButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=16)
        self.knowButton["font"] = ft
        self.knowButton["fg"] = "#000000"
        self.knowButton["justify"] = "center"
        self.knowButton["text"] = "I know this one"
        self.knowButton.place(x=390,y=530,width=403,height=152)
        self.knowButton["command"] = self.KnowBu

        self.notKnowButton=tk.Button(root)
        self.notKnowButton["anchor"] = "center"
        self.notKnowButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=16)
        self.notKnowButton["font"] = ft
        self.notKnowButton["fg"] = "#000000"
        self.notKnowButton["justify"] = "center"
        self.notKnowButton["text"] = "I don't know"
        self.notKnowButton.place(x=390,y=380,width=403,height=146)
        self.notKnowButton["command"] = self.notKnowBu

        self.viewedCard=tk.Listbox(root)
        self.viewedCard = tk.Entry(root)
        self.viewedCard.pack()
        self.viewedCard["borderwidth"] = "1px"
        self.viewedCard["cursor"] = "arrow"
        ft = tkFont.Font(family='Times',size=23)
        self.viewedCard["font"] = ft
        self.viewedCard["fg"] = "#333333"
        self.viewedCard["bg"] = "#6b6c6e"
        self.viewedCard["justify"] = "center"
        self.viewedCard.place(x=20,y=30,width=1153,height=331)
       

        self.filpCardButton=tk.Button(root)
        self.filpCardButton["anchor"] = "center"
        self.filpCardButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=14)
        self.filpCardButton["font"] = ft
        self.filpCardButton["fg"] = "#000000"
        self.filpCardButton["justify"] = "center"
        self.filpCardButton["text"] = "Flip"
        self.filpCardButton.place(x=460,y=270,width=264,height=73)
        self.filpCardButton["command"] = self.filpCardBu
        self.setText(self.c.cardTerm)
    def run(self):
        self.mainwindow.mainloop()
    def setText(self,Text):
        self.viewedCard.configure(state = 'normal')
        self.viewedCard.delete(0, "end")
        self.viewedCard.insert(0, Text)
        self.viewedCard.configure(state = 'disabled')
        pass
    def KnowBu(self):
        self.c.rerun(knownCard = True)
        if self.c.buttons == False:
            self.endScreen()
        else:
            self.setText(self.c.cardTerm)
            pass

    def endScreen(self):
            summaryText = "all cards studied. Here's what you got wrong and their answers"
            if self.c.GAMEOVER == True:
                summaryText = "GAMEOVER. Here's why"
            for missedCardPOS in self.c.missed:
                card = self.c.data.iloc[missedCardPOS]
                cardTerm = str(card.loc["TERMS"])
                cardDef = str(card.loc["DEF"])
                summaryText = summaryText + "\n\n" + cardTerm + "\n" + cardDef
            self.setText(summaryText)
            self.filpCardButton["state"] = "disabled"
            self.notKnowButton["state"] = "disabled"
            self.knowButton["state"] = "disabled"
    def notKnowBu(self):
        self.c.rerun(knownCard = False)
        if self.c.buttons == False:
            self.endScreen()
        else:
            self.setText(self.c.cardTerm)
            pass

    def filpCardBu(self):
        if self.cardText == self.c.cardTerm:
            self.cardText = self.c.cardDef
            self.setText(self.cardText)
            pass
        else:
            self.cardText = self.c.cardTerm
            self.setText(self.cardText)
            pass
        pass
    #unused code ;(
    '''
    @staticmethod
    def left_key(self,event):
        self.notKnowBu()
        pass
    def right_key(self,event):
        self.KnowBu()
        pass
    def down_key(self,event):
        self.filpCardBu()
        pass
    '''


if __name__ == "__main__":
    root = tk.Tk()
    app = Ui(root)
    root.mainloop()
