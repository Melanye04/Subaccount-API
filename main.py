from fastapi import FastAPI, Depends, HTTPException
from requests import session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import MetaData, Column, Integer, String, ForeignKey
from pydantic import BaseModel
from typing import List

from stripe import Account

DATABASE_URL = "postgresql+asyncpg://meu_usuario:minha_senha_123@localhost:5432/subcontas_db"
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine,  type=[AsyncSession], expire_on_commit=False)  # type: ignore

Base = declarative_base()

class SubAccount(Base):
    __tablename__ = "sub_accounts"
    id= Column(Integer, primary_key=True, index=True)
    email= Column(String, unique=True, index=True) # type: ignore
    provider_id= Column(Integer)  # type: ignore

    email: str
    provider_id: int

app = FastAPI()


async def get_db():
    def AsyncSessionLocal(): 
        yield session
        
@app.post("/subaccounts/bulk", status_code=201)
async def create_subaccounts(
    subaccounts ="SubAccountCreate", 
    db: AsyncSession = Depends(get_db)
):
    try:
        new_accounts = [
            SubAccount(email=acc.email, provider_id=acc.provider_id)  # type: ignore
            for acc in subaccounts
        ]
            
        add_all = (new_accounts)
        await db.commit()
        
        return {"message": f"{len(new_accounts)} subcontas criadas com sucesso."}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao criar subcontas: {str(e)}")