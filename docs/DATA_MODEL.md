# Data Model

## Core Entities

### companies

- company_id
- ticker
- name
- sector
- industry
- country
- market_cap
- created_at
- updated_at

### documents

- document_id
- source
- source_type
- url
- title
- content
- published_at
- ingested_at
- checksum
- language
- metadata

### events

- event_id
- company_id
- event_type
- event_date
- sentiment
- confidence
- importance
- summary
- created_at

### event_documents

- event_id
- document_id

### signals

- signal_id
- company_id
- signal_type
- strength
- confidence
- created_at

### opportunities

- opportunity_id
- company_id
- score
- reason
- confidence
- generated_at

### risks

- risk_id
- company_id
- score
- reason
- confidence
- generated_at

### insights

- insight_id
- title
- summary
- confidence
- importance
- created_at

## Search Indices

- documents
- events
- insights
- companies
- daily_reports
- chat_memory
