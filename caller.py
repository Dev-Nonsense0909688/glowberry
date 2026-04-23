import time
import subprocess

def process_call(ports):
    time.sleep(1)

    for port in ports:
        try:
            result = subprocess.run(
                ["curl", f"http://127.0.0.1:{port}"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=4,
            )

            if result.returncode == 0:
                return 
        except:
            pass
