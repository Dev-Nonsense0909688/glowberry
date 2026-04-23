PORTS = [3000, 4000, 5001]

METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "HEAD",
    "OPTIONS",
    "CONNECT",
    "TRACE",
]

timings = {}
wee = []
flow = []

data = {
    p: {
        "alive": False,
        "status_code": None,
        "method": None,
        "path": None,
        "latency": 0.0,
    }
    for p in PORTS
}

CURL_ERRORS = {
    0: "OK",
    6: "Couldn't resolve host",
    7: "Failed to connect",
    28: "Operation timeout",
    35: "SSL connect error",
    47: "Too many redirects",
    52: "Empty reply from server",
    56: "Failure in receiving data",
}
