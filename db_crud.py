import operator

from sqlalchemy import delete, create_engine
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
    "ne": operator.ne,
    'like': lambda col, val: col.like(f"%{val}%"),
    'ilike': lambda col, val: col.ilike(f"%{val}%")
}


##############################
# common used function
##############################

def filter_process(table_object, filters: dict[str,str]):
    filters_statement = []
    for key, value in filters.items():
        found = False
        for suffix, op in COMPARATION_SIGN_DICT.items():
            if key.endswith(f"_{suffix}"):
                column_name = key[:-(len(suffix) + 1)]
                column = getattr(table_object, column_name)
                if column is not None:
                    filters_statement.append(op(column, value))
                    found = True
                    break
        if not found:
            column = getattr(table_object, key)
            if column is not None:
                filters_statement.append(column == value)
    return filters_statement


##############################
# table main.raw_scrap_data
##############################

def read_raw_scrap_data(connection_engine, limit: int, offset: int, filters: dict[str,str]):
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        filters_statement = filter_process(raw_scrap_data, filters)
        stmt = session.query(raw_scrap_data)
        if filters_statement:
            stmt = stmt.filter(*filters_statement)
        result = stmt.filter(*filters_statement)
        return result

def delete_raw_scrap_data(connection_engine, filters: dict[str,str]):
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        filters_statement = filter_process(raw_scrap_data ,filters)
        stmt = delete(raw_scrap_data).where(*filters_statement)
        session.execute(stmt)
        session.commit()


if __name__ == "__main__":
    url = create_url(ordinal = 1, database_product = "postgresql")
    engine = create_engine(url)
    filters = {
        "id_lt": "5"
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