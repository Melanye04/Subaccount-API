from unittest.mock import Base
from relationship import relationship #type: ignore
from sqlalchemy import Column, ForeignKey, Integer, String


class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    subaccounts = relationship("SubAccount", back_populates="owner")

class SubAccount(Base):
    __tablename__ = "sub_accounts"
    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey("providers.id"))
    email = Column(String, unique=True)
    owner = relationship("Provider", back_populates="subaccounts")