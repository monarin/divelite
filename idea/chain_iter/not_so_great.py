class Step:
   def __init__(self,chunk_iter):
       self.chunk_iter = chunk_iter
   def events(self):
       for dg in self.chunk_iter:
           print('Step found dg',dg)
           if dg==102: return
           if dg<100: yield dg

class ChunkManager:
    def __init__(self):
        self.pos = 0
        self._chunks = [iter([101,1,2,3,102,101,4,5,102,101,6]),iter([7,8,102,101,9,10])]
        pass
    def chunks(self):
        while self.pos < len(self._chunks):
            self.pos += 1
            yield self._chunks[self.pos-1]


class Run:
   def __init__(self):
       pass
   def events(self):
       chunk_man = ChunkManager()
       for chunk_iter in chunk_man.chunks():
           for dg in chunk_iter:
               if dg<100: yield dg
   def steps(self):
       chunk_man = ChunkManager()
       for chunk_iter in chunk_man.chunks():
           for dg in chunk_iter:
               print('steps() found dg', dg)
               if dg==101: yield Step(chunk_iter)

if __name__ == "__main__":
    myrun = Run()

    #for evt in myrun.events():
    #    print(evt)                                                                                                                         
    for istep,step in enumerate(myrun.steps()):
       print('step:',istep)
       for evt in step.events():
           print(evt)
