from sqlalchemy import Column, DateTime
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Text

from db import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    img_url = Column(Text)
    done = Column(Boolean)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
