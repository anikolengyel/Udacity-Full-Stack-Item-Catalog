from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Item, Base, User

engine = create_engine('sqlite:///items_catalog.db')

Base.metadata.bind = engine

# bind the session with the engine
DBSession = sessionmaker(bind=engine)

# creating a new session
session = DBSession()

print("We created the session!")


# creating a test user with picture
user1 = User(id = 36, name="Sporty User", email="sporty@email.com",
             picture='http://cdn.shopify.com/s/files/1/0257/6087/products/48-Soccer-Ball-Solo_Single_Front_ee0e6213-8997-45fc-bfc5-483ef2dc1391.png?v=1524766022')
session.add(user1)
session.commit()

#creating Categories and Items

# HORSE RIDING
horse_riding = Category(name = "Horse Riding", user_id = user1.id)

session.add(horse_riding)
session.commit()

gloves = Item(name = "Horse Riding Gloves", description = "Stretcheable fabric, comfortable daily use. 1 year Warranty.", price = "$7.50", category = horse_riding, user_id = user1.id)

session.add(gloves)
session.commit()

boots = Item(name = "Starter Front Zip Paddock Boots", description = "Syntheic leather, stretcheable fabric, round toe. 1 year Warranty.", price = "$40.15", category = horse_riding, user_id = user1.id)

session.add(boots)
session.commit()

helmet = Item(name = "Schooler Helmet", description = "Leather, easy-adjust, extra-string adjustment mens added helmet life.", price = "$62.55", category = horse_riding, user_id = user1.id)

session.add(helmet)
session.commit()

###### SWIMMING

swimming = Category(name = "Swimming", user_id = user1.id)

session.add(swimming)
session.commit()

kickboard = Item(name = "Team Kickboard", description = "Made of lightweight texture, fleece lined.", price = "$15", category = swimming, user_id = user1.id)

session.add(kickboard)
session.commit()

goggle = Item(name = "Mirrored Swim Goggle", description = "UV-protected lenses, anti-fog coating, mirrored lens, 25% more peripheral vision.", price = "$22.15", category = swimming, user_id = user1.id)

session.add(goggle)
session.commit()

cap = Item(name = "Flexible Swimming Cap", description = "Suitable for all hair lenghts, plus nose clip, non-toxic.", price = "$10.55", category = swimming, user_id = user1.id)

session.add(cap)
session.commit()

##### RUNNING

running = Category(name = "Running", user_id = user1.id)

session.add(running)
session.commit()

shoes = Item(name = "Running Shoes", description = "Made of lightweight texture, robust.", price = "$105", category = running, user_id = user1.id)

session.add(shoes)
session.commit()

short = Item(name = "Short for Runners", description = "Suitable for every runner, breathing fabric.", price = "$35.15", category = running, user_id = user1.id)

session.add(short)
session.commit()

print('We created the database!')





