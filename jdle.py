print("jdle.py")
from Tkinter import *
from ttk import *
from Tkconstants import *
from omg import *
import tkFileDialog

class App(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.create_frame()
        self.wad = WAD()
        self.lump_tree = None
        self.create_tree()
        
    def create_frame(self):
        self.frame = Frame(self)
        self.frame.pack(fill=BOTH,expand=1)
        self.button = Button(self.frame,text="Load",command=self.load_wad)
        self.button.pack(side=TOP)
    
    def load_wad(self):
        path = tkFileDialog.askopenfilename()
        self.wad = WAD(str(path))
        self.create_tree()
    
    def create_tree(self):
    
        if (self.lump_tree != None):
            self.lump_tree.destroy()
        self.lump_tree = Treeview()
        print(write_order)  
        #load flats
        for g in write_order:
            #write the groups
            print(g)
            new_g = self.lump_tree.insert('',0)
            self.lump_tree.item(new_g, text=g)
            for l in getattr(self.wad,g):
                new_l = self.lump_tree.insert(new_g,0)
                self.lump_tree.item(new_l,text=l)
        
        self.lump_tree.height=999
        self.lump_tree.pack(side=TOP,fill=BOTH,expand=True)
        
        
        
        
app = App(None)
app.mainloop()