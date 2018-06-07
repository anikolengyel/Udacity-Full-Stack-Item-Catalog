
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3

# making an instance of the declarative_base
Base = declarative_base()


class User(Base):
    # creating a table restaurant
    __tablename__ = 'user'

    # creating new column called name
    # if there is no name, we cant create restaurant row
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable = False)
    email = Column(String(250), nullable = False)
    picture = Column(String(250))

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }

# creating new class restaurant inherited from the class base (inherits all the functions)
class Category(Base):
    # creating a table restaurant
    __tablename__ = 'category'

    # creating new column called name
    # if there is no name, we cant create restaurant row
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable = False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
        }

class Item(Base):
    # creating a table restaurant
    __tablename__ = 'items'

    # creating new column called name
    # if there is no name, we cant create restaurant row
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    price = Column(String(8))
    # creating a foreign key to the category, pointing to category.id
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)


    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'desctiption' : self.description,
            'price': self.price
        }


engine = create_engine('sqlite:///items_catalog.db')

# goes into the db and add the classes we created as tables
Base.metadata.create_all(engine)

print('We created the database structure!')
# creating a session and add some test data to the database





