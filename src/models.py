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
    character_id: Mapped[int] = mapped_column(
        ForeignKey("character.id"))
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"))
    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicle.id"))
    character: Mapped[list["Character"]] = relationship(
        back_populates="favorites")
    planet: Mapped[list["Planet"]] = relationship(back_populates="favorites")
    vehicle: Mapped[list["Vehicle"]] = relationship(
        back_populates="favorites")

    def serialize(self):
        return dict(
            id=self.id,
            planet=self.planet.serialize() if self.planet is not None else None,
            character=self.character.serialize() if self.character is not None else None,
            vehicle=self.vehicle.serialize() if self.vehicle is not None else None,
            user=self.user.serialize() if self.user is not None else None,
        )


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    favorites: Mapped[list["Favorites"]] = relationship(
        "Favorites", back_populates="character"
    )

    def serialize(self):
        return dict(
            id=self.id,
            name=self.name,
            description=self.description
        )


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    favorites: Mapped[list["Favorites"]] = relationship(
        "Favorites", back_populates="planet"
    )

    def serialize(self):
        return dict(
            id=self.id,
            name=self.name,
            description=self.description
        )


class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    favorites: Mapped[list["Favorites"]] = relationship(
        "Favorites", back_populates="vehicle"
    )

    def serialize(self):
        return dict(
            id=self.id,
            name=self.name,
            description=self.description
        )
