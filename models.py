from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Player(Base):
    __tablename__ = "players"
    # Columns
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    birth_year = Column(String, index=True)
    first = Column(String)
    last = Column(String)

    # Non-column, provides easy access to relevant rows in Ratings table by checking what Rating.player_id foreign keys
    # reference the player object
    ratings = relationship("Rating", back_populates="player")

class Organization(Base):
    __tablename__ = "organizations"
    # Columns
    code = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)

    # Non-column, provides easy access to relevant rows in Ratings table by checking what Rating.org_code foreign keys
    # reference the player object
    issued_ratings = relationship("Rating", back_populates="org")

class Rating(Base):
    __tablename__ = "ratings"
    player_id = Column(Integer, ForeignKey("players.id"), primary_key=True)
    org_code = Column(String, ForeignKey("organizations.code"), primary_key=True)
    title = Column(String, nullable=True, index=True)
    rating_number = Column(String, index=True)

    # Non-columns
    # Relating player attribute in Rating class and ratings attribute in Player class, so when one is updated,
    # the other is automatically modified.
    player = relationship("Player", back_populates="ratings")
    org = relationship("Organization", back_populates="issued_ratings")

