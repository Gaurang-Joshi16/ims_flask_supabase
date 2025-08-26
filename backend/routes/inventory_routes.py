from flask import Blueprint, request, jsonify
from config import supabase

inventory_bp = Blueprint("inventory", __name__)

@inventory_bp.route("/", methods=["GET"])
def get_inventory():
    response = supabase.table("inventory").select("*").execute()
    return jsonify(response.data), 200

@inventory_bp.route("/", methods=["POST"])
def add_item():
    data = request.json
    response = supabase.table("inventory").insert(data).execute()
    return jsonify({"message": "Item added", "data": response.data}), 201
