from Tkinter import *
from ttk import *
from Tkconstants import *
from omg import *
from jdle_data import *
from views.idgamesui import *
import os.path
import omg.playpal
import tkFileDialog
import subprocess
from PIL import Image, ImageTk
import sys
import views.textlump
import views.imagelump


class App(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.geometry(SCREEN_SIZE)
        self.title(TITLE)
        self.create_frame()
        self.wad = WAD()
        self.lump_tree = None
        self.wad_name = ""
        self.create_tree()
        self.preview_panel = None
        self.create_preview_panel()
        self.wad_path = ""
        self.text_view = None

    def create_preview_panel(self, data=None, lump_type="None", lump_name="None"):
        if self.preview_panel is not None:
            self.preview_panel.destroy()
            
        if data is None:  # create the normal preview
            img = ImageTk.PhotoImage(Image.open(SPLASH_IMAGE))
            self.preview_panel = Label(self.frame, image=img)
            self.preview_panel.image = img
            stick = ""
        else:
            lump_detect_type = self.detect_lump(data, lump_type, lump_name)
            self.preview_panel = Label(self.frame, text="{0}\nLump type: {1}".format(NO_PREVIEW, lump_detect_type))
            stick = ""
            if lump_detect_type == "TEXT":
                self.preview_panel = views.textlump.TextLump(self.frame,data)
                stick="news"
            if lump_detect_type == "IMAGE":
                self.preview_panel = views.imagelump.ImageLump(self.frame,data)
                stick = ""

        self.preview_panel.grid(row=0, column=2, sticky=stick)
        self.frame.columnconfigure(2, weight=1)

    @staticmethod
    def detect_lump(data, lump_type, lump_name):
        text_lumps = ("DEHACKED", "MAPINFO", "ZMAPINFO", "EMAPINFO", "DECORATE",
                      "DMXGUS", "DMXGUSC")
        image_groups = ("flats", "patches", "sprites", "graphics")
        unique_lumps = ("PLAYPAL", "COLORMAP", "ENDOOM", "GENMIDI")
        if lump_name in text_lumps:
            return "TEXT"
        if lump_type in image_groups:
            return "IMAGE"
        if lump_type == "maps":
            return "MAP"
        if lump_name in unique_lumps:
            return lump_name
        if "DEMO" in lump_name:
            return "DEMO"
        return "{0}\nLump group: {1}".format(UNKNOWN_LUMP, lump_type)
        
    def create_frame(self):
        self.frame = Frame(self, width=640, height=480)
        self.frame.grid(sticky="NSWE")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        menubar = Menu(self.frame)
        menubar.add_command(label="Load", command=self.load_dialog)
        menubar.add_command(label="idgames", command=self.open_idgames)
        menubar.add_command(label="zdoom", command=self.load_in_zdoom)
        menubar.add_command(label="load test wad", command=self.load_test_wad)
        self.config(menu=menubar)
    
    def load_test_wad(self):
        self.wad_path = r'D:\Doom\IWADs\freedoom2.wad'
        self.load_wad(self.wad_path)
    
    def load_in_zdoom(self):
        subprocess.call(ZDOOM_PATH+" -file "+self.wad_path)
    
    def load_dialog(self):
        self.wad_path = tkFileDialog.askopenfilename(filetypes=[('wad files', "wad")])
        self.load_wad(self.wad_path)
    
    def open_idgames(self):
        IdgamesUI(None, self)
    
    def load_wad(self, path):
        
        try:
            self.wad = WAD(str(path))
        except AssertionError, AttributeError:
            Dialog(None, "Error loading file: {}".format(path))
            return
            
        self.title("JDLE - "+path)    
        if "/" in path:
            self.wad_name = path[path.rfind("/")+1:]
        else:
            self.wad_name = path[path.rfind("\\")+1:]
        self.create_tree()

    def create_tree(self):
    
        if self.lump_tree is not None:
            self.lump_tree.destroy()
        self.lump_tree = Treeview(self.frame)
        self.lump_tree.heading("#0", text=self.wad_name)
        # load groups
        for g in write_order:
            # write the groups
            new_g = self.lump_tree.insert('', len(write_order))
            self.lump_tree.item(new_g, text=g)
            for l in getattr(self.wad, g):
                # write lumps in groups
                new_l = self.lump_tree.insert(new_g, len(self.lump_tree.get_children(new_g)))
                self.lump_tree.item(new_l, text=l)
        
        self.lump_tree.width = 100
        
        ysb = Scrollbar(self.frame, orient='vertical', command=self.lump_tree.yview)
        self.lump_tree['yscroll'] = ysb.set
        
        self.lump_tree.grid(row=0, column=0, sticky='nsw')
        ysb.grid(row=0, column=1, sticky='nsw')
        self.frame.columnconfigure(0)
        self.frame.columnconfigure(1)
        self.frame.rowconfigure(0, weight=1)
        
        # event handling
        def on_select(event):
            cur_item_id = self.lump_tree.selection()[0]
            cur_item = self.lump_tree.item(self.lump_tree.selection()[0])
            if cur_item["text"] not in write_order:
                parent_id = self.lump_tree.parent(cur_item_id)
                parent_name = self.lump_tree.item(parent_id)["text"]
                lump_name = getattr(self.wad, parent_name)[cur_item["text"]]
                self.create_preview_panel(lump_name, parent_name, cur_item["text"])
        
        self.lump_tree.bind("<<TreeviewSelect>>", on_select)

        
class Dialog(Tk):
    def __init__(self, parent, text):
        Tk.__init__(self, parent)
        self.frame = Frame(self)
        self.frame.pack()
        self.label = Label(self.frame, text=text)
        self.label.pack()
        self.button = Button(self.frame, text="OK", command=self.close)
        self.button.pack()
    
    def close(self):
        self.destroy()


if __name__ == '__main__':
    app = App(None)
    if len(sys.argv) == 2:
        # load the argument as a wad
        app.load_wad(sys.argv[1])
    app.mainloop()
