from sqlalchemy import (
    Column,
    String,
    BigInteger,
    SmallInteger,
    Float,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Address(Base):
    __tablename__ = "address"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    district = Column(String(4), nullable=False)
    legal_dong = Column(String(6), nullable=False)
    main_lot_number = Column(SmallInteger, nullable=False)
    sub_lot_number = Column(SmallInteger, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Address(district={self.district}, legal_dong={self.legal_dong}, main_lot_number={self.main_lot_number}, sub_lot_number={self.sub_lot_number}, latitude={self.latitude}, longitude={self.longitude})>"
