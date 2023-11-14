import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import random as ra
from playsound import playsound
#REMARK THIS WHEN ON LINUX
import threading
def playSoundFun():
    playsound("walking-on-a-wooden-floor-32056.mp3")
def gameOverSound():
    playsound("fuzzy-jumpscare-80560.mp3")
class cards:
    MISSED_COUNTER_WARNING_SOUND = 2
    MISSED_COUNTER_GAME_OVER = 4
    def __init__(self):
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
class FlashcardsUiApp:
    def __init__(self, master = None):
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
        '''
        self.flashcards.bind('<Left>', self.left_key)
        self.flashcards.bind('<Right>', self.right_key)
        self.flashcards.bind('<KeyRelease-Down>',self.down_key)
        '''
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
        self.viewedCard.insert("1.0", self.cardText)
        self.viewedCard.grid(column=0, row=0)


        # Main widget
        self.mainwindow = self.flashcards
        self.viewedCard.configure(state = 'disabled')

    def run(self):
        self.mainwindow.mainloop()
    def setText(self,Text):
        self.viewedCard.delete('1.0', '10000000000.0')
        self.viewedCard.insert("1.0", Text)
        pass
    def KnowBu(self):
        self.c.rerun(knownCard = True)
        if self.c.buttons == False:
            self.endScreen()
        else:
            self.viewedCard.configure(state = 'normal')
            self.setText(self.c.cardTerm)
            self.viewedCard.configure(state = 'disabled')
            pass

    def endScreen(self):
            self.viewedCard.configure(state = 'normal')
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
            self.viewedCard.configure(state = 'disabled')
    def notKnowBu(self):
        self.c.rerun(knownCard = False)
        self.viewedCard.configure(state = 'normal')
        if self.c.buttons == False:
            self.endScreen()
        else:
            self.viewedCard.configure(state = 'normal')
            self.setText(self.c.cardTerm)
            self.viewedCard.configure(state = 'disabled')
        pass

    def filpCardBu(self):
        self.viewedCard.configure(state = 'normal')
        if self.cardText == self.c.cardTerm:
            self.cardText = self.c.cardDef
            self.setText(self.cardText)
            self.viewedCard.configure(state = 'disabled')
            pass
        else:
            self.cardText = self.c.cardTerm
            self.setText(self.cardText)
            self.viewedCard.configure(state = 'disabled')
            pass
        self.viewedCard.configure(state = 'disabled')
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
    app = FlashcardsUiApp()
    app.run()



