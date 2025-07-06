from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import create_engine

from db_connection import create_url
from db_crud import create_tr_raw_scrap_data, read_tr_raw_scrap_data, update_tr_raw_scrap_data, delete_tr_raw_scrap_data


##############################
# common used variable
##############################

url = create_url(ordinal = 1, database_product = "postgresql")
engine = create_engine(url)

data_bp = Blueprint("data", __name__, url_prefix = "/data")


##############################
# routing function
##############################

@data_bp.route("/tr-raw-scrap-data", methods = ["POST"])
@jwt_required()
def method_post_tr_raw_scrap_data():
    try:
        data = request.get_data()
        create_tr_raw_scrap_data(connection_engine = engine, data = data)
        return jsonify({"msg": "Insert success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@data_bp.route("/tr-raw-scrap-data", methods = ["GET"])
@jwt_required()
def method_get_tr_raw_scrap_data():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 100))
        offset = (page - 1) * limit
        filters = request.get_data()
        products = read_tr_raw_scrap_data(connection_engine = engine, limit = limit, offset = offset, filters = filters)
        result = []
        for product in products:
            result.append({
                "id": product.id,
                "name": product.name,
                "detail": product.detail,
                "price": product.price,
                "originalprice": product.originalprice,
                "discountpercentage": product.discountpercentage,
                "platform": product.platform,
                "createdate": product.createdate.isoformat()
            })
        return jsonify({
            "page": page,
            "limit": limit,
            "data": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@data_bp.route("/tr-raw-scrap-data", methods = ["put"])
@jwt_required()
def method_put_tr_raw_scrap_data():
    raise NotImplementedError

@data_bp.route("/tr-raw-scrap-data", methods = ["DELETE"])
@jwt_required()
def method_delete_tr_raw_scrap_data():
    try:
        filters = request.args.to_dict()
        if len(filters) == 0:
            return jsonify({"msg": "Please specify delete filters"}), 401
        delete_tr_raw_scrap_data(connection_engine = engine, filters = filters)
        return jsonify({"msg": "Delete success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
