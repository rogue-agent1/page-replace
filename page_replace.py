#!/usr/bin/env python3
"""Page replacement: LRU, FIFO, Clock."""
import sys, collections
def fifo_replace(pages,frames):
    memory=collections.deque(maxlen=frames); faults=0
    for p in pages:
        if p not in memory: faults+=1; memory.append(p)
    return faults
def lru_replace(pages,frames):
    memory=[]; faults=0
    for p in pages:
        if p in memory: memory.remove(p); memory.append(p)
        else:
            faults+=1
            if len(memory)>=frames: memory.pop(0)
            memory.append(p)
    return faults
def clock_replace(pages,frames):
    memory=[None]*frames; use=[False]*frames; ptr=0; faults=0
    for p in pages:
        if p in memory: use[memory.index(p)]=True; continue
        faults+=1
        while use[ptr]: use[ptr]=False; ptr=(ptr+1)%frames
        memory[ptr]=p; use[ptr]=True; ptr=(ptr+1)%frames
    return faults
pages=[7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]
frames=int(sys.argv[1]) if len(sys.argv)>1 else 3
print(f"Pages: {pages}, Frames: {frames}\n")
for name,fn in [('FIFO',fifo_replace),('LRU',lru_replace),('Clock',clock_replace)]:
    f=fn(pages,frames); print(f"  {name:6s}: {f} faults ({f/len(pages)*100:.0f}%)")
