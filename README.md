# CDSS-NURSE-MANAGER

A FastAPI-based Clinical Decision Support System (CDSS) for managing hospital nursing staff and supporting safer shift planning through rule-based workload and rest-period assessment.

## Overview

**CDSS-NURSE-MANAGER** is a backend application designed to support nurse workforce management in hospital environments.

The system combines a RESTful API with a relational database to manage nurse records and provide basic decision-support functions related to:

* Weekly workload and overtime risk
* Nurse rest-period eligibility
* Burnout risk assessment
* Shift assignment support
* Structured nurse data management

The project is intended as a foundation for a larger clinical decision-support platform that can be extended with advanced scheduling algorithms, additional clinical/workforce rules, authentication, audit logging, and data analytics.

## Key Features

### Nurse Management

The API provides CRUD operations for nurse records.

Each nurse can be associated with:

* Name
* Department
* Education level
* Years of experience
* Weekly working hours
* Last shift date

### Rule-Based Decision Support

The project currently implements several basic CDSS rules.

#### 1. Overtime & Burnout Risk

Nurses working more than **40 hours per week** are identified as being at potential overtime/burnout risk.

Risk levels are evaluated as:

| Weekly Hours | Risk Level | Recommendation                    |
| ------------ | ---------- | --------------------------------- |
| `< 40`       | LOW        | Eligible for shift assignment     |
| `> 40`       | MEDIUM     | Consider reducing shift hours     |
| `>= 48`      | HIGH       | Immediate rest period recommended |

#### 2. Mandatory Rest Period Control

The system evaluates whether a nurse has completed the required rest period since their previous shift.

By default, a minimum rest period of **one day** is used.

#### 3. Burnout Risk Assessment

The system generates a structured risk assessment containing:

* Nurse ID
* Nurse name
* Weekly working hours
* Risk level
* Scheduling recommendation

These rules are implemented as service-layer functions and can be extended with additional decision-support criteria.

## Technology Stack

* **Python**
* **FastAPI** — REST API framework
* **Pydantic** — Data validation and API schemas
* **SQLAlchemy** — ORM and database interaction
* **PostgreSQL** — Relational database
* **python-dotenv** — Environment variable management
* **Uvicorn** — ASGI application server

## Project Structure

```text
CDSS-NURSE-MANAGER/
│
├── main.py          # FastAPI application and API endpoints
├── database.py      # Database configuration and session management
├── models.py        # SQLAlchemy database models
├── schemas.py       # Pydantic request/response schemas
├── services.py      # CDSS decision-support rules
├── .env             # Environment configuration (do not commit)
└── README.md
```

## API Endpoints

### Root

```http
GET /
```

Returns a basic API status message and points users to the interactive documentation.

### Nurses

#### Get all nurses

```http
GET /nurses/
```

Returns all registered nurses.

#### Get a nurse

```http
GET /nurses/{nurse_id}
```

Returns a specific nurse by ID.

#### Create a nurse

```http
POST /nurses/
```

Example request:

```json
{
  "name": "Jane Doe",
  "department": "Emergency",
  "education_level": "Bachelor's Degree",
  "experience_years": 5,
  "weekly_hours": 40,
  "last_shift_date": "2026-10-01"
}
```

#### Update a nurse

```http
PUT /nurses/{nurse_id}
```

Updates the information associated with an existing nurse.

#### Delete a nurse

```http
DELETE /nurses/{nurse_id}
```

Deletes a nurse record from the database.

## Interactive API Documentation

FastAPI automatically provides interactive API documentation.

After starting the application, open:

```text
http://127.0.0.1:8000/docs
```

The alternative OpenAPI documentation interface is available at:

```text
http://127.0.0.1:8000/redoc
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/CDSS-NURSE-MANAGER.git
cd CDSS-NURSE-MANAGER
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

Install the required packages:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic
```

### 4. Configure the database

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST/DATABASE?sslmode=require
```

Do **not** commit `.env` to GitHub.

Add it to `.gitignore`:

```gitignore
.env
__pycache__/
.venv/
*.pyc
```

### 5. Start the application

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## Database

The application uses PostgreSQL through SQLAlchemy.

The database schema is automatically initialized when the application starts:

```python
models.Base.metadata.create_all(bind=engine)
```

The primary database table is:

```text
nurses
```

with fields including:

```text
id
name
department
education_level
experience_years
weekly_hours
last_shift_date
```

## CDSS Architecture

The project follows a simple layered architecture:

```text
             Client
               │
               ▼
        ┌───────────────┐
        │    FastAPI    │
        │   REST API    │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │    Schemas    │
        │   Pydantic    │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │    Services   │
        │  CDSS Rules   │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │   SQLAlchemy  │
        │      ORM      │
        └───────┬───────┘
                │
                ▼
        ┌───────────────┐
        │  PostgreSQL   │
        └───────────────┘
```

This separation allows the decision-support logic to evolve independently from the API and database layers.

## Current Scope

The current version focuses on the backend foundation and rule-based decision support.

The project can be further developed with features such as:

* Automated nurse shift scheduling
* Constraint-based scheduling
* Advanced burnout prediction
* Staff shortage detection
* Department-level workload analysis
* Shift conflict detection
* Nurse availability management
* Authentication and role-based authorization
* Audit trails for clinical/workforce decisions
* Dashboard and data visualization
* Machine learning-based risk prediction
* Explainable AI for CDSS recommendations
* Hospital information system integration

## Future Development

A potential next stage of the project is to evolve the current rule-based system into a more comprehensive decision-support platform.

Possible future architecture:

```text
                   ┌─────────────────────┐
                   │   Hospital Data     │
                   │   / Staff Records   │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │   Data Validation   │
                   └──────────┬──────────┘
                              │
                              ▼
              ┌───────────────────────────────┐
              │       CDSS Engine             │
              │                               │
              │  • Workload Rules             │
              │  • Rest Constraints           │
              │  • Staffing Requirements      │
              │  • Risk Prediction            │
              │  • Scheduling Optimization    │
              └───────────────┬───────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Decision Support    │
                   │ Recommendations     │
                   └─────────────────────┘
```

## Disclaimer

> **Disclaimer:** This software is a research and educational project and is **not a medical device or a substitute for professional clinical judgment**. Its recommendations are based on simplified rules and should not be used as the sole basis for clinical, staffing, or patient-care decisions. Always validate system outputs with qualified healthcare professionals and applicable institutional policies and regulations.

## License

This project is provided for research and educational purposes. A specific open-source license should be added to the repository if redistribution or commercial use is intended.
