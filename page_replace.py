#!/usr/bin/env python3
"""Page replacement algorithms: FIFO, LRU, OPT, Clock."""
import sys
from collections import deque,OrderedDict
def fifo(pages,frames):
    mem=deque();faults=0
    for p in pages:
        if p not in mem:
            faults+=1
            if len(mem)>=frames: mem.popleft()
            mem.append(p)
    return faults
def lru(pages,frames):
    mem=OrderedDict();faults=0
    for p in pages:
        if p in mem: mem.move_to_end(p)
        else:
            faults+=1
            if len(mem)>=frames: mem.popitem(last=False)
            mem[p]=True
    return faults
def optimal(pages,frames):
    mem=set();faults=0
    for i,p in enumerate(pages):
        if p not in mem:
            faults+=1
            if len(mem)>=frames:
                future={m:next((j for j in range(i+1,len(pages)) if pages[j]==m),float('inf')) for m in mem}
                evict=max(future,key=future.get)
                mem.remove(evict)
            mem.add(p)
    return faults
def main():
    pages=[7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]
    frames=3
    print(f"Pages: {pages}\nFrames: {frames}\n")
    for name,algo in [("FIFO",fifo),("LRU",lru),("OPT",optimal)]:
        f=algo(pages,frames)
        print(f"  {name:5s}: {f} faults ({f/len(pages)*100:.0f}% miss rate)")
if __name__=="__main__": main()
