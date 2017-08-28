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
                        ip = line.split()[0]
                        user_agent = line.rstrip().split('"')[-2]
                        if ip and user_agent:
                            cls.load_to_db(ip, user_agent)
                        time.sleep(0.45)
            else:
                raise Exception(f"{file} doesn't exists")
        except BaseException as e:
            print('parsing failed')
            raise e

    @classmethod
    def load_to_db(cls, ip, user_agent):
        ip_obj = IpMapping.fetch(ip)
        ua_obj = DeviceInfo.fetch(user_agent)
        MappingDeviceInfoLink.insert_or_ignore(ip_obj, ua_obj)
