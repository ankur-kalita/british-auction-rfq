from datetime import date, timezone
from typing import Annotated, Literal

from fastapi import FastAPI
from pydantic import AwareDatetime, BaseModel, Field, StringConstraints, model_validator

import db

db.init()
app = FastAPI()

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Minutes = Annotated[int, Field(ge=1, le=1440)]


class RfqCreate(BaseModel):
    name: Text
    bid_start: AwareDatetime
    bid_close: AwareDatetime
    forced_close: AwareDatetime
    service_date: date
    trigger_window: Minutes
    extension_duration: Minutes
    trigger_type: Literal["BID_RECEIVED", "RANK_CHANGE", "L1_CHANGE"]

    @model_validator(mode="after")
    def check_times(self):
        if self.bid_start >= self.bid_close:
            raise ValueError("Bid close must be later than bid start")
        if self.forced_close <= self.bid_close:
            raise ValueError("Forced close must be later than bid close")
        return self


def to_utc(time):
    return time.astimezone(timezone.utc).isoformat(timespec="microseconds")


@app.post("/api/rfqs", status_code=201)
def create_rfq(rfq: RfqCreate):
    conn = db.connect()
    try:
        cursor = conn.execute(
            """INSERT INTO rfqs (name, bid_start, bid_close, current_close, forced_close,
               service_date, trigger_window, extension_duration, trigger_type)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                rfq.name,
                to_utc(rfq.bid_start),
                to_utc(rfq.bid_close),
                to_utc(rfq.bid_close),
                to_utc(rfq.forced_close),
                rfq.service_date.isoformat(),
                rfq.trigger_window,
                rfq.extension_duration,
                rfq.trigger_type,
            ),
        )
        return {"id": cursor.lastrowid}
    finally:
        conn.close()
