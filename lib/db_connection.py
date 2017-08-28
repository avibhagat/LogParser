from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import config.constants as C

engine = create_engine('mysql://{0}:{1}@{2}:3306/mydb'.format(C.DB.get('user'), C.DB.get('pass'), C.DB.get('host')))

Session = sessionmaker(bind=engine)
session = Session()
