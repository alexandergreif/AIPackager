
# AIPackager — AI-Powered App Deployment Script Generator

_AIPackager_ is an intelligent packaging assistant that automatically generates **PowerShell App Deployment Toolkit (PSADT)** scripts based on installer files, using an AI agent-driven architecture.

This MVP is developed as a **solo final project**, with future plans to support enterprise-scale software packaging and testing workflows in compliance with EU regulations (e.g., DSGVO, AI Act).

---

## 🚀 MVP Features

- 🔍 Upload `.exe` or `.msi` installer files via web UI
- 🤖 Auto-generate mock PSADT deployment scripts
- 🧠 Modular agent-based architecture (orchestration + script agent)
- 🗃️ Store and retrieve generated results (DB integration planned)
- 🌐 Built with **Python** + **Flask**

---

## 🧱 Project Structure

```
AIPackager/
├── app/
│   ├── agents/              # AI script generation logic
│   ├── routes/              # Flask route handlers
│   ├── static/              # JS, CSS, icons, Bootstrap
│   ├── templates/           # HTML (Jinja2) views
│   ├── uploads/             # Uploaded installer files
│   ├── models/              # DB models (planned)
│   └── orchestrator.py      # Task router / agent coordinator
├── main.py                  # Flask app entrypoint
├── requirements.txt         # Python dependencies
├── .gitignore               # Excludes venv, __pycache__, uploads
├── README.md                # You're here.
```

---

## 🛠️ Installation & Run

### ⚙️ Requirements

- Python 3.9+
- pip (Python package installer)
- Git (for cloning the repo)

### ▶️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/alexandergreif/AIPackager
cd AIPackager

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python main.py
```

Access it at `http://localhost:5000`

---

## 🧪 Roadmap

| Phase     | Focus                                     |
|-----------|-------------------------------------------|
| MVP       | File upload, AI script generation (mock)  |
| Phase 2   | Integrate LLM for actual PSADT generation |
| Phase 3   | DB storage, multi-agent coordination      |
| Phase 4   | Hyper-V based test automation             |
| Phase 5   | On-prem & Cloud deployment options        |

---

## 🧠 Agent Framework (Planned)

| Agent               | Role                                               |
|---------------------|----------------------------------------------------|
| **Orchestrator**    | Manages workflow between UI, agents, and DB        |
| **Script Agent**    | Generates PSADT deployment scripts                 |
| **Testing Agent**   | (Later) Automates Hyper-V deployment validation    |

---

## 👤 Author

**Alex ***


---

## 📜 License

This project is licensed for academic and demonstration use only. Future licensing for commercial/enterprise use is under review.
