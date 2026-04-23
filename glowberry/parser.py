from glowberry.state import METHODS

def parse_request(raw):
    line = raw.split("\r\n")[0]
    parts = line.split(" ")

    if parts and parts[0] in METHODS:
        return parts[0], parts[1] if len(parts) > 1 else "/"

    return None, None


def parse_response(raw):
    line = raw.split("\r\n")[0]
    parts = line.split(" ")

    if line.startswith("HTTP") and len(parts) > 1:
        return parts[1]
