# RetailPulse

## E-Commerce Product Analytics Platform

RetailPulse is a SQL-driven e-commerce analytics project built to demonstrate how Product Analysts evaluate customer behavior, conversion, revenue, product performance, and experiments.

The project uses simulated customer event data stored in PostgreSQL, analyzed with SQL and Python, and displayed through an interactive Streamlit dashboard.

---

## Tech Stack

- PostgreSQL
- SQL
- Python
- pandas
- SQLAlchemy
- Streamlit
- Git / GitHub

Future phases will add statistical testing for A/B experiments.

---

# Current Architecture

```text
Customer Event Data
        |
        v
   PostgreSQL
        |
        v
    SQL Analysis
        |
        v
 Python / Pandas
        |
        v
    Streamlit
        |
        v
 Product Insights
```

---

# Phase 1: Foundation + MVP

**Status: Complete**

Phase 1 created the core data pipeline and first working version of RetailPulse.

### Implemented

- Generated simulated e-commerce customer events
- Stored event data in PostgreSQL
- Connected Python to PostgreSQL
- Built SQL-driven KPI calculations
- Created the first Streamlit dashboard

### Customer Journey

```text
Homepage
   ↓
Product View
   ↓
Add to Cart
   ↓
Checkout
   ↓
Purchase
```

### Initial KPIs

- Sessions
- Purchases
- Conversion Rate
- Revenue

Phase 1 answered:

> **What happened?**

---

# Phase 2: Product Analytics

**Status: Complete**

Phase 2 expanded RetailPulse into a more complete product analytics platform.

### Core Features

#### Performance Overview
Tracks:

- Sessions
- Purchases
- Conversion Rate
- Revenue
- Average Order Value
- Revenue per Session
- Daily Conversion
- Daily Revenue

#### Conversion Funnel
Measures:

- Users at each funnel stage
- Stage-to-stage conversion
- Overall conversion
- Drop-off volume
- Drop-off percentage

#### Device Analysis
Compares:

- Mobile
- Desktop
- Tablet

Using:

- Sessions
- Purchases
- Conversion
- Revenue
- AOV
- Revenue per Session

#### Product Analysis
Tracks:

- Product Views
- Add-to-Cart Sessions
- Purchases
- Revenue
- View-to-Cart Rate
- View-to-Purchase Rate
- Revenue Ranking

#### Customer Segmentation
Customers are grouped as:

- Browser
- One-Time Buyer
- Repeat Buyer

---

## SQL Skills Demonstrated

- CTEs
- `CASE`
- `GROUP BY`
- `COUNT(DISTINCT)`
- Conditional aggregation
- `NULLIF`
- Date aggregation
- Window functions
- `LAG`
- `DENSE_RANK`

The analysis operates across:

- Event-level data
- Session-level data
- Customer-level data

---

# Current Product Finding

The largest customer drop-off occurs between:

```text
Product View
      ↓
Add to Cart
```

### Potential Causes

- Pricing
- Product information
- Shipping uncertainty
- Reviews
- Product imagery
- Inventory or size availability
- CTA visibility

These are possible explanations, not confirmed causes.

### Product Hypothesis

> Providing clearer value or purchasing information on product pages may improve Add-to-Cart conversion.

This hypothesis will be tested in Phase 3.

---

# Project Progress

```text
Phase 1: Foundation + MVP
COMPLETE

Phase 2: Product Analytics
COMPLETE

Phase 3: A/B Testing
NEXT

Phase 4: Product Insights Dashboard
PLANNED

Phase 5: Portfolio Case Study
PLANNED
```

---

# Phase 3: A/B Testing

The next phase will test whether a product-page change improves Add-to-Cart conversion.

Planned implementation:

- Control and treatment groups
- Experiment assignment
- Primary and secondary KPIs
- Conversion lift
- Revenue impact
- Statistical significance
- Confidence intervals
- Device-level experiment analysis

Phase 3 will answer:

> **Can a product change improve the identified funnel problem?**

---

# Phase 4: Product Decision Dashboard

Phase 4 will make the application more interactive and decision-focused.

Planned additions:

- Date filters
- Device filters
- Product filters
- Experiment filters
- Control vs. treatment comparison
- KPI lift
- Revenue impact
- Funnel comparison
- Product recommendations

The goal is to connect analysis directly to product decisions.

---

# Phase 5: Portfolio Case Study

The final phase will prepare RetailPulse as a complete portfolio project.

Final deliverables will include:

- Polished README
- Architecture overview
- KPI framework
- Funnel findings
- Experiment results
- Product recommendations
- Screenshots
- Resume bullets
- Interview talking points
- Limitations and future improvements

---

# Final Project Goal

RetailPulse is designed to demonstrate the full Product Analytics workflow:

```text
Customer Behavior
        ↓
SQL Analysis
        ↓
Product KPIs
        ↓
Funnel Investigation
        ↓
Product Hypothesis
        ↓
A/B Experiment
        ↓
Statistical Analysis
        ↓
Business Impact
        ↓
Product Recommendation
```

The project currently has the data foundation and product analysis layers complete. The next step is experimentation.