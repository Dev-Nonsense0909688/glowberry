import multiprocessing
from multiprocessing import Manager
from flask import Flask, request, jsonify
import requests, time, uuid

GRAPH = {
    4000: [4001, 4002, 4004, 4003],
    4001: [4003],
    4002: [],
    4003: [],
    4004: []
}


def run_service(port, REAL_EDGES, TRACE_LOG):
    app = Flask(__name__)

    @app.route("/")
    def handle():
        trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())

        time.sleep(0.1)  # fixed delay (no randomness)

        for nxt in GRAPH.get(port, []):
            try:
                # log edge
                REAL_EDGES.append((trace_id, port, nxt))

                if trace_id not in TRACE_LOG:
                    TRACE_LOG[trace_id] = []
                TRACE_LOG[trace_id].append((port, nxt))

                requests.get(
                    f"http://127.0.0.1:{nxt}",
                    headers={"X-Trace-ID": trace_id},
                    timeout=1,
                )
            except:
                pass

        return f"OK {port}"

    @app.route("/__truth__")
    def truth():
        return jsonify({"edges": list(REAL_EDGES), "traces": dict(TRACE_LOG)})

    app.run(port=port)


def start_all(REAL_EDGES, TRACE_LOG):
    processes = []

    for port in GRAPH:
        p = multiprocessing.Process(
            target=run_service, args=(port, REAL_EDGES, TRACE_LOG)
        )
        p.start()
        processes.append(p)

    return processes


if __name__ == "__main__":
    from multiprocessing import freeze_support

    freeze_support()

    manager = Manager()
    REAL_EDGES = manager.list()
    TRACE_LOG = manager.dict()

    print("🔥 Starting SIMPLE test services...")

    procs = start_all(REAL_EDGES, TRACE_LOG)

    print("👉 Entry: http://127.0.0.1:4000")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        for p in procs:
            p.terminate()
