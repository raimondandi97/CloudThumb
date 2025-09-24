from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.auth import verify_password, create_access_token, hash_password
from app.databases import get_db
from app.models import User
from app.schemas.user import UserResponse, UserCreate

router = APIRouter()


def _get_user(db, user):
    return db.query(User).filter(
        or_(User.username == user.username, User.email == user.email)
    ).first()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(
        or_(User.username == user.username, User.email == user.email)
    ).first():
        raise HTTPException(status_code=400, detail="Username or email already exists")
    new_user = User(username=user.username,
                    email=user.email,
                    hashed_password=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Login endpoint
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
