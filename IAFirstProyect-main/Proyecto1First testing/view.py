import tkinter as tk
from PIL import ImageTk,Image

class Application(tk.Frame):
    def __init__(self, master=None,Matrix=[],open_nodes = [],close_nodes = []):
        super().__init__(master)
        self.master = master
        self.master.geometry("800x800")
        self.init_Board()
        self.keyboard_list = Matrix
        self.open_nodes = open_nodes;
        self.close_nodes = close_nodes;
        self.pos_to_show = 0
        self.show_Elements()
        self.show_Matrix()
        self.show_Closed_Nodes()
        self.show_Open_Nodes()
        self.show_Buttoms()

    def init_Board(self):
        #load images
        self.image_green = ImageTk.PhotoImage(Image.open("images/green.png"))
        self.image_white = ImageTk.PhotoImage(Image.open("images/white.png"))
        self.image_green_queen = ImageTk.PhotoImage(Image.open("images/green_queen.png"))
        self.image_white_queen = ImageTk.PhotoImage(Image.open("images/white_queen.png"))
        self.image_open_node = ImageTk.PhotoImage(Image.open("images/open_node.png"))
        self.image_close_node = ImageTk.PhotoImage(Image.open("images/close_node.png"))

        #set default values
        self.matrix_state_of_nodes = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]];
        self.matrix_value_of_nodes = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]];
        self.matrix2 = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]];
        self.matrix_size = 6
        
        icount=0
        jcount=0
        #create initial board
        for i in self.matrix2:
            for j in i:
                if ((icount+jcount)%2 == 0):
                    self.matrix2[icount][jcount] = tk.Label(image=self.image_green)
                else:
                    self.matrix2[icount][jcount] = tk.Label(image=self.image_white)
                self.matrix2[icount][jcount].pack()
                self.matrix2[icount][jcount].place(x=jcount*100+100,y=icount*100+100,height=100, width=80)
                
                self.matrix_state_of_nodes[icount][jcount] = tk.Label(image = self.image_open_node)
                self.matrix_state_of_nodes[icount][jcount].pack()
                self.matrix_state_of_nodes[icount][jcount].place(x=jcount*100+180,y=icount*100+100,height=33, width=20)
                
                jcount +=1
            icount +=1
            jcount = 0

        
    def show_Elements(self):
        icount=0
        jcount=0
        print("keyboard_list", self.keyboard_list[self.pos_to_show])
        for i in self.keyboard_list[self.pos_to_show]:
            for j in i:
                if (self.keyboard_list[self.pos_to_show][icount][jcount] == "Q") and ((icount+jcount)%2 == 0):
                    self.matrix2[icount][jcount].configure(image=self.image_green_queen)
                elif (self.keyboard_list[self.pos_to_show][icount][jcount] == "Q") and ((icount+jcount)%2 == 1):
                    self.matrix2[icount][jcount].configure(image=self.image_white_queen)
                elif (icount+jcount)%2 == 0:
                    self.matrix2[icount][jcount].configure(image=self.image_green)
                else:
                    self.matrix2[icount][jcount].configure(image=self.image_white)
                
                self.matrix2[icount][jcount].pack()
                self.matrix2[icount][jcount].place(x=jcount*100+100,y=icount*100+100,height=100, width=80)
                jcount +=1
            icount +=1
            jcount = 0

    def show_Open_Nodes(self):
        print("value of closed nodes",self.open_nodes[self.pos_to_show])
        for i in self.open_nodes[self.pos_to_show]:
                x = (i-1) % self.matrix_size
                y = (i-1) // self.matrix_size
               
                self.matrix_state_of_nodes[x][y].configure(image = self.image_open_node)
                self.matrix_state_of_nodes[x][y].pack()
                self.matrix_state_of_nodes[x][y].place(x=x*100+180,y=y*100+100,height=33, width=20)

    def show_Closed_Nodes(self):
        print("value of closed nodes",self.close_nodes[self.pos_to_show])
        for i in self.close_nodes[self.pos_to_show]:
                x = (i-1) % self.matrix_size
                y = (i-1) // self.matrix_size

                self.matrix_state_of_nodes[x][y].configure(image = self.image_close_node)
                self.matrix_state_of_nodes[x][y].pack()
                self.matrix_state_of_nodes[x][y].place(x=x*100+180,y=y*100+166,height=33, width=20)

    def show_Matrix(self):
        
        cont = 0
        print(self.keyboard_list[self.pos_to_show])
        print(self.keyboard_list[self.pos_to_show][0])
        for i in self.keyboard_list[self.pos_to_show]:
            for j in i:
                x = cont % self.matrix_size
                y = cont // self.matrix_size
                tk.Label(image=self.image_open_node)
                self.matrix_value_of_nodes[x][y] = tk.Label(text = str(j))
                self.matrix_value_of_nodes[x][y].pack()
                self.matrix_value_of_nodes[x][y].place(x=x*100+180,y=y*100+133,height=33, width=20)
                cont += 1

    def show_Next(self):
        self.pos_to_show += 1;
        if(self.pos_to_show == len(self.keyboard_list)):
            self.pos_to_show -= 1;
        else:
            self.show_Elements()
            self.show_Matrix()
            self.show_Closed_Nodes()
            self.show_Open_Nodes()

    def show_Buttoms(self):
        self.button_next = tk.Button( text ="Next", command = self.show_Next);
        self.button_next.pack();
        self.button_next.place(x=400,y=50,height=33, width=70);
            


