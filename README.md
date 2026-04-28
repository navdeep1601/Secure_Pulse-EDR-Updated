# 🛡️ SecurePulse EDR v2 — Honeypot-Based Intrusion Detection System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3.0-black?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

> A lightweight, educational Endpoint Detection & Response (EDR) system that deploys honeypot traps on common attack ports, logs intrusion events to a local database, and visualises them in a real-time web dashboard.

---

## 📸 Dashboard Preview

![SecurePulse Dashboard](securepulse_edr_v2.html)

> Open `securepulse_edr_v2.html` in a browser for a standalone interactive preview of the dashboard UI.

---

## 📖 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Dashboard](#dashboard)
- [Honeypot Traps](#honeypot-traps)
- [API Endpoints](#api-endpoints)
- [Security Notice](#security-notice)
- [Roadmap](#roadmap)
- [Author](#author)

---

## Overview

**SecurePulse EDR v2** is a Python-based honeypot and intrusion detection framework built for learning and home-lab use. It listens on commonly attacked ports (SSH, HTTP, FTP, Telnet, SMB, RDP), captures attacker IPs and payloads, and surfaces the data through a clean real-time dashboard.

The project is designed to help cybersecurity students understand:

- How attackers probe networks using port scanners (e.g. Nmap)
- How honeypots deceive and log adversaries
- How backend APIs and databases tie into a SOC-style alerting workflow
- How a basic EDR pipeline is structured end-to-end

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      ATTACKER                           │
│              (Port Scanner / Exploit Tool)               │
└──────────────────────────┬──────────────────────────────┘
                           │  TCP Connection
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   MIRAGE ENGINE                         │
│              agent/agent_main.py                        │
│                                                         │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────────┐  │
│  │  SSH Trap    │ │  Web Trap    │ │ Generic Trap   │  │
│  │  Port 22     │ │  Port 80     │ │ 21/23/445/3389 │  │
│  └──────┬───────┘ └──────┬───────┘ └───────┬────────┘  │
│         └────────────────┼─────────────────┘           │
│                          │  HTTP POST /alert            │
└──────────────────────────┼──────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  FLASK BACKEND                          │
│              server/app.py   :5000                      │
│                                                         │
│              server/database.py (SQLite)                │
│              mirage_events.db                           │
└──────────────────────────┬──────────────────────────────┘
                           │  GET /events (JSON)
                           ▼
┌─────────────────────────────────────────────────────────┐
│               REAL-TIME DASHBOARD                       │
│         dashboard/index.html + script.js                │
│         Polls every 2 seconds — no refresh needed       │
└─────────────────────────────────────────────────────────┘
```

---

## Features

| Feature | Description |
|---|---|
| 🕵️ Multi-port honeypot | Listens on FTP (21), SSH (22), Telnet (23), HTTP (80), SMB (445), RDP (3389) |
| 🎭 Service emulation | Sends fake SSH banners, fake Apache headers, fake admin login pages |
| 📦 Auto port detection | Skips ports already in use via `psutil` |
| 🗃️ SQLite logging | All events persisted with timestamp, IP, port, service, and payload |
| 🌐 REST API | Flask backend exposes `/alert` and `/events` endpoints |
| 📊 Live dashboard | Browser-based UI polls every 2 seconds with flash effect on new alerts |
| 🧵 Threaded engine | Each trap runs in its own daemon thread via `MirageEngine` |

---

## Project Structure

```
SecurePulse_2/
│
├── agent/                        # Honeypot agent
│   ├── agent_main.py             # Entry point — starts MirageEngine
│   ├── core/
│   │   ├── engine.py             # MirageEngine: spawns trap threads
│   │   └── inventory.py         # Port scanner — finds free ports
│   └── traps/
│       ├── ssh_trap.py           # Fake SSH service (port 22)
│       ├── web_trap.py           # Fake HTTP/Apache server (port 80)
│       └── generic_trap.py      # Generic TCP listener (all other ports)
│
├── server/                       # Flask REST API
│   ├── app.py                    # Routes: /alert (POST), /events (GET)
│   └── database.py              # SQLite init + insert helpers
│
├── dashboard/                    # Frontend
│   ├── index.html                # Dashboard layout
│   ├── script.js                 # Polling logic + DOM updates
│   └── style.css                 # Styling
│
├── honey_files/
│   └── confidential.docx        # Decoy file (bait document)
│
├── logs/
│   ├── requirements.txt         # Python dependencies
│   └── README.md                # Logs folder notes
│
└── securepulse_edr_v2.html      # Standalone dashboard preview
```

---

## How It Works

1. **Agent starts** — `agent_main.py` checks which target ports (21, 22, 23, 80, 445, 3389) are free using `psutil`.
2. **MirageEngine deploys traps** — For each free port, a thread is spawned running the appropriate trap function.
3. **Attacker connects** — An attacker or port scanner hits one of the open trap ports.
4. **Trap responds** — The trap sends a convincing fake banner (SSH, HTTP, or generic TCP) to fool the attacker into thinking a real service is running.
5. **Alert is logged** — The trap POSTs the attacker's IP, port, service type, and payload to the Flask `/alert` endpoint.
6. **SQLite stores it** — The backend writes the event into `mirage_events.db`.
7. **Dashboard displays it** — The browser dashboard polls `/events` every 2 seconds and renders new alerts with a flash animation.

---

## Installation

### Prerequisites

- Python 3.10+
- pip
- A Linux or Windows host (Linux recommended for port binding)
- Admin/root privileges (required for binding to ports below 1024)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/SecurePulse.git
cd SecurePulse

# 2. (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r logs/requirements.txt
```

---

## Usage

You need two terminal windows — one for the Flask server and one for the agent.

### Terminal 1 — Start the Flask Backend

```bash
cd server
python app.py
```

Output:
```
 * Running on http://127.0.0.1:5000
```

### Terminal 2 — Start the Honeypot Agent

```bash
# Root/admin required to bind to privileged ports
sudo python agent/agent_main.py
```

Output:
```
[*] SecurePulse Mirage: Initializing System...
[*] Engine Active. 6 Traps Deployed.
```

> **Note:** If a port is already in use on your system, `inventory.py` will automatically skip it.

---

## Dashboard

Open `dashboard/index.html` in your browser (or use a local web server):

```bash
# Simple local server (Python built-in)
cd dashboard
python3 -m http.server 8080
# Then visit: http://localhost:8080
```

The dashboard will:
- Automatically fetch events from `http://127.0.0.1:5000/events`
- Refresh every **2 seconds**
- Flash new alert rows in a different colour when they appear
- Display: Timestamp · Attacker IP · Port · Service · Payload

---

## Honeypot Traps

| Trap | Port | Emulated Service | Behaviour |
|---|---|---|---|
| `ssh_trap.py` | 22 | OpenSSH 8.2p1 | Sends fake SSH banner, captures client response |
| `web_trap.py` | 80 | Apache/2.4.41 | Returns fake admin login page with Apache headers |
| `generic_trap.py` | 21, 23, 445, 3389 | Generic TCP | Accepts connection and immediately logs the probe |

---

## API Endpoints

| Method | Route | Description |
|---|---|---|
| `POST` | `/alert` | Receives intrusion events from traps. Body: `{ip, port, service, payload}` |
| `GET` | `/events` | Returns the latest 50 events from SQLite as JSON |

### Example `/events` Response

```json
[
  {
    "id": 12,
    "timestamp": "2026-04-28 10:45:02",
    "attacker_ip": "192.168.1.105",
    "port": 22,
    "service": "SSH",
    "payload": "SSH Scanner"
  }
]
```

---

## Security Notice

> ⚠️ **This project is for educational and home-lab use only.**

- Do **not** deploy this on a public-facing server without a firewall and proper network isolation.
- The Flask backend runs in `debug=True` mode — disable this in any production-like setup.
- Binding to ports below 1024 requires root/admin — understand the risks of running privileged processes.
- The honeypot is intentionally simple and **not designed to withstand sophisticated attacks**.

---

## Roadmap

- [ ] Add email/webhook alerting (Slack, Discord)
- [ ] Threat scoring per IP (frequency-based)
- [ ] GeoIP lookup to map attacker locations
- [ ] Persistent dashboard with Chart.js attack graphs
- [ ] Docker containerisation for easy deployment
- [ ] Export events to CSV / SIEM-compatible JSON
- [ ] PCAP capture integration

---

## Author

Built by Navdeep as a hands-on EDR and honeypot learning project.

If you find this useful, feel free to ⭐ the repo and share feedback via Issues.

---

## License

This project is licensed under the [MIT License](LICENSE).
