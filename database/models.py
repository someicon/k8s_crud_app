from sqlalchemy import Integer, String

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150))
    surname: Mapped[str] = mapped_column(String(150))
    age: Mapped[str] = mapped_column(Integer)
    email: Mapped[str] = mapped_column(String(150))
    password: Mapped[str] = mapped_column(String(150))

    def __repr__(self):
        return '<User %r>' % (self.id)
