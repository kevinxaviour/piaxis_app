# Task 2: RLS

## Setup Instructions

### Open task_2 folder
1. Run setup_rls.sql in Supabase SQL Editor
2. Create .env file:
   DATABASE_URL=postgresql://postgres:PASSWORD@db.REF.supabase.co:5432/postgres
3. pip install -r requirements.txt
4. uvicorn main:app --reload
5. Open http://localhost:8000/docs

## How to Switch Users / Roles

Pass x-user-email header to /secure/details:

  admin@piaxis.com   → admin     → 3 rows (all)
  kevin@piaxis.com   → architect → 3 rows (standard + owns id=3)
  naveen@piaxis.com     → architect → 2 rows (standard only)

curl examples:
  curl http://localhost:8000/secure/details -H "x-user-email: admin@piaxis.com"
  curl http://localhost:8000/secure/details -H "x-user-email: kevin@piaxis.com"
  curl http://localhost:8000/secure/details -H "x-user-email: naveen@piaxis.com"

## RLS Policies Explanation

ENABLE ROW LEVEL SECURITY → turns on RLS for the details table
FORCE ROW LEVEL SECURITY  → applies to Supabase superuser too

Policy rls_details_access has 4 rules:

1. admin     → true          → sees everything
2. architect → standard      → sees all rows where source = 'standard'
3. architect → user_project  → sees user_project rows where owner_id = their id
4. no role   → false         → sees nothing (secure by default)

Python never writes WHERE clauses for role filtering.
PostgreSQL enforces access rules automatically through the policy.
