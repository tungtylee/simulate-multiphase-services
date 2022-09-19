import time

LOG_EVENT = True
LOG_STATUS = True
LOG_MOVEMENT = True
LOG_INFO = True
vis_table = {}


def print_event(site, item_id, starttime, duration):
    if LOG_EVENT:
        print(
            f"Site {site}: Process {item_id} at {starttime:06.2f} using {duration:06.2f}"
        )


def print_status(timestamp, graph):
    if LOG_STATUS:
        print(f"[{timestamp:06.2f}]")
        all_status = ""
        for idx, k in enumerate(graph):
            site_status = f"{idx}: "
            for c in k["queue"]:
                site_status += f" {c[0]:4d}"
            all_status += site_status + "\n"
        print(all_status)
        vis_table[int(timestamp * 10)] = all_status


def print_movement(timestamp, cid, process_idx, nextidx):
    if LOG_MOVEMENT:
        print(f"[{timestamp:06.2f}]:", end="")
        print(f" Move Cus {cid} from {process_idx} to {nextidx}")


def print_info(info):
    if LOG_INFO:
        print(info)


def gen_table(table, timestamp, graph):
    maxsite = len(graph)
    for idx, k in enumerate(graph):
        for c in k["queue"]:
            cid = c[0]
            if cid not in table:
                t_template = [None] * maxsite * 3
                table[cid] = t_template
            site = idx
            subc = c[1:4]
            for cidx, cval in enumerate(subc):
                if cval is not None:
                    table[cid][site * 3 + cidx] = cval


def print_table(table):
    for k in sorted(table.keys()):
        print(f"{k}: {table[k]}")
    print_vis_table(vis_table)


def print_vis_table(vis):
    t = 0
    ith = 0
    tlist = list(vis.keys())
    maxt = max(tlist) + 10
    maxitem = len(tlist)
    oldstatus = "\n\n\n"
    LINE_UP = "\033[1A"
    LINE_DOWN = "\033[1B"
    LINE_CLEAR = "\x1b[2K"
    while t < maxt:
        if t == 0:
            print(f"[{t/10:06.2f}]")
            print(oldstatus)
            t += 1
        elif ith >= maxitem or t < tlist[ith]:
            print(LINE_UP, end="")
            print(LINE_UP, end="")
            print(LINE_UP, end="")
            print(LINE_UP, end="")
            print(LINE_UP, end=LINE_CLEAR)
            print(f"[{t/10:06.2f}]")
            print(LINE_DOWN, end="")
            print(LINE_DOWN, end="")
            print(LINE_DOWN, end="")
            print(LINE_DOWN, end="")
            # print(oldstatus)
            t += 1
        else:
            oldstatus = vis[tlist[ith]]
            ith += 1
            print(LINE_UP, end=LINE_CLEAR)
            print(LINE_UP, end=LINE_CLEAR)
            print(LINE_UP, end=LINE_CLEAR)
            print(LINE_UP, end=LINE_CLEAR)
            print(LINE_UP, end=LINE_CLEAR)
            print(f"[{t/10:06.2f}]")
            print(oldstatus)
            t += 1
        time.sleep(0.02)
