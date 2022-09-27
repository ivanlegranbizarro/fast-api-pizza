from fastapi import APIRouter, Depends
from database import Session, engine
from schemas import Signup, Login
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

session = Session(bind=engine)


@auth_router.post('/signup', response_model_exclude_defaults=Signup, status_code=201)
async def signup(user: Signup):
    """_summary_: This is the signup route

    Args:
        user (Signup): username, email, password

    Returns:
        _type_: Json response and status code 201
    """
    db_email = session.query(User).filter_by(email=user.email).first()
    db_username = session.query(User).filter_by(username=user.username).first()

    if db_email or db_username:
        return HTTPException(status_code=400, detail="This User already exists")
    else:
        new_user = User(
            username=user.username,
            email=user.email,
            password=generate_password_hash(user.password)
        )
        session.add(new_user)
        session.commit()
        return {"message": "User created successfully"}


@auth_router.post('/login', response_model_exclude_defaults=Login, status_code=200)
async def login(user: Login, Authorize: AuthJWT = Depends()):
    """_summary_: This is the login route

    Args:
        user (Login): username, password

    Returns:
        _type_: Json response and status code 200 with token
    """
    db_user = session.query(User).filter_by(username=user.username).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=user.username)
        refresh_token = Authorize.create_refresh_token(subject=user.username)

        return ({
            "access_token": access_token,
            "refresh_token": refresh_token
        })

    raise HTTPException(status_code=401, detail="Invalid username or password")


@auth_router.post('/refresh', status_code=200)
async def refresh(Authorize: AuthJWT = Depends()):
    """_summary_: This is the refresh route

    Args:
        Authorize (AuthJWT): AuthJWT

    Returns:
        _type_: Json response with new token
    """
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        new_access_token = Authorize.create_access_token(subject=current_user)
        return {"access_token": new_access_token}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@auth_router.get('/users', status_code=200)
async def get_users(Authorize: AuthJWT = Depends()):
    """_summary_: This is the get users route

    Args:
        Authorize (AuthJWT, optional): AuthJWT. Defaults to Depends().

    Raises:
        HTTPException: 401

    Returns:
        _type_: Json response with all users
    """
    try:
        Authorize.jwt_required()
        users = session.query(User).all()
        for user in users:
            user.password = None
            user.is_active = None
            user.is_staff = None
        return users

    except Exception:
        raise HTTPException(status_code=401, detail="No token provided")
