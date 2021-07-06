import tkinter as tk
from PIL import ImageTk,Image

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("800x800")
        self.create_board()
        testMatrix = [[0,0,"Q",0,0,0],[0,0,0,0,0,"Q"],[0,"Q",0,0,0,0],[0,0,0,0,"Q",0],["Q",0,0,0,0,0],[0,0,0,"Q",0,0]]
        self.show_elements(testMatrix)

    def create_board(self):
        self.matriz = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
        icount=0
        jcount=0
        self.image1 = ImageTk.PhotoImage(Image.open("images/green.png"))
        self.image2 = ImageTk.PhotoImage(Image.open("images/white.png"))
        for i in self.matriz:
            for j in i:
                if (icount+jcount)%2 == 0:
                    self.matriz[icount][jcount] = tk.Label(image=self.image1)
                else:
                    self.matriz[icount][jcount] = tk.Label(image=self.image2)
                
                self.matriz[icount][jcount].pack()
                self.matriz[icount][jcount].place(x=jcount*100+100,y=icount*100+100,height=100, width=100)
                jcount +=1
            icount +=1
            jcount = 0

        
    def show_elements(self,show_matrix):
        self.matrix2 = show_matrix;
        icount=0
        jcount=0
        self.imagequeen = ImageTk.PhotoImage(Image.open("images/queen.png"))
        for i in self.matrix2:
            for j in i:
                if self.matrix2[icount][jcount] == "Q":
                    self.matrix2[icount][jcount] = tk.Label(image=self.imagequeen)
                else:
                    self.matrix2[icount][jcount] = tk.Label(self,text = self.matrix2[icount][jcount])
                
                self.matrix2[icount][jcount].pack()
                self.matrix2[icount][jcount].place(x=jcount*100+100,y=icount*100+100,height=100, width=100)
                jcount +=1
            icount +=1
            jcount = 0


    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)

app.mainloop()