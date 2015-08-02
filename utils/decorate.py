class Decorate:
    def __init__(self, decorate):
        self.code = decorate.data.split("\n")
        self.actor_list = []
        self.parse_actors()
        
    def parse_actors(self):
        for l in self.code:
            if l.find("ACTOR") == 0:
                rem_ac = l[6:]
                name = rem_ac[:rem_ac.find(" ")]
                
                actor = Actor(name)
                # find end of actor code
                p = self.code.index(l)
                q = p
                while self.code[q][0] != "}":
                    q+=1
                actor.states = self.parse_states(self.code.index(l),q+1)
                actor.code = "\n".join(self.code[p:q+1])
                
                self.actor_list.append(actor)
                # actor.p()
            
    def parse_states(self,actor_code_start,actor_code_end):
        output = []
            
        i = actor_code_start
        while "States" not in self.code[i]:
            i += 1
            
        for p in range(i,actor_code_end):
            if ":" in self.code[p]:
                statename = self.code[p][:len(self.code[p])-2]
                while ord(statename[0]) == 32 or ord(statename[0]) == 9:
                    statename = statename[1:]
                
                q = p+1 #look for end of state
                while ":" not in self.code[q] and "}" not in self.code[q]:
                    q += 1
                    if q == actor_code_end: 
                        break
                
                output.append(self.parse_state(statename,p,q-1))
        
        return output
        
    def parse_state(self,name,state_start,state_end):
        state = State(name)
        for i in range(state_start+1,state_end):
            line = self.code[i]
            # parse out spaces and tabs
            while ord(line[0]) == 32 or ord(line[0]) == 9:
                line = line[1:]
                
            ldat = line.split(' ')
            if (len(ldat) >= 3):
                spritename = ldat[0]
                spriteframes = ldat[1]
                spritetics = ldat[2]
            
                for f in spriteframes:
                    state.frames.append(Frame(spritename,f,spritetics))
        return state
        
    def get_actor(self,name):
        for a in self.actor_list:
            if (a.name == name): 
                return a
                break
        
class Actor:
    def __init__(self,name):
        self.name = name
        self.states = []
        self.code = ""
        
    def p(self):
        print self.name
        for s in self.states:
            s.p()
            
    def get_state(self,name):
        for s in self.states:
            if (s.name == name):
                return s
                break
    
class State:
    def __init__(self,name):
        self.name = name
        self.frames = []
        
    def p(self):
        print(self.name)
        for f in self.frames:
            f.p()
    
class Frame:
    def __init__(self,sprite,frame,tics):
        self.sprite = sprite
        self.frame = frame
        self.tics = int(tics)
        
    def p(self):
        print '  {} {} {}'.format(self.sprite,self.frame,self.tics)
        
    
    
if __name__ == '__main__':
    test_wad = r'D:\Doom\wads\valiant_final.wad'
    import omg
    wad = omg.WAD(test_wad)
    dcode = wad.data["DECORATE"]
    dec = Decorate(dcode)