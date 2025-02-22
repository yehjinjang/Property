from sqlalchemy import (
    Column,
    String,
    BigInteger,
    SmallInteger,
    Float,
    DECIMAL,
    ForeignKey,
    Integer,
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


class Building(Base):
    __tableanme__ = "building"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    address_id = Column(BigInteger, ForeignKey("address.id"), nullable=False)
    building_name = Column(String(30), nullable=False)
    construction_year = Column(SmallInteger, nullable=False)
    building_usage = Column(String(5), nullable=False)
    building_area_sqm = Column(DECIMAL(5, 2), nullable=False)
    floor = Column(SmallInteger, nullable=False)

    def __repr__(self):
        return f"<Building(address_id={self.address_id}, building_name={self.building_name}, construction_year={self.construction_year}, building_usage={self.building_usage}, building_area_sqm={self.building_area_sqm}, floor={self.floor})>"


class RealestateDeal(Base):
    __tablename__ = "realestate_deal"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    building_id = Column(BigInteger, ForeignKey("building.id"), nullable=False)
    reception_year = Column(SmallInteger, nullable=False)
    transaction_price_million = Column(Integer, nullable=False)
    report_type = Column(String(4), nullable=False)
    reported_real_estate_agent_district = Column(String(27), nullable=False)
    contract_year = Column(SmallInteger, nullable=False)
    contract_month = Column(SmallInteger, nullable=False)
    contract_day = Column(SmallInteger, nullable=False)

    def __repr__(self):
        return f"<RealestateDeal(building_id={self.building_id}, reception_year={self.reception_year}, transaction_price_million={self.transaction_price_million}, report_type={self.report_type}, reported_real_estate_agent_district={self.reported_real_estate_agent_district}, contract_year={self.contract_year}, contract_month={self.contract_month}, contract_day={self.contract_day})>"
