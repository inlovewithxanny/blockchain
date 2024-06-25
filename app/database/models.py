from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import (
    VARCHAR,
    Integer,
    TIMESTAMP,
    Float,
    func,
    ForeignKey
)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Block(Base):
    __tablename__ = "blocks"

    id: Mapped[int] = mapped_column(primary_key=True)
    hash: Mapped[str] = mapped_column(VARCHAR(64), nullable=False)
    parent_hash: Mapped[str] = mapped_column(VARCHAR(64), nullable=False)
    proof: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP(), nullable=False, server_default=func.now())
    merkle_root: Mapped[str] = mapped_column(VARCHAR(64), nullable=False)

    transactions: Mapped[List["Transaction"]] = relationship(back_populates="block")


class Transaction(Base):
    __tablename__ = "transactions"

    hash: Mapped[str] = mapped_column(VARCHAR(64), primary_key=True)
    block_id: Mapped[int] = mapped_column(ForeignKey("blocks.id"), nullable=False)
    sender: Mapped[str] = mapped_column(VARCHAR(128), nullable=False)
    recipient: Mapped[str] = mapped_column(VARCHAR(128), nullable=False)
    amount: Mapped[float] = mapped_column(Float(), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(TIMESTAMP(), nullable=False, server_default=func.now())

    block: Mapped["Block"] = relationship(back_populates="transactions")
