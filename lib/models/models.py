import requests
import config.constants as C
from user_agents import parse
from datetime import datetime
from sqlalchemy import Column, Float, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

import lib.db_connection as db_conn
session = db_conn.session

Base = declarative_base()


class PrintObject(object):

    DATE_COLUMNS = ['created_at', 'updated_at']

    def as_dict(self):
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for column in self.DATE_COLUMNS:
            data[column] = data[column].strftime('%Y-%m-%d %H:%m:%S')
        return data


class IpMapping(Base, PrintObject):
    __tablename__ = 'ip_mapping'
    id = Column(Integer, primary_key=True)
    ip_address = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    country = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    devices = relationship('DeviceInfo', secondary='mapping_deviceinfo_link')

    @classmethod
    def fetch(cls, ip_address):
        # Make api call only if ip address not present in db.
        ip_obj = session.query(cls).filter_by(ip_address=ip_address).first()
        if ip_obj is None:
            ip_obj = cls.make_api_call(ip_address)
        return ip_obj

    @classmethod
    def make_api_call(cls, ip_address):
        r = requests.get(C.API_URL+ip_address)
        json_data = r.json()
        city = json_data['city']
        state = json_data['regionName']
        country = json_data['country']
        latitude = json_data['lat']
        longitude = json_data['lon']
        zip_code = json_data['zip']

        return cls(ip_address=ip_address, city=city, state=state, country=country, latitude=latitude, longitude=longitude, zip_code=zip_code)


class DeviceInfo(Base, PrintObject):
    __tablename__ = 'device_info'
    id = Column(Integer, primary_key=True)
    browser = Column(String)
    device_type = Column(String)
    operating_system = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    ips = relationship(IpMapping, secondary='mapping_deviceinfo_link')

    @classmethod
    def fetch(cls, ua_string):
        user_agent = parse(ua_string)
        browser = user_agent.browser.family
        os = user_agent.os.family
        if user_agent.is_bot:
            device = 'Robot'
        elif user_agent.is_mobile:
            device = 'Mobile'
        elif user_agent.is_pc:
            device = 'Desktop'
        elif user_agent.is_tablet:
            device = 'Tablet'
        else:
            device = 'Other'

        # Create device_info_obj only if it doesn't exist
        device_info_obj = session.query(cls).filter_by(browser=browser, device_type=device, operating_system=os).first()
        if device_info_obj is None:
            device_info_obj = cls(browser=browser, device_type=device, operating_system=os)
        return device_info_obj


class MappingDeviceInfoLink(Base, PrintObject):
    __tablename__ = 'mapping_deviceinfo_link'
    ip_mapping_id = Column(Integer, ForeignKey('ip_mapping.id'), primary_key=True)
    device_info_id = Column(Integer, ForeignKey('device_info.id'), primary_key=True)
    notes = Column(String)

    # creating relationship to keep db in normalized form
    ip_mapping = relationship(IpMapping, backref=backref("ip_mapping_assoc"))
    device_info = relationship(DeviceInfo, backref=backref("device_info_assoc"))

    @classmethod
    def insert_or_ignore(cls, ip_obj, ua_obj):
        obj = session.query(cls).filter_by(ip_mapping=ip_obj, device_info=ua_obj).first()
        if obj is None:
            try:
                obj = cls(ip_mapping=ip_obj, device_info=ua_obj)
                session.add(obj)
            except Exception as e:
                session.rollback()
                print("Something went wrong", e)
            else:
                session.commit()
