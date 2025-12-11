# Secure System Call Interface — Tkinter (Portfolio Project)

A compact, well-structured Tkinter application that simulates a secure system-call gateway with authentication, RBAC policy, audit logging, and a tidy UI.

## Features
- Username/password authentication (admin / user / guest)
- Role-Based Access Control (RBAC) via `data/policy.json`
- Simulated privileged actions: read/write file, list/spawn processes, ping
- Audit logging in SQLite with query & CSV export
- Logs viewer with filters and refresh
- System Info viewer with refresh
- Optional dark theme and sidebar navigation

## Default users
- admin / admin123 (admin)
- user / user123 (standard_user)
- guest / guest123 (guest)

## Requirements
- Python 3.9+
- psutil (`pip install psutil`)

## Run
```bash
pip install -r requirements.txt   # optional: psutil only
python main.py
