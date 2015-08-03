from Tkinter import *
from Tkconstants import *
import omg


class TextLump(Frame):
    def __init__(self, parent, data):
        Frame.__init__(self, parent)
        self.text_view = Text(self)
        self.text_view.insert(END, data.data)
        # self.text_view["state"] = DISABLED
        self.text_view["wrap"] = NONE
        self.text_view.grid(sticky="NEWS")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        ysb = Scrollbar(self, orient='vertical', command=self.text_view.yview)
        hsb = Scrollbar(self, orient='horizontal', command=self.text_view.xview)
        self.text_view['yscroll'] = ysb.set
        self.text_view['xscroll'] = hsb.set
        ysb.grid(row=0, column=1, sticky="NS")
        hsb.grid(row=1, column=0, sticky="EW")
        
    def save_data(self):
        output_lump = omg.Lump(self.text_view.get(1.0, END))
        return output_lump
            
if __name__ == '__main__':
    class TestData:
        def __init__(self):
            self.data = "Fart Fart Fart\nfart\n"
    app = Tk(None)
    TextLump(app, TestData()).grid(sticky="news")
    app.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=1)
    app.mainloop()
