import tkinter as tk
import tkinter.font as tkFont

class Ui:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=1200
        height=700
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
        self.viewedCard.configure(state = 'disabled')

    def notKnowBu(self):
        print("no know")


    def KnowBu(self):
        print("KNOW")


    def filpCardBu(self):
        print("FLIP")
        self.filpCardButton.place_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = Ui(root)
    root.mainloop()
