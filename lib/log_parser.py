import os
import time
from lib.models.models import IpMapping, DeviceInfo, MappingDeviceInfoLink


class LogParser:

    @classmethod
    def parse_log(cls, file):
        try:
            if os.path.exists(file):
                with open(file) as f:
                    for line in f:
                        # IP address is first column when separated by space
                        ip = line.split()[0]
                        # User agent is 2nd last column when separated by double quotes
                        user_agent = line.rstrip().split('"')[-2]
                        if ip and user_agent:
                            # Insert data into db
                            cls.load_to_db(ip, user_agent)
                            time.sleep(0.45)
            else:
                raise Exception(f"{file} doesn't exists")
        except BaseException as e:
            print('parsing failed')
            raise e

    @classmethod
    def load_to_db(cls, ip, user_agent):
        # fetch IpMapping object
        ip_obj = IpMapping.fetch(ip)
        # fetch DeviceInfo object
        ua_obj = DeviceInfo.fetch(user_agent)
        # insert into all 3 tables
        MappingDeviceInfoLink.insert_or_ignore(ip_obj, ua_obj)
