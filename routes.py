from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from db_connection import engine
from db_crud import read_raw_scrap_data


data_bp = Blueprint("data", __name__, url_prefix = "/data")

@data_bp.route("/raw-scrap-data", methods = ["GET"])
def get_raw_scrap_data():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 100))
        offset = (page - 1) * limit
        filters = request.args.to_dict()
        filters.pop("page", None)
        filters.pop("limit", None)
        products = read_raw_scrap_data(connection_engine = engine, limit = limit, offset = offset, **filters)
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
                "createdate": product.createdate.isoformat() if product.createdate else None
            })
        return jsonify({
            "page": page,
            "limit": limit,
            "data": result
        })
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
