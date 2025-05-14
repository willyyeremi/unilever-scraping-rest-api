from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from db_connection import engine
from db_crud import read_raw_scrap_data


data = Blueprint("data", __name__)

@data.route("/", methods = ["GET"])
def get_raw_scrap_data():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 100))
        offset = (page - 1) * limit
        filters = request.args.to_dict()
        filters.pop("page", None)
        filters.pop("limit", None)
        games = read_raw_scrap_data(connection_engine = engine, limit = limit, offset = offset, **filters)
        result = []
        for game in games:
            result.append({
                "id": game.id,
                "name": game.name,
                "detail": game.detail,
                "price": game.price,
                "originalprice": game.originalprice,
                "discountpercentage": game.discountpercentage,
                "platform": game.platform,
                "createdate": game.createdate.isoformat() if game.createdate else None
            })
        return jsonify({
            "page": page,
            "limit": limit,
            "data": result
        })
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500
