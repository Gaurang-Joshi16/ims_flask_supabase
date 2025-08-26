import os
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nerzmbcilthokuyqmtwj.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lcnptYmNpbHRob2t1eXFtdHdqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU4MDUzMjEsImV4cCI6MjA3MTM4MTMyMX0.HBou9bR3fezEuklwXmgH7cMLMwzPXH-ndm325TbkTIM")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
