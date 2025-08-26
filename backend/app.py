from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from supabase import create_client, Client
import os
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nerzmbcilthokuyqmtwj.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lcnptYmNpbHRob2t1eXFtdHdqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU4MDUzMjEsImV4cCI6MjA3MTM4MTMyMX0.HBou9bR3fezEuklwXmgH7cMLMwzPXH-ndm325TbkTIM")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


from flask import Flask, request, jsonify, render_template, redirect, url_for, session


import re
import hashlib



# Import models
from models import (
    get_machines, add_machine, get_machine, update_machine, delete_machine,
    get_crops, add_crop, get_farmers, add_farmer
)

# Import Auth Blueprint
try:
    from routes.auth_routes import auth_bp  
except Exception as e:
    print("❌ Error importing auth_routes:", str(e))
    auth_bp = None

# Load environment variables
load_dotenv()

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# ---------------- Home ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "✅ Inventory Management System API running with Supabase!"})


# ---------------- Machines ----------------

@app.route("/machines", methods=["GET"])
def machines_list():
    try:
        response = supabase.table("machines").select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/machines/<machine_id>", methods=["GET"])
def machine_detail(machine_id):
    try:
        response = supabase.table("machines").select("*").eq("id", machine_id).execute()
        if not response.data:
            return jsonify({"error": "Machine not found"}), 404
        return jsonify(response.data[0]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/machines", methods=["POST"])
def machines_create():
    data = request.get_json(force=True)

    if not data or "name" not in data or "type" not in data:
        return jsonify({"error": "Both 'name' and 'type' are required"}), 400

    new_machine = {
        "name": data["name"],
        "type": data["type"],
        "status": data.get("status", "Available"),
        "location": data.get("location"),
        "description": data.get("description"),
        "created_by": data.get("created_by")  # If handling auth, set this via JWT
    }

    try:
        response = supabase.table("machines").insert(new_machine).execute()
        return jsonify(response.data[0]), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/machines/<machine_id>", methods=["PUT"])
def machines_update(machine_id):
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "Update data required"}), 400

    try:
        response = supabase.table("machines").update(data).eq("id", machine_id).execute()
        if not response.data:
            return jsonify({"error": "Machine not found"}), 404
        return jsonify(response.data[0]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/machines/<machine_id>", methods=["DELETE"])
def machines_delete(machine_id):
    try:
        response = supabase.table("machines").delete().eq("id", machine_id).execute()
        if not response.data:
            return jsonify({"error": "Machine not found"}), 404
        return jsonify({"message": "Machine deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route("/machines/<machine_id>/reports", methods=["GET"])
def machine_reports(machine_id):
    try:
        # Fetch machine data
        response = supabase.table("machines").select("*").eq("id", machine_id).execute()
        if not response.data:
            return jsonify({"error": "Machine not found"}), 404
        machine = response.data[0]

        # If these fields exist in the DB, return them; else use defaults
        reports = {
            "efficiency": machine.get("efficiency", 80),
            "uptime": machine.get("uptime", 90),
            "downtime": machine.get("downtime", 10),
            "tasks_completed": machine.get("tasks_completed", 50)
        }
        return jsonify(reports), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------- Crops ----------------
@app.route("/crops", methods=["GET"])
def crops_list():
    try:
        return jsonify(get_crops())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/crops", methods=["POST"])
def crops_create():
    data = request.get_json(force=True)
    if not data or "name" not in data or "season" not in data:
        return jsonify({"error": "Crop name and season are required"}), 400

    try:
        created = add_crop(data["name"], data["season"])
        return jsonify(created), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# # ---------------- Farmers ----------------
# @app.route("/farmers", methods=["GET"])
# def farmers_list():
#     try:
#         return jsonify(get_farmers())
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# @app.route("/farmers", methods=["POST"])
# def farmers_create():
#     data = request.get_json(force=True)
#     if not data or "name" not in data or "contact" not in data:
#         return jsonify({"error": "Farmer name and contact are required"}), 400

#     try:
#         created = add_farmer(data["name"], data["contact"])
#         return jsonify(created), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
@app.route('/manager_dashboard')
def manager_dashboard():
    if 'username' in session and session['role'] == 'manager':
        return render_template('manager_dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/employee_dashboard')
def employee_dashboard():
    if 'username' in session and session['role'] == 'employee':
        return render_template('employee_dashboard.html', username=session['username'])
    return redirect(url_for('login'))





# ---------------- Register Blueprints ----------------
if auth_bp:
    app.register_blueprint(auth_bp, url_prefix="/auth")
    print("✅ Auth blueprint registered at /auth")
else:
    print("⚠️ Auth blueprint not found, check routes/auth_routes.py")


# ---------------- Run ----------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
