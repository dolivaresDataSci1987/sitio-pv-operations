import streamlit as st
from supabase import create_client

@st.cache_resource
def db():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_SERVICE_ROLE_KEY"])

def rows(table):
    return db().table(table).select("*").order("created_at",desc=True).execute().data or []

def update_project(project_id, values):
    return db().table("projects").update(values).eq("id",project_id).execute()

def requests():
    return rows("client_requests")

def projects():
    return rows("projects")

def safety():
    return rows("client_safety_intake")
