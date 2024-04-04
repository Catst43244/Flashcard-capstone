import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import pandas as pd
import random as ra
from playsound import playsound
import threading
def playSoundFun():
    playsound("walking.mp3")
def gameOverSound():
    playsound("jumpscare.mp3")
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


class Ui:
    def __init__(self, window):
        self.c = cards()
        self.displaySwitch = False
        #setting title
        window.title("Horror Flashcards")
        #setting window size
        width=1200
        height=700
        screenwidth = window.winfo_screenwidth()
        screenheight = window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        window.geometry(alignstr)
        window.resizable(width=False, height=False)
        window.configure(bg = "#4e4f4f")

        self.knowButton=tk.Button(window)
        self.knowButton["anchor"] = "center"
        self.knowButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=16)
        self.knowButton["font"] = ft
        self.knowButton["fg"] = "#000000"
        self.knowButton["justify"] = "center"
        self.knowButton["text"] = "I know this one"
        self.knowButton.place(x=390,y=530,width=403,height=152)
        self.knowButton["command"] = self.KnowBu

        self.notKnowButton=tk.Button(window)
        self.notKnowButton["anchor"] = "center"
        self.notKnowButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=16)
        self.notKnowButton["font"] = ft
        self.notKnowButton["fg"] = "#000000"
        self.notKnowButton["justify"] = "center"
        self.notKnowButton["text"] = "I don't know"
        self.notKnowButton.place(x=390,y=380,width=403,height=146)
        self.notKnowButton["command"] = self.notKnowBu

        self.viewedCard = tk.Text(window)
        self.viewedCard["borderwidth"] = "1px"
        self.viewedCard["cursor"] = "arrow"
        ft = tkFont.Font(family='Times',size=23)
        self.viewedCard["font"] = ft
        self.viewedCard["fg"] = "#333333"
        self.viewedCard["bg"] = "#6b6c6e"
        self.viewedCard.place(x=20,y=30,width=1153,height=331)
        self.viewedCard.tag_configure("center", justify='center')
        self.viewedCard.config(wrap=tk.WORD)

        self.flipCardButton=tk.Button(window)
        self.flipCardButton["anchor"] = "center"
        self.flipCardButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=14)
        self.flipCardButton["font"] = ft
        self.flipCardButton["fg"] = "#000000"
        self.flipCardButton["justify"] = "center"
        self.flipCardButton["text"] = "Flip"
        self.flipCardButton.place(x=460,y=270,width=264,height=73)
        self.flipCardButton["command"] = self.flipCardBu
        self.setText(self.c.cardTerm)
        
        self.restartButton=tk.Button(window)
        self.restartButton["bg"] = "#e9e9ed"
        ft = tkFont.Font(family='Times',size=16)
        self.restartButton["font"] = ft
        self.restartButton["fg"] = "#000000"
        self.restartButton["justify"] = "center"
        self.restartButton["text"] = "Restart"
        self.restartButton.place(x=390,y=380,width=403,height=146)
        self.restartButton["command"] = self.restartBu
        self.restartButton.place_forget()

    def run(self):
        self.mainwindow.mainloop()
    def setText(self,Text):
        self.viewedCard.configure(state = 'normal')
        self.viewedCard.delete("1.0", "end")
        self.viewedCard.insert("1.0", Text)
        self.viewedCard.tag_add("center", "1.0", "end")
        self.viewedCard.configure(state = 'disabled')
        pass
    def KnowBu(self):
        self.c.rerun(knownCard = True)
        if self.c.buttons == False:
            self.endScreen()
        else:
            self.setText(self.c.cardTerm)
            self.displaySwitch = False
            pass

    def endScreen(self):
            summaryText = "All cards studied. Here's what you got wrong and their answers"
            if self.c.GAMEOVER == True:
                summaryText = "GAMEOVER. Here's why"
            for missedCardPOS in self.c.missed:
                card = self.c.data.iloc[missedCardPOS]
                cardTerm = str(card.loc["TERMS"])
                cardDef = str(card.loc["DEF"])
                summaryText = summaryText + "\n\n" + cardTerm + "\nwas\n" + cardDef
            if len(self.c.missed) == 0:
                summaryText = "It didn't see you"
            self.setText(summaryText)
            self.flipCardButton.place_forget()
            self.notKnowButton.place_forget()
            self.knowButton.place_forget()
            self.restartButton.place(x=390,y=380,width=403,height=146)

    def notKnowBu(self):
        self.c.rerun(knownCard = False)
        if self.c.buttons == False:
            self.endScreen()
        else:
            self.setText(self.c.cardTerm)
            self.displaySwitch = False
            pass

    def flipCardBu(self):
        if self.displaySwitch == False:
            self.setText(self.c.cardDef)
            self.displaySwitch = True
            pass
        else:
            self.setText(self.c.cardTerm)
            self.displaySwitch = False
            pass
        pass
    def restartBu(self):
        self.c.remove = []
        self.c.missed = []
        self.c.data = pd.read_excel('database.xlsx')
        self.c.termsLeft = self.c.data['TERMS'].values.tolist()      
        self.c.POS = ra.randrange(0,len(self.c.data))
        self.c.card = self.c.data.iloc[self.c.POS]
        self.c.cardTerm = str(self.c.card.loc["TERMS"])
        self.c.cardDef = str(self.c.card.loc["DEF"])
        self.c.buttons = True
        self.c.missedCounter = 0
        self.c.GAMEOVER = False
        self.c.playWarningSoundThread = threading.Thread(target=playSoundFun, name="Playsound")
        self.c.playGameOverSoundThread = threading.Thread(target=gameOverSound, name="Playsound")
        self.c.playWarningSoundThread.daemon = True
        self.c.playGameOverSoundThread.daemon = True
        #I need a funtion for this

        self.displaySwitch = False
        self.c.rerun(knownCard = False)
        self.setText(self.c.cardTerm)
        self.restartButton.place_forget()
        self.flipCardButton.place(x=460,y=270,width=264,height=73)
        self.notKnowButton.place(x=390,y=380,width=403,height=146)
        self.knowButton.place(x=390,y=530,width=403,height=152)




if __name__ == "__main__":
    window = tk.Tk()
    app = Ui(window)
    window.mainloop()
