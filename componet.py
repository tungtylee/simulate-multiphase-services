import numpy as np
from simulatorlog import print_event, print_info, print_movement, print_status

src = {}
registration = {}
service = {}

graph = [src, registration, service]
src["next"] = 1
src["distr"] = [np.random.exponential, 10]
src["blocked"] = True
src["isblocked"] = False
src["capacity"] = -1
src["queue"] = []
src["src"] = True

registration["next"] = 2
registration["distr"] = [np.random.normal, 18, 5]
registration["blocked"] = True
registration["isblocked"] = False
registration["capacity"] = 5
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
maxcid = 0
timestamp = 0
maxduration = 180  # * 3600
maxsites = len(graph)
tlist = [0] * maxsites
while timestamp < maxduration:
    # traverse the graph
    # generate and process
    for idx, k in enumerate(graph):
        if k["src"]:
            if (
                len(k["queue"]) < 1
                or timestamp > k["queue"][0][1] + k["queue"][0][3]
            ):
                maxcid = maxcid + 1
                cid = maxcid
                interarrtime = k["distr"][0](*k["distr"][1:])
                newtimestamp = timestamp + interarrtime
                duration = interarrtime
                c = [cid, timestamp, None, interarrtime]
                k["queue"].append(c)
                print_event(idx, cid, timestamp, duration)
        elif len(k["queue"]) > 0:
            if k["queue"][0][3] == None:
                # the item to process
                processtime = k["distr"][0](*k["distr"][1:])
                k["queue"][0][3] = processtime
                cid = k["queue"][0][0]
                duration = processtime
                print_event(idx, cid, timestamp, duration)

    for idx, k in enumerate(graph):
        if len(k["queue"]) > 0:
            if k["queue"][0][2] == None:
                k["queue"][0][2] = timestamp + k["queue"][0][3]
            tlist[idx] = k["queue"][0][2]
        else:
            tlist[idx] = maxduration

    sortedidx = [i[0] for i in sorted(enumerate(tlist), key=lambda x: x[1])]
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

    assert process_idx != None
    if tlist[process_idx] >= maxduration:
        print_info("[INFO] Time is up")
        exit(0)

    # update the process_idx
    moving_c = graph[process_idx]["queue"][0]
    del graph[process_idx]["queue"][0]
    moving_c[2] = tlist[process_idx]
    nextidx = graph[process_idx]["next"]
    if nextidx == None:
        # out
        print_movement(tlist[process_idx], moving_c[0], process_idx, nextidx)
    else:
        # moving
        print_movement(tlist[process_idx], moving_c[0], process_idx, nextidx)
        moving_c[1] = moving_c[2]
        moving_c[2] = None
        moving_c[3] = None
        graph[nextidx]["queue"].append(moving_c)
    # update timestamp
    timestamp = tlist[process_idx]
    print_status(timestamp, graph)
