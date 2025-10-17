from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    favorites: Mapped[list["Favorites"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return dict(
            id=self.id,
            email=self.email,
        )


class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates="favorites")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    characters: Mapped[list["Character"]] = relationship(
        back_populates="favorites")
    planets: Mapped[list["Planet"]] = relationship(back_populates="favorites")
    vehicles: Mapped[list["Vehicle"]] = relationship(
        back_populates="favorites")


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    favorites: Mapped["Favorites"] = relationship(back_populates="characters")
    favorite_id: Mapped[int] = mapped_column(ForeignKey("favorites.id"))


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    favorites: Mapped["Favorites"] = relationship(back_populates="planets")
    favorite_id: Mapped[int] = mapped_column(ForeignKey("favorites.id"))


class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    favorites: Mapped["Favorites"] = relationship(back_populates="vehicles")
    favorite_id: Mapped[int] = mapped_column(ForeignKey("favorites.id"))
