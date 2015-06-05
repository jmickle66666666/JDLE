from Tkinter import *
from ttk import *
from Tkconstants import *
from omg import *
import tkFileDialog

class App(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.geometry("640x480")
        self.create_frame()
        self.wad = WAD()
        self.lump_tree = None
        self.wad_name = ""
        self.create_tree()
        
    def create_frame(self):
        self.frame = Frame(self, width=640, height=480)
        self.frame.pack(expand=True,fill=BOTH,anchor=W)
        self.button = Button(self.frame,text="Load",command=self.load_wad)
        self.button.pack(anchor=W)
    
    def load_wad(self):
        path = tkFileDialog.askopenfilename(filetypes=[('wad files',"wad")])
        self.wad = WAD(str(path))
        self.wad_name = path[path.rfind("/")+1:]
        self.create_tree()
    
    def create_tree(self):
    
        if (self.lump_tree != None):
            self.lump_tree.destroy()
        self.lump_tree = Treeview(self.frame)
        self.lump_tree.heading("#0",text=self.wad_name)
        #load groups
        for g in write_order:
            #write the groups
            new_g = self.lump_tree.insert('',0)
            self.lump_tree.item(new_g, text=g)
            for l in getattr(self.wad,g):
                #write lumps in groups
                new_l = self.lump_tree.insert(new_g,0)
                self.lump_tree.item(new_l,text=l)
        
        self.lump_tree.width = 100
        self.lump_tree.pack(anchor=W,fill=Y,expand=True,side=LEFT)
        
        
        
        
app = App(None)
app.mainloop()
