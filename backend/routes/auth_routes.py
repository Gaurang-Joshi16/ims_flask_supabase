from flask import Blueprint, request, jsonify
from db import supabase  # using your db.py connection
from db import insert_user 
from werkzeug.security import generate_password_hash, check_password_hash
auth_bp = Blueprint("auth", __name__)

# ------------------- SIGNUP -------------------
@auth_bp.route("/signup", methods=["POST"])

def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    re_password = data.get("re_password")
    address = data.get("address")
    contact_no = data.get("contact_no")
    role = data.get("role")

    if not username or not password or not re_password or not role:
        return jsonify({"error": "Username, password, re_password, and role are required"}), 400

    if password != re_password:
        return jsonify({"error": "Passwords do not match"}), 400

    try:
        # check if username already exists
        existing_user = supabase.table("users").select("*").eq("username", username).execute()
        if existing_user.data:
            return jsonify({"error": "Username already exists"}), 400

        # check if contact number already exists
        if contact_no:
            existing_contact = supabase.table("users").select("*").eq("contact_no", contact_no).execute()
            if existing_contact.data:
                return jsonify({"error": "Contact number already registered"}), 400

        # ✅ Hash password before storing
        hashed_password = generate_password_hash(password)

        # insert user with role
        response = supabase.table("users").insert({
            "username": username,
            "password": hashed_password,   # store only hashed password
            "address": address,
            "contact_no": contact_no,
            "role": role
        }).execute()

        return jsonify({"message": "Signup successful", "user": response.data}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------------------- LOGIN -------------------
# @auth_bp.route("/login", methods=["POST"])
# def login():
#     data = request.json
#     username = data.get("username")
#     password = data.get("password")

#     if not username or not password:
#         return jsonify({"error": "Username and password required"}), 400

#     try:
#         user = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()

#         if not user.data:
#             return jsonify({"error": "Invalid username or password"}), 401

#         return jsonify({"message": "Login successful", "user": user.data[0]}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password required"}), 400

    try:
        # get user by username only
        result = supabase.table("users").select("*").eq("username", username).execute()

        if not result.data:
            return jsonify({"success": False, "message": "Invalid username or password"}), 401

        user = result.data[0]

        # ✅ Check hashed password
        if not check_password_hash(user["password"], password):
            return jsonify({"success": False, "message": "Invalid username or password"}), 401

        # ✅ Role-based redirect
        role = user.get("role", "employee")  # default to employee if not found
        if role == "manager":
            redirect_url = "/manager/dashboard"
        else:
            redirect_url = "/employee/dashboard"

        return jsonify({
            "success": True,
            "message": "Login successful",
            "redirect_url": redirect_url,
            "user": {"username": user["username"], "role": role}
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

