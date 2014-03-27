from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String ,DateTime,Text

Base=declarative_base()

class user(Base):
    __tablename__="users"
    id=Column(Integer ,primary_key = True)
    user_name=Column(String(20))
    psw=Column(String(20))
    email=Column(String(20))
    time=Column(DateTime)
    def __init__(self):
        self.id=id
        self.user_name=user_name
        self.psw=psw
        self.email=email
        self.time=time

class article(Base):
    __tablename__="articles"
    pid=Column(Integer ,primary_key = True)
    title=Column(String(100))
    content=Column(Text)
    post_time=Column(DateTime)

'''class comment(Base):
    __tablename__="comments"'''


from sqlalchemy.orm import sessionmaker,scoped_session
#The scoped_session() function wraps around the sessionmaker() function, and produces an object which behaves the same as the Session subclass returned by sessionmaker():
from sqlalchemy import create_engine

db=create_engine('mysql+mysqldb://root:yayun@localhost/sqldem?charset=utf8',echo=False,pool_recycle=36)
#global scope
Session = sessionmaker(bind=db)
'''local scope any keyword arguments sent to the constructor itself will override the "configured"keywords:
session=Session()
'''
session=scoped_session(Session)

    
'''metadata=MetaData(bind=db)
users_table=Table('user',metadata,
        Column('user_id',Integer,primary_key=True),
        Column('user_name',String(40)),
        Column('password',String(10))
        )
users_table.create()
i=users_table.insert()
'''
