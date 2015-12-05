from six.moves.tkinter import *
from six.moves.tkinter_constants import *
from six.moves.tkinter_ttk import *
import utils.decorate
from PIL import ImageTk
import threading
import time


class DecorateUI(Frame):
    def __init__(self, parent, data, wad):
        Frame.__init__(self, parent)
        self.data = utils.decorate.Decorate(data)
        self.wad = wad
        self.anim_state = 0
        self.anim_thread = None
        self.anim_frame = 0
        
        self.actor_preview = Label(self, text="")
        
        self.actor_name = Label(self, text="")
        
        self.actor_list = Treeview(self)
        self.actor_list.heading("#0", text="Actor List")
        
        self.actor_code = Text(self)
        self.actor_code.configure(height=12)
        self.actor_code["wrap"] = NONE
        
        self.actor_states = Treeview(self)
        self.actor_states.heading("#0", text="States")
        
        self.actor_preview.grid(row=1, column=0, sticky="news")
        self.actor_name.grid(row=0, column=0, columnspan=2, sticky="news")
        self.actor_list.grid(row=0, column=2, rowspan=3, sticky="news")
        self.actor_code.grid(row=2, column=0, columnspan=2, sticky="ews")
        self.actor_states.grid(row=1, column=1, sticky="news")
        
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        
        self.build_actors()

    def build_actors(self):
        for a in self.data.actor_list:
            self.actor_list.insert('', len(self.actor_list.get_children('')), text=a.name)
            
        # event handling
        def on_select(event):
            cur_item = self.actor_list.item(self.actor_list.selection()[0])
            self.build_actor_view(self.data.get_actor(cur_item["text"]))
                
        self.actor_list.bind("<<TreeviewSelect>>", on_select)
    
    def build_actor_view(self, actor):
        self.actor_name.configure(text=actor.name)
        
        # build state tree
        if self.actor_states is not None:
            self.actor_states.destroy()
            
        self.actor_states = Treeview(self)
        self.actor_states.heading("#0", text="States")
        self.actor_states.grid(row=1, column=1, sticky="news")
        
        for s in actor.states:
            self.actor_states.insert('', len(self.actor_states.get_children('')), text=s.name)
        
        # state click event handling
        def state_select(event):
            cur_item = self.actor_states.item(self.actor_states.selection()[0])
            self.build_sprite_preview(actor, cur_item["text"])
                
        self.actor_states.bind("<<TreeviewSelect>>", state_select)
        
        # build code preview
        self.actor_code["state"] = NORMAL
        self.actor_code.delete(1.0, END)
        self.actor_code.insert(END, actor.code)
        self.actor_code["state"] = DISABLED
        
        self.build_sprite_preview(actor)
        
    def build_sprite_preview(self, actor, state=None):
        # build preview image
        lump_name = "n/a"
        lumps = []
        anim_speeds = [35 * 0.2]
        if len(actor.states) != 0:
            if state is None:
                frame = actor.states[0].frames[0]
                spr_name = frame.sprite + frame.frame
                
                for l in self.wad.sprites:
                    if spr_name in l:
                        lumps.append(l)
            else:
                st = actor.get_state(state)
                anim_speeds = []
                for f in st.frames:
                    for l in self.wad.sprites:
                        if f.sprite+f.frame in l:
                            lumps.append(l)
                            if f.tics != -1:
                                anim_speeds.append(f.tics)
                            else:
                                anim_speeds.append(35)
                            break
        
        if self.actor_preview is not None:
            self.actor_preview.destroy()

        self.anim_state = 0
        if self.anim_thread is not None:
            if self.anim_thread.is_alive():
                self.anim_thread.join()
                
        self.actor_preview = Label(self, text="No preview available")
                
        if len(lumps) > 0:
            self.animate(lumps,  anim_speeds)
        else: 
            self.anim_thread = None
            
        if lump_name != "n/a":
            image = self.wad.sprites[lump_name].to_Image()
            img = ImageTk.PhotoImage(image)
            self.actor_preview.configure(image=img, text="")
            self.actor_preview.image = img

        self.actor_preview.grid(row=1, column=0)
        
    def animate(self, lumps, anim_speeds):
        self.anim_frame = 0
        
        def async_latest():
            if self.anim_state == 1:
                self.anim_frame += 1
                image = self.wad.sprites[lumps[self.anim_frame % len(lumps)]].to_Image()
                img = ImageTk.PhotoImage(image)
                self.actor_preview.configure(image=img, text="")
                self.actor_preview.image = img
                time.sleep(anim_speeds[self.anim_frame % len(anim_speeds)]*0.029)
                self.anim_thread = threading.Thread(target=async_latest)
                self.anim_thread.start()
            
        self.anim_thread = threading.Thread(target=async_latest)
        self.anim_state = 1
        self.anim_thread.start()
