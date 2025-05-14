from sqlalchemy.orm import Session

from db_connection import engine
from db_object import raw_scrap_data


def read_raw_scrap_data(connection_engine, limit: int, offset: int, **kwargs):
    with Session(autocommit = False, autoflush = False, bind = connection_engine) as session:
        if kwargs.items():
            result = session.query(raw_scrap_data).filter_by(**kwargs).limit(limit).offset(offset)
        else:
            result = session.query(raw_scrap_data).limit(limit).offset(offset)
    return result


if __name__ == "__main__":
    print(read_raw_scrap_data(connection_engine = engine, limit = 1, offset = 5, id = 1))
    print(read_raw_scrap_data(connection_engine = engine, limit = 1, offset = 5))