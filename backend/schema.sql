CREATE TABLE IF NOT EXISTS rfqs (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    bid_start TEXT NOT NULL,
    bid_close TEXT NOT NULL,
    current_close TEXT NOT NULL,
    forced_close TEXT NOT NULL,
    service_date TEXT NOT NULL,
    trigger_window INTEGER NOT NULL CHECK (trigger_window > 0),
    extension_duration INTEGER NOT NULL CHECK (extension_duration > 0),
    trigger_type TEXT NOT NULL CHECK (trigger_type IN ('BID_RECEIVED', 'RANK_CHANGE', 'L1_CHANGE')),
    CHECK (bid_start < bid_close),
    CHECK (forced_close > bid_close),
    CHECK (current_close <= forced_close)
);

CREATE TABLE IF NOT EXISTS bids (
    id INTEGER PRIMARY KEY,
    rfq_id INTEGER NOT NULL REFERENCES rfqs(id),
    carrier_name TEXT NOT NULL COLLATE NOCASE,
    freight_charges REAL NOT NULL CHECK (freight_charges >= 0),
    origin_charges REAL NOT NULL CHECK (origin_charges >= 0),
    destination_charges REAL NOT NULL CHECK (destination_charges >= 0),
    total REAL NOT NULL,
    transit_days INTEGER NOT NULL CHECK (transit_days > 0),
    valid_until TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY,
    rfq_id INTEGER NOT NULL REFERENCES rfqs(id),
    type TEXT NOT NULL CHECK (type IN ('BID', 'EXTENSION')),
    message TEXT NOT NULL,
    created_at TEXT NOT NULL
);
