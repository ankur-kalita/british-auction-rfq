# Database Design

SQL: [schema.sql](../backend/schema.sql)

```mermaid
erDiagram
    rfqs ||--o{ bids : has
    rfqs ||--o{ activity_logs : has
    rfqs {
        int id PK
        text name
        text bid_start
        text bid_close "original close"
        text current_close "moves on extension"
        text forced_close
        text service_date
        int trigger_window "X minutes"
        int extension_duration "Y minutes"
        text trigger_type
    }
    bids {
        int id PK
        int rfq_id FK
        text carrier_name
        real freight_charges
        real origin_charges
        real destination_charges
        real total
        int transit_days
        text valid_until
        text created_at
    }
    activity_logs {
        int id PK
        int rfq_id FK
        text type "BID or EXTENSION"
        text message
        text created_at
    }
```

- Times are UTC ISO strings in one fixed format, so they compare correctly as text.
- Bids are never updated. Ranking uses each supplier's latest row.
- Status is computed, not stored.
