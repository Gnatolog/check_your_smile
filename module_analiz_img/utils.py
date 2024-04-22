import threading


def start_tread(frontal, lateral):
    treads = []
    t_1 = threading.Thread(target=frontal)
    t_2 = threading.Thread(target=lateral)
    treads.append(t_1)
    treads.append(t_1)
    t_1.start()
    t_2.start()

    for thread in treads:
        thread.join()
