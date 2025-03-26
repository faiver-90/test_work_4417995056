from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey


# Базовый класс
class Base(DeclarativeBase):
    pass


# Таблица Files
class File(Base):
    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)

    # Один ко многим: File -> Tags
    tags: Mapped[list["Tag"]] = relationship(back_populates="file",
                                             cascade="all, delete-orphan")


# Таблица Tags
class Tag(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    file_id: Mapped[int] = mapped_column(ForeignKey("files.id"))

    file: Mapped["File"] = relationship(back_populates="tags")
    attributes: Mapped[list["Attribute"]] = relationship(
        back_populates="tag",
        cascade="all, delete-orphan")


# Таблица Attributes
class Attribute(Base):
    __tablename__ = 'attributes'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    value: Mapped[str] = mapped_column(String)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))

    tag: Mapped["Tag"] = relationship(back_populates="attributes")
