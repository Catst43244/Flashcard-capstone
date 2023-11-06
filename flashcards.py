import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import random as ra
from playsound import playsound
import threading
def playSoundFun():
    playsound("walking-on-a-wooden-floor-32056.mp3")
class cards:
    MISSED_COUNTER_WARNING_SOUND = 2
    MISSED_COUNTER_GAME_OVER = 4
    def __init__(self):
        self.remove = []
        self.missed = []
        #might be a problem. repeat idems
        self.data = pd.read_excel('database.xlsx')
        self.termsLeft = self.data['TERMS'].values.tolist() 
        #problem: t in terms left should not be capitatilized       
        self.POS = ra.randrange(0,len(self.data))
        self.card = self.data.iloc[self.POS]
        self.cardTerm = str(self.card.loc["TERMS"])
        self.cardDef = str(self.card.loc["DEF"])
        self.buttons = True
        self.debug1 = input("debug on or off")
        #problem: have a var that takes the input into true and false 
        self.debug = self.debug1.upper()
        self.missedCounter = 0
        
    def rerun(self,knownCard = False):
        if self.debug == "ON":
            print("current position")
            print(self.POS)
            print("the current term is")
            print(self.cardTerm)
            print("and the answer is")
            print(self.cardDef)
            print("currently in remove")
            print(self.remove)
        if knownCard == True:
            self.remove.append(self.POS)
            if self.debug == "ON":
                print("this position shouldn't show up again")
                print(self.POS)
        if knownCard == False:
            if self.POS != self.missed:
                self.missed.append(self.POS)
            self.missedCounter += 1
            match self.missedCounter:
                case cards.MISSED_COUNTER_WARNING_SOUND:
                    download_thread = threading.Thread(target=playSoundFun, name="Downloader")
                    download_thread.start()
                    print("Playsound")
                case cards.MISSED_COUNTER_GAME_OVER:
                    print("GAME OVER")
        self.lastPOS = self.POS
        self.POS = ra.randrange(0,len(self.termsLeft))
        if self.debug == "ON":
            print("new position #1")
            print(self.POS)
        if self.POS in self.remove:
            if self.debug == "ON":
                print("current position is in remove. will pick a different number")
            while self.POS in self.remove:
                self.POS = ra.randrange(0,len(self.termsLeft))
                if len(self.remove) >= len(self.termsLeft):
                    if self.debug == "ON":
                        print("all positions are in remove")
                        #error: can go over terms left which should not be possable
                    self.buttons = False
                    break
        if self.POS == self.lastPOS:
            if self.debug == "ON":
                print("the new position can't be the same as the last.will pick a different number")
            self.rerun()
            pass
        self.card = self.data.iloc[self.POS]
        self.cardTerm = str(self.card.loc["TERMS"])
        self.cardDef = str(self.card.loc["DEF"])
        if self.debug == "ON":
            print("new position. final number")
            print(self.POS)
            print("the term is")
            print(self.cardTerm)
            print("and the answer is")
            print(self.cardDef)
            print("missed counter/list")
            print(self.missedCounter)
            print(self.missed)
            print("END OF CARDS")
            print("________________________")
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
        if self.c.buttons == False:
            self.viewedCard.configure(state = 'normal')
            summaryText = "all cards studied. Here's what you got wrong and their answers"
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
        else:
            self.viewedCard.configure(state = 'normal')
            self.c.rerun(knownCard = True)
            self.setText(self.c.cardTerm)
            self.viewedCard.configure(state = 'disabled')
            pass


    def notKnowBu(self):
        self.viewedCard.configure(state = 'normal')
        self.c.rerun(knownCard = False)
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



