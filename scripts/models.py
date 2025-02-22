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
    name = Column(String(30), nullable=False)
    construction_year = Column(SmallInteger, nullable=False)
    purpose = Column(String(5), nullable=False)
    area_sqm = Column(DECIMAL(5, 2), nullable=False)
    floor = Column(SmallInteger, nullable=False)

    def __repr__(self):
        return f"<Building(address_id={self.address_id}, name={self.name}, construction_year={self.construction_year}, usage={self.usage}, area_sqm={self.area_sqm}, floor={self.floor})>"


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


class BusStation(Base):
    __tablename__ = "bus_station"

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(26), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    def __repr__(self):
        return f"<BusStation(id={self.id}, name={self.name}, latitude={self.latitude}, longitude={self.longitude})>"


class Hospital(Base):
    __tablename__ = "hospital"

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    address = Column(String(22), nullable=False)
    note = Column(String(239), nullable=False)
    map = Column(String(67), nullable=False)
    name = Column(String(29), nullable=False)
    phone = Column(String(12), nullable=False)
    emergency_phone = Column(String(13), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Hospital(address={self.address}, map={self.map}, name={self.name}, phone={self.phone}, emergency_phone={self.emergency_phone}, latitude={self.latitude}, longitude={self.longitude})>"


class Subway(Base):
    __tablename__ = "subway"

    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    line = Column(String(3), nullable=False)
    name = Column(String(10), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Subway(line={self.line}, name={self.name}, latitude={self.latitude}, longitude={self.longitude})>"
