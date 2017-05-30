import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tableBuilder import *
 
engine = create_engine('sqlite:///testfrench2017.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()
 
user = User("Ben","admin")
session.add(user)
# user = User("Steve","admin")
# session.add(user)
# user = User("Santay","admin")
# session.add(user)
# user = User("Jack","admin")
# session.add(user)
# user = User("Geoff","admin")
# session.add(user)

# commit the record the database
session.commit() 
session.commit()