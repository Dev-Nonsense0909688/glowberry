from scapy.all import AsyncSniffer, TCP, Raw


def start_sniffer(flow, PORTS: set):
    def cb(pkt):
        if not (pkt.haslayer(TCP) and pkt.haslayer(Raw)):
            return

        tcp = pkt[TCP]
        s, d = tcp.sport, tcp.dport

        try:
            raw = pkt[Raw].load.decode("utf-8", errors="ignore")
        except:
            return

        if raw.startswith("HTTP"):
            return

        if d in PORTS:
            flow.append(d)
            print(f"{s} → {d}")
        elif s in PORTS:
            flow.append(s)
            print(f"{s} → {d}")

    filter_str = "tcp and (" + " or ".join(f"port {p}" for p in PORTS) + ")"

    sniffer = AsyncSniffer(
        iface=r"\Device\NPF_Loopback",
        filter=filter_str,
        prn=cb,
        store=False,
    )

    return sniffer
