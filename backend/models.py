from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Functions for interacting with Supabase tables

def add_machine(name, location):
    response = supabase.table("machines").insert({"name": name, "location": location}).execute()
    return response.data

def get_machines():
    response = supabase.table("machines").select("*").execute()
    return response.data

def add_crop(name, season):
    response = supabase.table("crops").insert({"name": name, "season": season}).execute()
    return response.data

def get_crops():
    response = supabase.table("crops").select("*").execute()
    return response.data

def add_farmer(name, contact):
    response = supabase.table("farmers").insert({"name": name, "contact": contact}).execute()
    return response.data

def get_farmers():
    response = supabase.table("farmers").select("*").execute()
    return response.data
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ------- MACHINES -------

def add_machine(name, location=None, efficiency=None, days_used=None):
    payload = {"name": name}
    if location is not None:
        payload["location"] = location
    if efficiency is not None:
        payload["efficiency"] = efficiency
    if days_used is not None:
        payload["days_used"] = days_used
    return supabase.table("machines").insert(payload).execute().data

def get_machines():
    return supabase.table("machines").select("*").order("created_at", desc=True).execute().data

def get_machine(machine_id):
    return supabase.table("machines").select("*").eq("id", machine_id).single().execute().data

def update_machine(machine_id, fields: dict):
    # Only allow known columns; ignore others
    allowed = {"name", "location", "efficiency", "days_used", "status"}
    clean = {k: v for k, v in (fields or {}).items() if k in allowed}
    if not clean:
        return None
    return supabase.table("machines").update(clean).eq("id", machine_id).execute().data

def delete_machine(machine_id):
    supabase.table("machines").delete().eq("id", machine_id).execute()
    return True
