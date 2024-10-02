from typing import Any, List, Optional
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from ..db.models.user import User
from ..db.schemas.user import UserCreate
from ..db.conn import get_db
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
    
    def list(
        self,
        limit: Optional[int]=100,
        start: Optional[int]=0,
        name: Optional[str]="",
    ) -> List[User]:
        query = self.db.query(User)

        if name:
            query = query.filter_by(name=name)
        
        return query.offset(start).limit(limit).all()  or []

    
    def get_by_name(self, username, password)->User:
        user = self.db.query(User).filter(User.email == username).first()    
        
        if not user or not pwd_context.verify(User().hash(password), user.hashed_password):
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    
    def get_by_id(self,user_id)->User|None:
        return self.db.query(User).filter(User.id == user_id).first() or None
    
    def create(self, user_create: UserCreate) -> User:
        db_user = User(**user_create.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    

    def delete(self, user_id) -> Any:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.db.delete(user)
        self.db.commit()
        return {"message": "User deleted successfully"}
    
    def update(self, user: User, user_update: UserCreate) -> User:
        for key, value in user_update.dict().items():
            if(key in ["id", "created_at", "email"]):
                continue
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def hash(self, password: str) -> str:
        return pwd_context.hash(password)