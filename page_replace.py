#!/usr/bin/env python3
"""Page replacement algorithms (FIFO, LRU, OPT, Clock) — zero-dep."""
from collections import OrderedDict

def fifo(pages, frames):
    memory=[]; faults=0
    for p in pages:
        if p not in memory:
            faults+=1
            if len(memory)>=frames: memory.pop(0)
            memory.append(p)
    return faults

def lru(pages, frames):
    memory=OrderedDict(); faults=0
    for p in pages:
        if p in memory: memory.move_to_end(p)
        else:
            faults+=1
            if len(memory)>=frames: memory.popitem(last=False)
            memory[p]=True
    return faults

def optimal(pages, frames):
    memory=[]; faults=0
    for i,p in enumerate(pages):
        if p not in memory:
            faults+=1
            if len(memory)>=frames:
                future={m:len(pages) for m in memory}
                for m in memory:
                    for j in range(i+1,len(pages)):
                        if pages[j]==m: future[m]=j; break
                victim=max(memory,key=lambda m:future[m])
                memory.remove(victim)
            memory.append(p)
    return faults

def clock(pages, frames):
    memory=[None]*frames; use=[False]*frames; ptr=0; faults=0
    for p in pages:
        if p in memory: use[memory.index(p)]=True; continue
        faults+=1
        while use[ptr]: use[ptr]=False; ptr=(ptr+1)%frames
        memory[ptr]=p; use[ptr]=True; ptr=(ptr+1)%frames
    return faults

if __name__=="__main__":
    pages=[7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]
    frames=3
    print(f"Pages: {pages}, Frames: {frames}")
    for name,fn in [("FIFO",fifo),("LRU",lru),("Optimal",optimal),("Clock",clock)]:
        print(f"  {name:>8}: {fn(pages,frames)} faults")
