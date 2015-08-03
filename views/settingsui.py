from Tkinter import *


class SettingsUI(Tk):
    def __init__(self,  parent):
        Tk.__init__(self,  parent)
        options = ["screen_size", "zdoom_path"]
        for i in range(len(options)):
            o = options[i]
            label = Label(self, text=o)
            label.grid(row=i, column=0)
            textfield = Text(self)
            textfield.configure(height=1, width=20)
            textfield.grid(row=i, column=1)
        btn_done = Button(self, text="Done")
        btn_done.grid(row=len(options), column=1, sticky="e", command=self.save_settings())
    
    # def save_settings(self):
        
        
if __name__ == '__main__':
    
    app = Tk(None)
    SettingsUI(app).grid(sticky="news")
    app.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=1)
    app.mainloop()