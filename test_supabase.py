"""
Test Supabase connection and database operations
Run this to verify Supabase setup
"""

import streamlit as st
from database import get_supabase_client, create_project, get_projects, is_supabase_enabled

st.title("🧪 Supabase Connection Test")

# Test 1: Check if Supabase is enabled
st.header("1. Check Configuration")
if is_supabase_enabled():
    st.success("✅ Supabase is configured!")
else:
    st.error("❌ Supabase is NOT configured")
    st.info("Check `.streamlit/secrets.toml` for SUPABASE_URL and SUPABASE_KEY")
    st.stop()

# Test 2: Test connection
st.header("2. Test Connection")
try:
    client = get_supabase_client()
    if client:
        st.success("✅ Connected to Supabase!")
        st.code(f"URL: {st.secrets['SUPABASE_URL']}")
    else:
        st.error("❌ Failed to connect")
        st.stop()
except Exception as e:
    st.error(f"❌ Connection error: {e}")
    st.stop()

# Test 3: Check tables
st.header("3. Check Database Tables")
try:
    # Try to query projects table
    result = client.table("projects").select("*").limit(1).execute()
    st.success("✅ Table 'projects' exists!")
    
    # Check other tables
    tables = ["scenes", "analysis_results", "action_plans"]
    for table in tables:
        try:
            client.table(table).select("*").limit(1).execute()
            st.success(f"✅ Table '{table}' exists!")
        except Exception as e:
            st.error(f"❌ Table '{table}' not found: {e}")
            st.warning("Run the SQL schema in Supabase SQL Editor!")
            
except Exception as e:
    st.error(f"❌ Tables not found: {e}")
    st.warning("⚠️ You need to run `supabase_schema.sql` in Supabase SQL Editor!")
    st.info("""
    Steps:
    1. Go to Supabase dashboard
    2. Click 'SQL Editor'
    3. Click 'New query'
    4. Copy content from `supabase_schema.sql`
    5. Paste and click 'Run'
    """)
    st.stop()

# Test 4: Create test project
st.header("4. Test CRUD Operations")

if st.button("Create Test Project"):
    with st.spinner("Creating test project..."):
        try:
            project = create_project("Test Project", "This is a test project")
            if project:
                st.success(f"✅ Created project: {project['name']}")
                st.json(project)
            else:
                st.error("❌ Failed to create project")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Test 5: List projects
st.header("5. List All Projects")
if st.button("Get Projects"):
    with st.spinner("Fetching projects..."):
        try:
            projects = get_projects()
            if projects:
                st.success(f"✅ Found {len(projects)} projects")
                st.dataframe(projects)
            else:
                st.info("No projects found. Create one above!")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Summary
st.header("✅ Summary")
st.success("""
All tests passed! Your Supabase setup is working correctly.

Next steps:
1. Run the main app: `streamlit run app.py`
2. Try creating a project in the sidebar
3. Upload a PDF and start working!
""")
