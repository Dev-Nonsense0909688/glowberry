import threading
from state import PORTS as DEFAULT_PORTS
from caller import process_call
from sniffer import start_sniffing
import argparse
import subprocess
from colorama import Fore, Style
from state import CURL_ERRORS

def parse_ports(port_args):
    mapping = {}
    for item in port_args:
        port, name = item.split(":")
        mapping[int(port)] = name
    return mapping


def get_curl_status(code: int) -> str:
    return CURL_ERRORS.get(code, f"Unknown error ({code})")


parser = argparse.ArgumentParser(prog="glowberry")

sub = parser.add_subparsers(dest="command")


watch = sub.add_parser("watch", help="Trace routes of microservices...")
watch.add_argument("services", nargs="+")
watch.add_argument("--no-call", action="store_true")
watch.add_argument("--interval", type=float, default=1.0)

scan = sub.add_parser("scan", help="check which services respond")
scan.add_argument("ports", nargs="+", type=int)

args = parser.parse_args()

if args.command == "watch":
    services: dict = parse_ports(args.services)
    PORTS = list(services.keys()) or DEFAULT_PORTS

    print(f"🍇 Monitering {PORTS.__len__()} berries...")

    if not args.no_call:
        threading.Thread(target=process_call, args=(PORTS,), daemon=True).start()

    start_sniffing()


elif args.command == "scan":

    print("Scanning ports...")
    for p in args.ports:
        print(f"[{p}]", end=" -> ")
        result = subprocess.run(
            ["curl", f"http://127.0.0.1:{p}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=4,
        )
        if result.returncode == 0:
            text = Fore.GREEN + get_curl_status(result.returncode) + Fore.RESET
        else:
            text = Fore.RED + get_curl_status(result.returncode) + Fore.RESET
        print(text)

    print()
else:
    parser.print_help()
