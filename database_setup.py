
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


# making an instance of the declarative_base
Base = declarative_base()


class User(Base):
    # creating a user object with user info
    __tablename__ = 'user'

    # creating id as primary key
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    # creating a serialize function to loop thourg the user info
    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }


# creating a category object inherited from the class base
class Category(Base):
    __tablename__ = 'category'

    # creating id as primary key
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
        }


class Item(Base):
    # creating an item object
    __tablename__ = 'items'

    # using id as the primary key
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    # creating a foreign key to the category, pointing to category.id
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    # creating a foreign key to the user, pointing to the user's id
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'desctiption': self.description,
            'price': self.price,
            'category_id': self.category_id,
            'user_id': self.user_id
        }

# creating engine on items_catalog.db
engine = create_engine('sqlite:///items_catalog.db')

# goes into the db and add the classes we created as tables
Base.metadata.create_all(engine)

print('We created the database structure!')
