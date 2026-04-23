from scapy.all import sniff, TCP, Raw
from glowberry.parser import *
from glowberry.state import *
import time
from colorama import Fore
import threading

def cb(pkt):
    global flow, data, wee

    if not (pkt.haslayer(TCP) and pkt.haslayer(Raw)):
        return

    tcp = pkt[TCP]
    s, d = tcp.sport, tcp.dport
    raw = pkt[Raw].load.decode("utf-8", errors="ignore")

    method, path = parse_request(raw)
    status = parse_response(raw)

    if d in PORTS and method:
        wee.append(d)
        flow.append(d)
        data[d]["method"] = method
        data[d]["path"] = path
        timings[d] = time.time()

    elif s in PORTS and status:
        wee.append(s)
        data[s]["status_code"] = status

        if s in timings:
            data[s]["latency"] = round((time.time() - timings[s]) * 1000, 2)

    if wee and wee[-1] == wee[0] and len(wee) > 2:
        if len(set(flow)) != len(flow):
            print(Fore.YELLOW + "Possible branching detected!" + Fore.RESET)
        print()
        for i in range(len(flow) - 1):
            port = flow[i]
            nport = flow[i + 1]

            status_code = int(data[port]["status_code"])

            if status_code == 200:
                color = Fore.LIGHTGREEN_EX
                text = "200 OK"
            else:
                color = Fore.LIGHTRED_EX
                text = f"{status_code} Error"

            print(
                f"[{port}] -> [{nport}] {data[port]['method']} {data[port]['path']} "
                f"({color}{text}{Fore.RESET}) - {data[port]['latency']:.0f}ms"
            )

        # reset state
        flow.clear()
        wee.clear()
        for p in PORTS:
            data[p] = {
                "alive": False,
                "status_code": None,
                "method": None,
                "path": None,
                "latency": 0.0,
            }


from scapy.all import AsyncSniffer
import time


def start_sniffing():

    sniffer = AsyncSniffer(
        iface=r"\Device\NPF_Loopback",
        filter="tcp and (port 3000 or port 4000 or port 5001)",
        prn=cb,
        store=False,
    )

    sniffer.start()

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        sniffer.stop()  
        print("Stopped")
