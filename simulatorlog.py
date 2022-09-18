LOG_EVENT = True
LOG_STATUS = True
LOG_MOVEMENT = True
LOG_INFO = True


def print_event(site, item_id, starttime, duration):
    if LOG_EVENT:
        print(
            f"Site {site}: Process {item_id} at {starttime:06.2f} using {duration:06.2f}"
        )


def print_status(timestamp, graph):
    if LOG_STATUS:
        print(f"[{timestamp:06.2f}]")
        for idx, k in enumerate(graph):
            print(f"{idx}: ", end="")
            for c in k["queue"]:
                print(f" {c[0]:4d}", end="")
            print("")


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
