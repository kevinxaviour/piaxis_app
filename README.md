# PiAxis Assgnment

### This project demonstrates:

- Backend API development
- Secure data access using PostgreSQL RLS
- Role-based data isolation
- Unified frontend interface
- Production deployment using Render

---

# Live Demo
- [Streamlit App](https://piaxisapp-ui.streamlit.app/)
- [Task 1 API Docs](https://piaxis-app.onrender.com/docs)
- [Task 2 API Docs](https://piaxis-t2.onrender.com/docs)

---

# Deployment Note

The backend services are deployed using **Render’s free tier**, which automatically suspends services after 15 minutes of inactivity.

On the first request after inactivity, there may be a **cold start delay (~1–2 minutes)** while the backend restarts.

---

# System Architecture

Frontend (Streamlit)  
⬇  
FastAPI Backend  
⬇  
PostgreSQL (Supabase with RLS)

### Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Database**: PostgreSQL (Supabase)
- **Security**: PostgreSQL Row-Level Security (RLS)
- **Deployment**: Render

---

# Task 1: Mini Detail Library App

## Setup Instructions

### [Open backend folder](https://github.com/kevinxaviour/piaxis_app/tree/0c7f25ce677c377a6e7e6dc5905c43aa90374941/backend)
1. Run superbase_setup.sql in Supabase SQL Editor
2. Create .env file:
   DATABASE_URL="postgresql://postgres:PASSWORD@db.REF.supabase.co:5432/postgres"
3. pip install -r requirements.txt
4. uvicorn main:app --reload
5. Open http://localhost:8000/docs

---

# Task 2: RLS

## Setup Instructions

### [Open task_2 folder](https://github.com/kevinxaviour/piaxis_app/tree/0c7f25ce677c377a6e7e6dc5905c43aa90374941/task_2)
1. Run setup_rls.sql in Supabase SQL Editor
2. Create .env file:
   DATABASE_URL="postgresql://postgres:PASSWORD@db.REF.supabase.co:5432/postgres"
3. pip install -r requirements.txt
4. uvicorn main:app --reload
5. Open http://localhost:8000/docs

## How to Switch Users / Roles

- Pass x-user-email header to /secure/details:
   - admin@piaxis.com   → admin     → 3 rows (all)
   - kevin@piaxis.com   → architect → 3 rows (standard + owns id=3)
   - naveen@piaxis.com     → architect → 2 rows (standard only)

- curl examples:
   - curl http://localhost:8000/secure/details -H "x-user-email: admin@piaxis.com"
   - curl http://localhost:8000/secure/details -H "x-user-email: kevin@piaxis.com"
   - curl http://localhost:8000/secure/details -H "x-user-email: naveen@piaxis.com"

## RLS Policies Explanation

- ENABLE ROW LEVEL SECURITY → turns on RLS for the details table
- FORCE ROW LEVEL SECURITY  → applies to Supabase superuser too

Policy rls_details_access has 4 rules:
1. admin     → true          → sees everything
2. architect → standard      → sees all rows where source = 'standard'
3. architect → user_project  → sees user_project rows where owner_id = their id
4. no role   → false         → sees nothing (secure by default)

## RLS Policy for Each Table

- Table: details
   - ALTER TABLE details ENABLE ROW LEVEL SECURITY;
   - ALTER TABLE details FORCE ROW LEVEL SECURITY;

Policy: rls_details_access

CREATE POLICY rls_details_access
    ON details FOR SELECT
    USING (
        CASE current_setting('app.current_user_role', true)
            WHEN 'admin'     THEN true
            WHEN 'architect' THEN (
                source = 'standard'
                OR (source = 'user_project' AND owner_id = current_setting('app.current_user_id', true)::INT)
            )
            ELSE false
        END
    );


Table: users
No RLS applied. Only accessed internally by the API.
