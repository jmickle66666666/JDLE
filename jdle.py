from Tkinter import *
from ttk import *
from Tkconstants import *
from omg import *
import tkFileDialog

class App(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.geometry("640x480")
        self.title("JDLE")
        self.create_frame()
        self.wad = WAD()
        self.lump_tree = None
        self.wad_name = ""
        self.create_tree()
        self.preview_panel = None
        self.create_preview_panel()
        
    def create_preview_panel(self):
        if (self.preview_panel != None):
            self.preview_panel.destroy()
        self.preview_panel = Frame(self.frame,background='#ff0000')
        self.preview_panel.grid(row=0,column=2,sticky="nse")
        self.preview_panel.bg="#f00"
        self.frame.columnconfigure(2,weight=1)
        self.frame.rowconfigure(0,weight=1)
        
        
    def create_frame(self):
        self.frame = Frame(self, width=640, height=480)
        self.frame.grid(sticky="NSW")
        #self.frame.pack(expand=True,fill=BOTH,anchor=W)
        #self.button = Button(self.frame,text="Load",command=self.load_wad)
        #self.button.grid()
        #self.button.pack(anchor=W)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        menubar = Menu(self.frame)
        menubar.add_command(label="Load", command=self.load_wad)
        self.config(menu=menubar)
    
    def load_wad(self):
        path = tkFileDialog.askopenfilename(filetypes=[('wad files',"wad")])
        self.title("JDLE - "+path)
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
            new_g = self.lump_tree.insert('',len(write_order))
            self.lump_tree.item(new_g, text=g)
            for l in getattr(self.wad,g):
                #write lumps in groups
                new_l = self.lump_tree.insert(new_g,len(self.lump_tree.get_children(new_g)))
                self.lump_tree.item(new_l,text=l)
        
        self.lump_tree.width = 100
        
        ysb = Scrollbar(self.frame,orient='vertical', command=self.lump_tree.yview)
        self.lump_tree['yscroll'] = ysb.set
        
        
        self.lump_tree.grid(row=0,column=0,sticky='nsw')
        ysb.grid(row=0,column=1,sticky='nsw')
        self.frame.columnconfigure(0,weight=1)
        self.frame.columnconfigure(1,weight=1)
        self.frame.rowconfigure(0,weight=1)
        
        #self.lump_tree.pack(anchor=W,fill=Y,expand=True,side=LEFT)
        
        
        
        
app = App(None)
app.mainloop()
