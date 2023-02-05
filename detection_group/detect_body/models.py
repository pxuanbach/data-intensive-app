from sqlalchemy import Column, DateTime
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Text, Float

from db import Base


class DetectModel(Base):
    __tablename__ = "detect_body"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    img_id = Column(Integer)
    x = Column(Float)
    y = Column(Float)
    width_of_obj = Column(Float)
    height_of_obj = Column(Float)
    width_of_img = Column(Float)
    height_of_img = Column(Float)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
