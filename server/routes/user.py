from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.hash import bcrypt
from ..routes import SessionLocal




from server.database.models.user import User

router = APIRouter()


# Request body model for user registration
class UserRegister(BaseModel):
    name: str
    email: str
    password: str

# Request body model for user login
class UserLogin(BaseModel):
    email: str
    password: str

@router.get("/")
def health_check():
    return "Hello world"

# Route for user registration
@router.post('/register')
def register(user: UserRegister):
    session = SessionLocal()

    # Check if the email or username already exists
    existing_email = session.query(User).filter_by(email=user.email).first()
    
    if existing_email:
        raise HTTPException(status_code=400, detail='Email already exists.')

    # Encrypt the password
    hashed_password = bcrypt.hash(user.password)

    # Create a new user
    new_user = User(name=user.name, email=user.email, password=hashed_password)
    session.add(new_user)
    session.commit()

    return {'message': 'User registered successfully.'}

# Route for user sign-in
@router.post('/login')
def login(user: UserLogin):
    session = SessionLocal()
    db_user = session.query(User).filter_by(email = user.email).first()

    if not db_user or not bcrypt.verify(user.password, db_user.password):
        raise HTTPException(status_code=401, detail='Invalid username or password.')

    return {'message': 'User signed in successfully.', 'content' : db_user}