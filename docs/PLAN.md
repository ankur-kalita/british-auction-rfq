# API Plan

Each step is one API plus its screen, in one commit. Rules are in [HLD.md](HLD.md).

**Files:** `backend/main.py` (routes), `backend/auction.py` (status, ranking, extension), `backend/test_auction.py`, `frontend/src/App.jsx` (switches pages with `useState`), one component per screen. Styling is plain HTML with a few lines of CSS.

## 1. Create RFQ

- `POST /api/rfqs` → `201 {id}`
- Body: `name, bid_start, bid_close, forced_close, service_date, trigger_window, extension_duration, trigger_type`
- `422` if the name is blank, a time has no timezone, start >= close, forced close <= close, X or Y is not between 1 and 1440, or the trigger is unknown
- Store times as UTC ISO with microseconds. `current_close` starts as `bid_close`
- Frontend: `CreateRfq.jsx`, showing API errors. Remove the health route
- Check: a valid RFQ saves; forced close equal to bid close is rejected

## 2. List RFQs

- `GET /api/rfqs` → `[{id, name, lowest_bid, current_close, forced_close, status}]`, newest first
- `auction.py`: `status(rfq, now)`, `ranking(bids)`. `lowest_bid` is the L1 total, or `null`
- Frontend: `RfqList.jsx`, with a table and links to create and details
- Check: all four statuses, including the exact start and close times

## 3. RFQ details

- `GET /api/rfqs/{id}` → `{rfq, status, ranking, bids, logs}`, or `404`
- `ranking` has each supplier's latest bid with its L1, L2... label; `bids` has every bid sorted by price; `logs` is newest first
- Frontend: `RfqDetails.jsx`, polling every 5 seconds
- Check: ties go to the earlier bid; a supplier with several bids is ranked once

## 4. Submit bid

- `POST /api/rfqs/{id}/bids` → `201 {id}`
- Body: `carrier_name, freight_charges, origin_charges, destination_charges, transit_days, valid_until`
- `404` unknown RFQ, `409` not active or not lower than the supplier's last bid, `422` blank carrier, negative or non-finite charge, or zero total
- `auction.py`: `extension(rfq, before, after, now)` → new close time and reason, or `None`
- `BEGIN IMMEDIATE`, then read the time, so a bid that waited for the lock cannot be accepted late
- Frontend: `BidForm.jsx` on the details page, shown only while Active
- Check, with fixed times:
  - 5:49 no extension, 5:50 and 5:55 extend, 6:00 rejected (close 6:00, X = 10)
  - `RANK_CHANGE` and `L1_CHANGE` do not extend when the order or L1 stays the same
  - an extension stops at forced close, and at forced close nothing is logged
  - `Acme` and ` acme ` are the same supplier
  - two simultaneous bids are both processed correctly
