# import ORM package to handle write and read to database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# import the setub file to load tables in order to write data
from Database_Setup import Category, CategoryItem, User, Base
# call the sqlite database file
engine = create_engine('postgresql://catalog:hazem123@localhost/catalog')

# Clear database from any data
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Bind the engine to the metadata of the Base class so it can be accessed
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

# A DBSession() instance establishes all conversations with the database
session = DBSession()

# Create dummy user to test our tables relations with it
user1 = User(name="THANOS", email="testUSER@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18deb'
             'd694829ed78203a5a36dd364160_400x400.png')
session.add(user1)
session.commit()

# Items for Strings in data base
category1 = Category(name="strings", user_id=1)

session.add(category1)
session.commit()

# item 1
item1 = CategoryItem(name="violin", user_id=1, description="Violin, family " +
                     "of stringed musical instruments having wooden " +
                     "bodies whose backs and fronts are slightly convex," +
                     " the fronts pierced" +
                     " by two-shaped resonance holes. The instruments of " +
                     "the violin family have been the dominant bowed" +
                     " instruments because of their versatility, brilliance," +
                     " and balance of tone, and their wide dynamic range." +
                     " A variety of " +
                     "sounds may be produced, e.g., by different types of " +
                     "bowing or by plucking the string (see pizzicato)." +
                     " The violin has always been the most important member " +
                     "of the family, from the beginning being the" +
                     " principal orchestral instrument and holding" +
                     " an equivalent position in chamber music and as a solo" +
                     " instrument. The technique of the violin" +
                     "was developed much earlier than that of the " +
                     "viola or cello.", category=category1)

session.add(item1)
session.commit()
# item 2
item2 = CategoryItem(name="viola", user_id=1,
                     description="The viola is a string instrument that is "
                     "bowed or played with varying techniques. It is slightly "
                     "larger than a violin and has a lower "
                     "and deeper sound.", category=category1)

session.add(item2)
session.commit()
# item 3
item3 = CategoryItem(name="cello", user_id=1, description="The cello or" +
                     " violoncello is a string instrument. It is played by" +
                     " bowing or plucking its four strings, which are " +
                     "usually tuned in perfect fifths an octave lower than " +
                     "the viola: from low to " +
                     "high, C, G, D and A. ", category=category1)

session.add(item3)
session.commit()

# Items for Woodwinds in data base
category2 = Category(name="woodwinds", user_id=1)

session.add(category2)
session.commit()
# item 4
item1 = CategoryItem(name="flute", user_id=1, description="The flute is " +
                     "a family of musical instruments in the woodwind group." +
                     " Unlike woodwind instruments with reeds, a flute is" +
                     " an aerophone or reedless wind instrument that " +
                     "produces its sound from the flow of air across " +
                     "an opening.", category=category2)

session.add(item1)
session.commit()
# item 5
item2 = CategoryItem(name="piccolo", user_id=1,  description="The piccolo " +
                     "is a half-size flute, and a member of the woodwind " +
                     "family of musical instruments. The modern piccolo " +
                     "has most of the same fingerings as its larger sibling," +
                     " the standard transverse flute,", category=category2)

session.add(item2)
session.commit()
# item 6
item3 = CategoryItem(name="oboe", user_id=1, description="Oboes are a " +
                     "family of double reed woodwind instruments. The most " +
                     "common oboe plays in the treble or soprano range. " +
                     "Oboes are usually made of wood, but there are also " +
                     "oboes made of synthetic materials.", category=category2)

session.add(item3)
session.commit()

# Items for Percussion in data base
category3 = Category(name="percussion", user_id=1)

session.add(category3)
session.commit()
# item 7
item1 = CategoryItem(name="marimba", user_id=1, description="The marimba " +
                     "is a percussion instrument consisting of a set of " +
                     "wooden bars struck with mallets called knobs to " +
                     "produce musical tones. Resonators or pipes suspended " +
                     "underneath the bars amplify " +
                     "their sound.", category=category3)

session.add(item1)
session.commit()
# item 8
item2 = CategoryItem(name="timpani", user_id=1, description="Timpani or " +
                     "kettledrums are musical instruments in the percussion" +
                     " family. A type of drum, they consist of a membrane " +
                     "called a head stretched over a large bowl " +
                     "traditionally made of copper.", category=category3)

session.add(item2)
session.commit()
# item 9
item3 = CategoryItem(name="xylophone", user_id=1,
                     description="The xylophone is a musical instrument " +
                     "in the percussion family that consists of wooden bars " +
                     "struck by mallets.", category=category3)

session.add(item3)
session.commit()

# Items for Brass in data base
category4 = Category(name="brass", user_id=1)

session.add(category4)
session.commit()
# item 10
item1 = CategoryItem(name="Rebab", user_id=1, description="The rebab is " +
                     "a type of a bowed string instrument so named no later " +
                     "than the 8th century and spread via Islamic trading " +
                     "routes over much of North Africa, the Middle East, " +
                     "parts of Europe, and the Far East.", category=category4)

session.add(item1)
session.commit()

categories = session.query(Category).all()
print "Items Created Successfully"
