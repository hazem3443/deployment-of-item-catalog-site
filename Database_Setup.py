# import os package to load data to a file in database using orm
import sys
# import ORM packages
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# 'user' Table has 4 colums 'id','name','email','picture'
# these data is specific to each user


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

# 'category' Table has 3 colums 'id','name','user_id'
# each user has it's own categories also each category has it's own items
# serialize property is used to jsonify the data in database in order to be
# sent to the browser


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
        }
# 'category_item' Table has 6 colums 'name','description','id','category_id',
# 'category','user_id' these data is related to each item which is going to
# be displayed with templates also this one has a serialize property to
# jsonify the data to be sent to the browser


class CategoryItem(Base):
    __tablename__ = 'category_item'

    name = Column(String(80), nullable=False)
    description = Column(String(250))
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'category': self.category.name,
            'description': self.description,
            'name': self.name,
        }


engine = create_engine('postgresql://catalog:hazem123@localhost/catalog')
Base.metadata.create_all(engine)
