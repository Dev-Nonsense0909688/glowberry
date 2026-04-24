import time
from .sniffer import start_sniffer
from ..tree import build_tree, print_tree

flow = []


def start_machine(PORTS):
    sniffer = start_sniffer(flow, PORTS)

    print("Tracing started...")
    sniffer.start()

    try:
        while True:
            time.sleep(0.5)

    except KeyboardInterrupt:
        sniffer.stop()

        print("\nFlow:", flow)

        tree = build_tree(flow)
        print(tree)
        root = flow[0] if flow else None

        if root:
            print_tree(root, tree)

        print("Stopped")
