from fastapi import FastAPI

import db

db.init()
app = FastAPI()


@app.get("/api/health")
def health():
    return {"status": "ok"}
