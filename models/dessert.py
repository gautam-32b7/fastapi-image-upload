from sqlalchemy import Column, Integer, String, Double

from database import Base


# SQLAlchemy model representing a dessert in the database
class Dessert(Base):
    __tablename__ = 'desserts'

    id = Column(Integer, primary_key=True, index=True)
    dessert_name = Column(String)
    description = Column(String)
    price = Column(Double)
    image_url = Column(String)
