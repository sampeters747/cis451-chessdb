from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Player(Base):
    __tablename__ = "players"
    # Columns
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    birth_year = Column(Integer)
    first = Column(String(18))
    last = Column(String(18))

    # Non-columns
    # ratings variable provides easy access to relevant rows in Ratings table by checking what Rating.player_id foreign keys
    # reference the player object
    ratings = relationship("Rating", back_populates="player")
    tournaments = relationship("TournamentEntry", back_populates="player")

class Organization(Base):
    __tablename__ = "organizations"
    # Columns
    code = Column(String(8), primary_key=True, index=True)
    name = Column(String(36))

    # Non-column, provides easy access to relevant rows in Ratings table by checking what Rating.org_code foreign keys
    # reference the player object
    issued_ratings = relationship("Rating", back_populates="org")
    # More non-columns
    tournaments = relationship("Tournament", back_populates="org")

class Rating(Base):
    __tablename__ = "ratings"
    # Columns
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, primary_key=True)
    org_code = Column(String(8), ForeignKey("organizations.code"), nullable=False, primary_key=True)
    title = Column(String(18), nullable=True)
    rating_number = Column(Integer)

    # Non-columns
    # Relating player attribute in Rating class and ratings attribute in Player class, so when one is updated,
    # the other is automatically modified.
    player = relationship("Player", back_populates="ratings")
    org = relationship("Organization", back_populates="issued_ratings")

class Tournament(Base):
    __tablename__ = "tournaments"
    # Columns
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    org_code = Column(String(8), ForeignKey("organizations.code"), nullable=False)
    name = Column(String(36))
    year = Column(Integer)

    # Non-columns
    org = relationship("Organization", back_populates="tournaments")
    players = relationship("TournamentEntry", back_populates="tournament")

class TournamentEntry(Base):
    __tablename__ = "tournamententry"
    # Columns
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, primary_key=True)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False, primary_key=True)

    # Non-columns
    player = relationship("Player", back_populates="tournaments")
    tournament = relationship("Tournament", back_populates="players")
