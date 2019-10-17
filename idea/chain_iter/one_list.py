class Step:
   def __init__(self,dgrams):
       self.dgrams = dgrams
   def events(self):
       for d in self.dgrams:
           if d==102: return
           if d<100: yield d

class Dgrams:
    def __init__(self):
        self.max_retries = 2
        self.n_retries = 0
        self._chunk = iter([])
    def __iter__(self):
        return self
    def __next__(self):
        """ Returns an item in the chunk
        Tries to get another chunk when the last item is reached.
        Raises StopIteration when the last item is reached and
        there are no more chunk.
        """
        try:
            return next(self._chunk)
        except StopIteration: # last item in the chunk reached
            if self.n_retries == 0:
                self._chunk = iter([101,1,2,3,102,101,4,5,102,101,6])
            elif self.n_retries == 1:
                self._chunk = iter([7,8,102,101,9,10])
            else: 
                raise StopIteration # no more chunk
            self.n_retries += 1
            return next(self._chunk)

class Run:
   def __init__(self):
       pass
   def events(self):
       dgrams = Dgrams()
       for d in dgrams:
           if d<100: yield d
   def steps(self):
       dgrams = Dgrams()
       for d in dgrams:
           if d==101: yield Step(dgrams)

if __name__ == "__main__":
    myrun = Run()

    #for evt in myrun.events():
    #    print(evt)                                                                                                                         

    for istep,step in enumerate(myrun.steps()):
       print('step:',istep)
       for evt in step.events():
           print(evt)
