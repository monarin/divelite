class Step:
    def __init__(self,chunks):
        self.chunks = chunks
    def events(self):
        for i, chunk in enumerate(chunks):
            print(f'events() chunk {i}')
            for dg in chunk:
                if dg==102: return
                if dg<100: yield dg

chunks = [iter([101,1,2,3,102,101,4,5,102,101,6]),iter([7,8,102,101,9,10])]

class Run:
    def __init__(self):
        pass
    def events(self):
        for chunk in chunks:
            for dg in chunk:
                if dg<100: yield dg
    def steps(self):
        for chunk in chunks:
            for dg in chunk:
                if dg==101: yield Step(chunks)

myrun = Run()

#for evt in myrun.events():                                                                                                            
#    print(evt)                                                                                                                        

for istep,step in enumerate(myrun.steps()):
    print('step:',istep)
    for evt in step.events():
        print(evt)

