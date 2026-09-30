# 🛡️ Cybersecurity Attack Path Visualizer




Interactive defensive cybersecurity application for visualizing simulated network attack paths and exposure relationships.

> Educational/local simulation only. It does not exploit systems, scan external networks, steal credentials, or perform real attacks.

## Features
- Interactive network visualization
- Simulated compromised starting node
- Target selection
- Possible attack-path discovery using graph analysis
- Educational risk scoring
- LOW / MEDIUM / HIGH severity
- Add custom nodes and connections
- JSON report export
- Streamlit dashboard

## Structure
```text
Cybersecurity-Attack-Path-Visualizer/
├── app.py
├── attack_path.py
├── requirements.txt
├── README.md
└── reports/
    └── .gitkeep
```

## Install
```powershell
cd Cybersecurity-Attack-Path-Visualizer
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## How it works
The application models systems as graph nodes and network relationships as edges. A selected source represents a simulated compromised system. The application then finds possible paths to a selected target and calculates an educational exposure score.

The score is a simple heuristic and is **not** a real CVSS or vulnerability rating.

## Example
```text
Internet
   ↓
Web Server
   ↓
Internal Server
   ↓
Database
```

## Safety
Use this project for learning, lab environments, and systems you own or are authorized to analyze. The application performs no real exploitation or unauthorized network activity.

## License
Educational portfolio project.
