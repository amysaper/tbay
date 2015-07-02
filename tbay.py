from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



engine = create_engine('postgresql://ubuntu:glasswoodfallshift@localhost:5432/ubuntu')

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


from datetime import datetime

from sqlalchemy import Table, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship


class Item(Base):
    __tablename__ = "Items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    #One-to-many relationship between an owner and the items up for auction
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)

    #one-to-many relationship btwn an item and the bids placed on it  
    bids = relationship("Bid", backref="item")
    
class User(Base):    
    __tablename__ = "User"
    
    id = Column(Integer, primary_key=True)
    username= Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    #One-to-many relationship between an item up for auction and its owner
    items = relationship("Item", backref="user") 
    
    #one-to-many relationship btwn a user who places a bid and the  bids that user places 
    bids = relationship("Bid", backref="user")

class Bid(Base):    
    __tablename__ = "Bid"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    
    #One-to-many relationship between a bidder and the bids in the auction 
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    
    #One-to-many relationship between an item and the bids placed on it  
    item_id = Column(Integer, ForeignKey('Items.id'), nullable=False)

Base.metadata.create_all(engine)


#Question for Chris, getting errors when I try to createdb tbay

amy = User(username= "amys", password = "123")
julia = User(username= "julias", password = "dolphin")
kim = User(username= "kimbo", password = "caden")
baseball = Item(name= "baseball", description= "pretty self explanatory", user = amy)


#question on syntax for bids
bid1 = Bid(price = 7.3, user = julia, item = baseball)
bid2= Bid(price = 10.2, user = kim, item = baseball)


#ugly, longer version that amy is more comfortable with to find highest bidder
highest_bid = 0;
highest = amy;
for bid in baseball.bids:
    print bid.price;
    if bid.price > highest_bid:
        highest_bid = bid.price
        highest = bid.user
print highest.username

#alternate magical method to find highest bidder
top_bid = max(baseball.bids, key=lambda bid: bid.price)
print top_bid.user.username;