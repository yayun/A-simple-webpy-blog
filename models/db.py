#coding:utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
class User(Base):
    __tablename__="user"
    id=Column(Integer ,primary_key = True)
    user_name=Column(String(20))
    psw=Column(String(20))
    email=Column(String(20)
    time=Column(DateTime)
class Article(Base):
    __tablename__="articles"
    pid=Column(Integer ,primary_key = True)
    title=Column(String(100))
    content=Column(Text)
    tag=Column(Stirng(50))
    author=Column(String(50))
    post_time=Column(DateTime)

'''class Comment(Base): 
    __tablename__="comments"'''

db=create_engine('mysql+mysqldb://root:yayun@localhost/blog?charset=utf8',echo=False,pool_recycle=36)
#global scope
Session = sessionmaker(bind=db)

def load_sqla(handler):
    import web
    web.ctx.orm = scoped_session(Session)
    try:
        return handler()
    except web.HTTPError:
       web.ctx.orm.commit()
       raise
    except:
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()


