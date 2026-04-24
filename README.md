<p align="center">
  <img src="screenshots/logo.png" width="300">
</p>
<p align=center>
  <img src="https://img.shields.io/badge/python-3.11-blue">
  <img src="https://img.shields.io/badge/status-beta-orange">
  <img src="https://img.shields.io/badge/License-MIT-green">
  <img src="https://img.shields.io/github/stars/Dev-Nonsense0909688/glowberry">
</p>

# Glowberry
Lightweight CLI tool to trace service-to-service request flow and latency on localhost.


## Usage

```bash
glowberry watch 3000:frontend 4000:gateway 5001:db
```


## Features

* **Service Flow Tracing**
  Track how requests move between services (frontend → gateway → db)

* **Latency Measurement**
  See response time between hops in milliseconds

* **HTTP Parsing**
  Extract method and path (`GET /`, etc.)

* **Status Detection**
  Displays response status (200 OK / errors)

* **Colored Output**
  Green = success, Red = failure


## Example Output

```
🍇 Monitoring 3 berries...

[frontend] → [gateway] GET / (200 OK) - 7ms
[gateway] → [db]       GET / (200 OK) - 4ms
```



## Installation

```bash
git clone https://github.com/Dev-Nonsense0909688/glowberry
cd glowberry
pip install -e .
```


## Requirements

* Python 3.10+




## Beta Limitations

* Only supports **linear request flows** (no branching yet)
* Works best on **localhost traffic**
* No persistent storage (no history yet)



## How it works

Glowberry uses:

* **Scapy** → sniff network packets
* **curl (subprocess)** → trigger requests
* Custom parsing → detect flow, latency, and status



## Contributing

Pull requests are welcome. This is an early-stage tool — expect rough edges.



## If you like it

Drop a star — helps more than you think.
