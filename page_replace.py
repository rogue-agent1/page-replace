#!/usr/bin/env python3
"""page_replace - Page replacement algorithms (FIFO, LRU, Optimal)."""
import sys, collections
def fifo(pages, frames):
    memory=collections.deque(maxlen=frames); faults=0; history=[]
    for p in pages:
        hit=p in memory
        if not hit: memory.append(p); faults+=1
        history.append((p,"HIT" if hit else "FAULT",list(memory)))
    return faults, history
def lru(pages, frames):
    memory=[]; faults=0; history=[]
    for p in pages:
        hit=p in memory
        if hit: memory.remove(p); memory.append(p)
        else:
            if len(memory)>=frames: memory.pop(0)
            memory.append(p); faults+=1
        history.append((p,"HIT" if hit else "FAULT",list(memory)))
    return faults, history
def optimal(pages, frames):
    memory=[]; faults=0; history=[]
    for i,p in enumerate(pages):
        hit=p in memory
        if not hit:
            if len(memory)>=frames:
                furthest=-1; victim=0
                for j,m in enumerate(memory):
                    try: next_use=pages[i+1:].index(m)
                    except ValueError: next_use=float('inf')
                    if next_use>furthest: furthest=next_use; victim=j
                memory[victim]=p
            else: memory.append(p)
            faults+=1
        history.append((p,"HIT" if hit else "FAULT",list(memory)))
    return faults, history
if __name__=="__main__":
    pages=[7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]
    frames=int(sys.argv[1]) if len(sys.argv)>1 else 3
    print(f"Pages: {pages}, Frames: {frames}")
    for name,fn in [("FIFO",fifo),("LRU",lru),("Optimal",optimal)]:
        faults,history=fn(pages,frames)
        print(f"\n{name}: {faults} faults ({faults/len(pages)*100:.0f}% miss rate)")
        for p,status,mem in history[-5:]:
            print(f"  Page {p}: {status:5s} {mem}")
