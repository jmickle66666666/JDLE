import threading
import utils.idgames as idgames
import requests
from tkinter import *
from jdle_data import *
import random
import zipfile


class IdgamesWadUI(Tk):
    def __init__(self, parent, idgamesui, wad_json):
        Tk.__init__(self, parent)
        self.geometry(IDGAMES_WAD_SCREEN_SIZE)
        self.data = wad_json["content"]
        self.title(self.data["filename"])
        self.idgamesui = idgamesui
        self.build_ui()
        self.title_label = None
        self.author_label = None
        self.date_label = None
        self.size_label = None
        self.description_label = None
        self.title_content = None
        self.author_content = None
        self.date_content = None
        self.size_content = None
        self.description_text = None
        self.open_button = None
        self.download_button = None
        
    def build_ui(self):
        self.frame = Frame(self)
        self.frame.pack(fill="both", expand=True)
        self.title_label = Label(self.frame, text="Title:")
        self.title_label.grid(row=0, column=0)
        self.author_label = Label(self.frame, text="Author:")
        self.author_label.grid(row=1, column=0)
        self.date_label = Label(self.frame, text="Label:")
        self.date_label.grid(row=2, column=0)
        self.size_label = Label(self.frame, text="Size:")
        self.size_label.grid(row=3, column=0)
        self.description_label = Label(self.frame, text="Description:")
        self.description_label.grid(row=4, column=0)
        
        self.title_content = Label(self.frame, text=self.data["title"])
        self.title_content.grid(row=0, column=1, sticky="w")
        self.author_content = Label(self.frame, text=self.data["author"])
        self.author_content.grid(row=1, column=1, sticky="w")
        self.date_content = Label(self.frame, text=self.data["date"])
        self.date_content.grid(row=2, column=1, sticky="w")
        self.size_content = Label(self.frame, text=self.data["size"])
        self.size_content.grid(row=3, column=1, sticky="w")
        self.description_text = Text(self.frame)
        self.description_text.insert("end", self.data["description"])
        self.description_text.grid(row=5, column=0, columnspan=2, sticky="news")
        
        if os.path.exists(JDLE_DIR+"/download/"+self.data["filename"]):
            self.open_button = Button(self.frame, text="Open", command=self.open_wad)
            self.open_button.grid(row=6, column=0, sticky="ws")
        else:
            self.download_button = Button(self.frame, text="Download", command=self.download_wad)
            self.download_button.grid(row=6, column=0, sticky="ws")
        
        self.frame.rowconfigure(5, weight=1)
        self.frame.columnconfigure(1, weight=1)
        
    def open_wad(self):
        path = JDLE_DIR + "/download/" + self.data["filename"]
        zf = zipfile.ZipFile(path, "r")
        wadfile = ""
        for zf_f in zf.namelist():
            if ".WAD" in zf_f:
                wadfile = zf_f
            if ".wad" in zf_f:
                wadfile = zf_f
        print(wadfile)
        wadpath = zf.extract(wadfile, JDLE_DIR+"/download/")
        zf.close()
        self.idgamesui.main_ui.wadpath = wadpath
        self.idgamesui.main_ui.load_wad(wadpath)
        self.idgamesui.destroy()
        self.destroy()

    def download_wad(self):
        url = IDGAMES_MIRROR_URL + self.data["dir"] + self.data["filename"]
        print(url)
        r = requests.get(url)
        if os.path.isdir(JDLE_DIR + "/download" is False):
            os.makedirs(JDLE_DIR + "/download")
        write_f = open(JDLE_DIR + "/download/" + self.data["filename"], "wb")
        write_f.write(r.content)
        write_f.close()
        print("done")
        self.open_wad()


class IdgamesUI(Tk):
    def __init__(self, parent, main_ui):
        Tk.__init__(self, parent)
        self.geometry(IDGAMES_SCREEN_SIZE)
        self.title(IDGAMES_TITLE)
        self.main_ui = main_ui
        self.result_data = None
        self.last_value = ""
        self.search_bar = None
        self.search_button = None
        self.random_button = None
        self.innerframe = None
        self.results_box = None
        self.results_box_yscroll = None
        self.build_ui()
        self.load_latest()
    
    def load_latest(self):
        
        def async_latest():
            data = idgames.latest_files(limit=15)
            self.results_box.delete(0, "end")
            self.result_data = {}
            for file_data in data["content"]["file"]:
                self.results_box.insert("end", file_data["title"])
                self.result_data[file_data["title"]] = file_data["id"]
            
        self.results_box.delete(0, "end")
        self.results_box.insert("end", "Loading latest files...")
        
        t = threading.Thread(target=async_latest)
        t.start()
        
    def idgames_search(self):
        
        def async_search():
            data = idgames.search(self.search_bar.get())
            self.results_box.delete(0, "end")
            if data["content"]["file"] is list:
                self.result_data = {}
                for file_data in data["content"]["file"]:
                    self.results_box.insert("end", file_data["title"])
                    self.result_data[file_data["title"]] = file_data["id"]
            else:
                self.results_box.insert("end", data["content"]["file"]["title"])
                self.result_data = {}
                self.result_data[data["content"]["file"]["title"]] = data["content"]["file"]["id"]
                
        self.results_box.delete(0, "end")
        self.results_box.insert("end", "Searching for {0}...".format(self.search_bar.get()))
        
        t = threading.Thread(target=async_search)
        t.start()
    
    def on_result_click(self, event):
        w = event.widget
        index = w.curselection()[0]
        value = w.get(index)
        if value == self.last_value:
            IdgamesWadUI(None, self, idgames.get(id=self.result_data[value]))
        else:
            self.last_value = value
    
    def random_wad(self):
        data = idgames.latest_files(limit=1)
        lastid = data["content"]["file"]["id"]
        randid = random.randrange(lastid)
        IdgamesWadUI(None, self, idgames.get(id=randid))
    
    def build_ui(self):
        self.frame = Frame(self, width=640, height=480)
        self.frame.pack(fill="both", expand=True)
        
        self.search_bar = Entry(self.frame)
        self.search_bar.grid(row=0, column=0, sticky="EW")
        
        self.search_button = Button(self.frame, text="Search", command=self.idgames_search)
        self.search_button.grid(row=0, column=1, sticky="E")
        
        self.random_button = Button(self.frame, text="Random!", command=self.random_wad)
        self.random_button.grid(row=0, column=2, sticky="E")
        
        self.innerframe = Frame(self.frame)
        self.innerframe.grid(row=1, column=0, columnspan=3, sticky="nsew")
        
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        
        self.results_box = Listbox(self.innerframe)
        self.results_box.grid(row=0, column=0, sticky="nsew")
        
        self.results_box_yscroll = Scrollbar(self.innerframe, orient='vertical', command=self.results_box.yview)
        self.results_box['yscroll'] = self.results_box_yscroll.set
        self.results_box_yscroll.grid(row=0, column=1, sticky="nsew")
        
        self.innerframe.columnconfigure(0, weight=1)
        self.innerframe.rowconfigure(0, weight=1)
        
        self.results_box.bind("<<ListboxSelect>>", self.on_result_click)
