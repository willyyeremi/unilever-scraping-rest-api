import operator

from sqlalchemy import create_engine, delete, or_, and_
from sqlalchemy.orm import Session

from db_object import raw_scrap_data
from db_connection import create_url


##############################
# common used variable
##############################

COMPARATION_SIGN_DICT = {
    "lt": operator.lt,
    "lte": operator.le,
    "gt": operator.gt,
    "gte": operator.ge,
    "eq": operator.eq,
    "ne": operator.ne,
    'like': lambda col, val: col.like(f"%{val}%"),
    'ilike': lambda col, val: col.ilike(f"%{val}%"),
    "in": lambda col, val: col.in_(val),
}


##############################
# common used function
##############################

def filter_process(table_object, filters):
    filters_statement = []
    for key, value in filters.items():
        if key in ("and", "or"):
            sub_filter = filter_process(table_object, value)
            if sub_filter:
                filters_statement.append(and_(*sub_filter) if key == "and" else or_(*sub_filter))
        else:
            matched = False
            for op in COMPARATION_SIGN_DICT:
                suffix = f"_{op}"
                if key.endswith(suffix):
                    column_name = key[:-len(suffix)]
                    column = getattr(table_object, column_name)
                    func = COMPARATION_SIGN_DICT[op]
                    filters_statement.append(func(column, value))
                    matched = True
                    break
            if not matched:
                column = getattr(table_object, key)
                for op, val in value.items():
                    func = COMPARATION_SIGN_DICT[op]
                    if op in ("like", "ilike") and isinstance(val, list):
                        filters_statement.append(or_(*[func(column, v) for v in val]))
                    else:
                        filters_statement.append(func(column, val))
    return filters_statement


##############################
# table main.raw_scrap_data
##############################

def read_raw_scrap_data(connection_engine, limit: int, offset: int, filters):
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        filters_statement = filter_process(raw_scrap_data, filters)
        stmt = session.query(raw_scrap_data)
        if filters_statement:
            stmt = stmt.filter(*filters_statement)
        result = stmt.limit(limit).offset(offset)
        return result

def delete_raw_scrap_data(connection_engine, filters: dict):
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        filters_statement = filter_process(raw_scrap_data ,filters)
        stmt = delete(raw_scrap_data).where(*filters_statement)
        session.execute(stmt)
        session.commit()


if __name__ == "__main__":
    url = create_url(ordinal = 1, database_product = "postgresql")
    engine = create_engine(url)
    filters = {
        "and": {
            "name": {
                "like": ["%Sampo%", "%Sabun%"]
            },
            "and" : {
                "price_gte": 100000,
                "price_lte": 500000,
            },
            "or": {
                "originalprice_gt": 10000,
                "discountpercentage_gte": 5.0,
                "platform": {
                    "in": ["tokopedia", "blibli"]
                },
            },
        },
    }
    products = read_raw_scrap_data(engine, 5, 0, filters)
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
    for item in result:
        print(item)
    delete_raw_scrap_data(engine, filters)