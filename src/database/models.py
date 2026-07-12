from sqlalchemy import Text, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Secret(Base):
    __tablename__ = "secrets"

    id: Mapped[str] = mapped_column(primary_key=True)
    secret_data: Mapped[str] = mapped_column(Text, nullable=False)
    hashed_password: Mapped[str | None] = mapped_column(String(255))
    is_viewed: Mapped[bool] = mapped_column(default=False)
