import numpy as np

src = {}
registration = {}
service = {}

graph = [src, registration, service]
src["next"] = 1
src["distr"] = [np.random.exponential, 20]
src["blocked"] = False
src["capacity"] = -1
src["queue"] = []
src["src"] = True

registration["next"] = 2
registration["distr"] = [np.random.normal, 28, 10]
registration["blocked"] = True
registration["isblocked"] = False
registration["capacity"] = -1
registration["queue"] = []
registration["src"] = False

service["next"] = None
service["distr"] = [np.random.normal, 35, 5]
service["blocked"] = False
service["capacity"] = 3
service["queue"] = []
service["src"] = False

# Please make sure that the ordering in the graph is in topological sorting

# customer format
# (cid, in_time, out_time, process_time)
cid = 0
timestamp = 0
maxduration = 180 #* 3600
maxsites = len(graph)
tlist = [0] * maxsites
while timestamp < maxduration:
    # traverse the graph
    # generate and process
    for idx, k in enumerate(graph):
        if k["src"]:
            if len(k["queue"]) < 1:
                cid = cid + 1
                interarrtime = k["distr"][0](*k["distr"][1:])
                newtimestamp = timestamp + interarrtime
                c = [cid, timestamp, None, interarrtime]
                k["queue"].append(c)
                print("Generate Cus", c[0], "at", newtimestamp)
        elif len(k["queue"]) > 0:
            if k["queue"][0][3] == None:
                # the item to process
                processtime = k["distr"][0](*k["distr"][1:])                
                k["queue"][0][3] = processtime
                print("Site",  idx, "Process Cus", k["queue"][0][0], "using", processtime)
    
    for idx, k in enumerate(graph):
        if len(k["queue"])>0:
            if k["queue"][0][2] == None:
                k["queue"][0][2] = timestamp + k["queue"][0][3]
            tlist[idx] = k["queue"][0][2]
        else:
            tlist[idx] = maxduration
    
    sortedidx = [i[0] for i in sorted(enumerate(tlist), key=lambda x:x[1])]
    process_idx = None
    for idx in sortedidx:
        nextidx = graph[idx]["next"]
        if graph[idx]["blocked"]:
            if graph[nextidx]["capacity"] == len(graph[nextidx]["queue"]):
                graph[idx]["isblocked"] = True
                print("[INFO] Site", idx, "BLOCKED")
                graph[idx]["queue"][0][2] = None
                continue
            else:
                graph[idx]["isblocked"] = False
                process_idx = idx
                break
        else:
            process_idx = idx
            break

    assert(process_idx != None)
    if tlist[process_idx] >= maxduration:
        print("[INFO] Time is up")
        exit(0)

    # update the process_idx
    moving_c = graph[process_idx]["queue"][0]
    del graph[process_idx]["queue"][0]
    moving_c[2] = tlist[process_idx]
    nextidx = graph[process_idx]["next"]
    if nextidx == None:
        # out
        print("[{:06.2f}]".format(tlist[process_idx]), "Move Cus {} from {} to Out".format(moving_c[0], process_idx))
    else:
        # moving
        print("[{:06.2f}]".format(tlist[process_idx]), "Move Cus {} from {} to {}".format(moving_c[0], process_idx, nextidx))
        moving_c[1] = moving_c[2]
        moving_c[2] = None
        moving_c[3] = None
        graph[nextidx]["queue"].append(moving_c)
    # update timestamp
    timestamp = tlist[process_idx]
