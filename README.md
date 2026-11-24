# British Auction RFQ

A simplified RFQ system with British Auction bidding. FastAPI + SQLite + React.

- [HLD](docs/HLD.md)
- [Database design](docs/DATABASE.md)
- [API plan](docs/PLAN.md)

## Run

Backend:

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn main:app --reload
```

Frontend (second terminal):

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173
