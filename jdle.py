from six.moves.tkinter_ttk import *
from six.moves import tkinter_tkfiledialog as tkFileDialog
from omg import *
from views.idgamesui import *
import subprocess
from PIL import Image, ImageTk, _imaging
import sys
import views.textlump
import views.imagelump
import views.settingsui
import views.decorateui


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
        self.preview_frame = None
        self.btn_grid = None
        self.btn_save = None
        self.btn_viewastext = None
        self.create_preview_panel()
        self.wad_path = ""
        self.text_view = None

    def create_preview_panel(self, data=None, lump_type="None", lump_name="None", force_view="None"):
        if self.preview_frame is None:
            self.preview_frame = Frame(self.frame)
            self.preview_frame.grid(row=0, column=2, sticky="news")
            self.frame.columnconfigure(2, weight=1)
            self.frame.rowconfigure(0, weight=1)
    
        if self.preview_panel is not None:
            self.preview_panel.destroy()
            
        if self.btn_grid is not None:
            self.btn_grid.destroy()
            
        if data is None:  # create a default preview
            img = ImageTk.PhotoImage(Image.open(SPLASH_IMAGE))
            self.preview_panel = Label(self.preview_frame, image=img)
            self.preview_panel.image = img
            stick = ""
        else:
            lump_detect_type = self.detect_lump(data, lump_type, lump_name)
            if force_view != "None":
                lump_detect_type = force_view
            self.preview_panel = Label(self.preview_frame, text="{0}\nLump type: {1}".format(NO_PREVIEW,
                                                                                             lump_detect_type))
            stick = ""
            if lump_detect_type == "TEXT":
                self.preview_panel = views.textlump.TextLump(self.preview_frame, data)
                stick = "news"
            if lump_detect_type == "IMAGE":
                self.preview_panel = views.imagelump.ImageLump(self.preview_frame, data)
                stick = "news"
            if lump_detect_type == "DECORATE":
                self.preview_panel = views.decorateui.DecorateUI(self.preview_frame, data, self.wad)
                stick = "news"
                
            # create buttons here
            def view_as_text():
                self.create_preview_panel(data, lump_type, lump_name, "TEXT")
            
            def save_data():
                save_lump = self.preview_panel.save_data()
                self.wad.data[lump_name] = save_lump
                self.create_preview_panel(self.wad.data[lump_name], lump_type, lump_name)
            
            self.btn_grid = Frame(self.preview_frame)
            self.btn_grid.grid(row=1, column=0, sticky="w")
            
            self.btn_viewastext = Button(self.btn_grid, text="View as text", command=view_as_text)
            if lump_detect_type == "TEXT":
                self.btn_viewastext.configure(state=DISABLED)
            self.btn_viewastext.grid(row=0, column=0, sticky="w")
                
            self.btn_save = Button(self.btn_grid,  text="Save", state=DISABLED)
            if hasattr(self.preview_panel, 'save_data'):
                self.btn_save.configure(state=NORMAL, command=save_data)
            self.btn_save.grid(row=0,  column=1, sticky="w")

        self.preview_panel.grid(row=0, column=0, sticky=stick)
        self.preview_frame.columnconfigure(0, weight=1)
        self.preview_frame.rowconfigure(0, weight=1)

    @staticmethod
    def detect_lump(data, lump_type, lump_name):
        text_lumps = ("DEHACKED", "MAPINFO", "ZMAPINFO", "EMAPINFO", 
                      "DMXGUS", "DMXGUSC", "WADINFO", "EMENUS", "MUSINFO",
                      "SNDINFO", "GLDEFS", "KEYCONF", "SCRIPTS", "LANGUAGE")
        image_groups = ("flats", "patches", "sprites", "graphics")
        unique_lumps = ("PLAYPAL", "COLORMAP", "ENDOOM", "GENMIDI", "DECORATE")
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
        # file menu
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", state=DISABLED)
        filemenu.add_command(label="Load", command=self.load_dialog)
        filemenu.add_command(label="Save", command=self.save_wad)
        filemenu.add_command(label="Quit", state=DISABLED)
        menubar.add_cascade(label="File", menu=filemenu)
        
        # stuff menu
        stuffmenu = Menu(menubar, tearoff=0)
        stuffmenu.add_command(label="idgames", command=self.open_idgames)
        stuffmenu.add_command(label="zdoom", command=self.load_in_zdoom)
        # stuffmenu.add_command(label="load test wad", command=self.load_test_wad)
        stuffmenu.add_command(label="settings", command=self.open_settings)
        menubar.add_cascade(label="Stuff", menu=stuffmenu)

        self.config(menu=menubar)
    
    def save_wad(self):
        self.wad.to_file(tkFileDialog.asksaveasfilename())
    
    def load_test_wad(self):
        self.wad_path = r'D:\Doom\wads\valiant_final.wad'
        self.load_wad(self.wad_path)
    
    def load_in_zdoom(self):
        subprocess.call(ZDOOM_PATH+" -file "+self.wad_path)
    
    def load_dialog(self):
        self.wad_path = tkFileDialog.askopenfilename(filetypes=[('wad files', "wad")])
        self.load_wad(self.wad_path)
    
    def open_idgames(self):
        IdgamesUI(None, self)
        
    def open_settings(self):
        views.settingsui.SettingsUI(None)
    
    def load_wad(self, path):
        
        try:
            self.wad = WAD(str(path))
        except AssertionError:
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
