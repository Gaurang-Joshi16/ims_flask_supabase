from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("⚠️ Missing SUPABASE_URL or SUPABASE_KEY in environment variables")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Function to insert a new user
def insert_user(username, password, re_password, address, contact_no):
    try:
        response = supabase.table("users").insert({
            "username": username,
            "password": password,
            "re_password": re_password,
            "address": address,
            "contact_no": contact_no
        }).execute()

        if response.data:
            print("✅ User inserted successfully:", response.data)
            return True
        else:
            print("⚠️ Failed to insert user:", response)
            return False

    except Exception as e:
        print("⚠️ Error inserting user:", str(e))
        return False
