from flask import Blueprint, request, jsonify
from config import supabase

machine_bp = Blueprint("machines", __name__)

@machine_bp.route("/", methods=["GET"])
def get_machines():
    response = supabase.table("machines").select("*").execute()
    return jsonify(response.data), 200

@machine_bp.route("/", methods=["POST"])
def add_machine():
    data = request.json
    response = supabase.table("machines").insert(data).execute()
    return jsonify({"message": "Machine added", "data": response.data}), 201
