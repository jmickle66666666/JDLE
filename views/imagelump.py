from six.moves.tkinter import *
from PIL import Image, ImageTk

class ImageLump(Frame):
    def __init__(self, parent, data):
        Frame.__init__(self, parent)
        
        self.image = data.to_Image()
        self.img = ImageTk.PhotoImage(self.image)
        self.label = Label(self, image=self.img)
        self.label.image = self.img
        self.label.grid(row=0, column=0, sticky="news")
        self.scale = 1
        
        self.button_frame = Frame(self)
        self.button_frame.grid(row=1,column=0,sticky="sw")
        
        self.btn_scaleup = Button(self.button_frame, text="+", command=self.scale_up)
        self.btn_scaledown = Button(self.button_frame, text="-", command=self.scale_down)
        self.btn_scaleup.grid(row=0, column=0, sticky="sw")
        self.btn_scaledown.grid(row=0, column=1, sticky="sw")
        
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        
    def scale_up(self):
        self.scale += 1
        self.image = self.image.resize((self.image.size[0]*2,  self.image.size[1]*2))
        self.reload_image()
        
    def scale_down(self):
        if self.scale > 1:
            self.scale -= 1
            self.image = self.image.resize((self.image.size[0]/2, self.image.size[1]/2))
            self.reload_image()
            
    def reload_image(self):
        self.label.destroy()
        self.img = ImageTk.PhotoImage(self.image)
        self.label = Label(self, image=self.img)
        self.label.image = self.img
        self.label.grid(row=0, column=0, sticky="news")
    
if __name__ == '__main__':
    import omg
    test_data = omg.Graphic()
    test_data.from_Image(Image.new("RGB", (128, 128)))
    app = Tk(None)
    ImageLump(app, test_data).grid(sticky="")
    app.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=1)
    app.mainloop()
