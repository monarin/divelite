class Step:
   def __init__(self,chunk_man):
       self.chunk_man = chunk_man
   def events(self):
       while self.chunk_man.has_more():
           print(f'events() chunk_man.get()')
           chunk_iter = self.chunk_man.get()
           for dg in chunk_iter:
               if dg==102: return
               if dg<100: yield dg
           self.chunk_man.next()

class ChunkManager:
    def __init__(self):
        self.pos = 0
        self._chunks = [iter([101,1,2,3,102,101,4,5,102,101,6]),iter([7,8,102,101,9,10])]
    def has_more(self):
        if self.pos <= len(self._chunks) - 1:
            return True
        else:
            return False
    def get(self):
        return self._chunks[self.pos]
    def next(self):
        self.pos += 1


class Run:
   def __init__(self):
       pass
   def events(self):
       chunk_man = ChunkManager()
       for chunk_iter in chunk_man:
           for dg in chunk_iter:
               if dg<100: yield dg
   def steps(self):
       chunk_man = ChunkManager()
       while chunk_man.has_more():
           print(f'steps() chunk_man.get()')
           chunk_iter = chunk_man.get()
           for dg in chunk_iter:
               if dg==101: yield Step(chunk_man)

if __name__ == "__main__":
    myrun = Run()

    #for evt in myrun.events():
    #    print(evt)                                                                                                                         
    for istep,step in enumerate(myrun.steps()):
       print('step:',istep)
       for evt in step.events():
           print(evt)
