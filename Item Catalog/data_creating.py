from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Item, Base, User

engine = create_engine('sqlite:///items_catalog.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

print("We created the session!")

User1 = User(id = 35, name="Sporty User", email="sporty@email.com",
             picture='http://cdn.shopify.com/s/files/1/0257/6087/products/48-Soccer-Ball-Solo_Single_Front_ee0e6213-8997-45fc-bfc5-483ef2dc1391.png?v=1524766022')
session.add(User1)
session.commit()

#Categories and Items
horse_riding = Category(name = "Horse Riding", user_id = 34)

session.add(horse_riding)
session.commit()

gloves = Item(name = "Horse Riding Gloves", description = "Stretcheable fabric, comfortable daily use. 1 year Warranty.", price = "$7.50", category = horse_riding, user_id = 34)

session.add(gloves)
session.commit()

boots = Item(name = "Starter Front Zip Paddock Boots", description = "Syntheic leather, stretcheable fabric, round toe. 1 year Warranty.", price = "$40.15", category = horse_riding, user_id = 34)

session.add(boots)
session.commit()

helmet = Item(name = "Schooler Helmet", description = "Leather, easy-adjust, extra-string adjustment mens added helmet life.", price = "$62.55", category = horse_riding, user_id = 34)

session.add(helmet)
session.commit()

###### SWIMMING

swimming = Category(name = "Swimming", user_id = 34)

session.add(swimming)
session.commit()

kickboard = Item(name = "Team Kickboard", description = "Made of lightweight texture, fleece lined.", price = "$15", category = swimming, user_id = 34)

session.add(kickboard)
session.commit()

goggle = Item(name = "Mirrored Swim Goggle", description = "UV-protected lenses, anti-fog coating, mirrored lens, 25% more peripheral vision.", price = "$22.15", category = swimming, user_id = 34)

session.add(goggle)
session.commit()

cap = Item(name = "Flexible Swimming Cap", description = "Suitable for all hair lenghts, plus nose clip, non-toxic.", price = "$10.55", category = swimming, user_id = 34)

session.add(cap)
session.commit()

##### RUNNING

print('We created the database!')





