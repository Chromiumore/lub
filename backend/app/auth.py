from hashlib import sha256
from authx import AuthX, AuthXConfig, RequestToken, TokenPayload
from fastapi import APIRouter, HTTPException, Depends
from .config import Config
from .schemas import LoginSchema, RegisterSchema
from .database import db_helper
from .models import User

config = AuthXConfig(
    JWT_SECRET_KEY = Config.load().auth.secret_key.get_secret_value(),
    JWT_TOKEN_LOCATION = ['headers'],
)

auth = AuthX(config=config)


router = APIRouter()


@router.post('/register', status_code=201)
def register(creds: RegisterSchema):
    email = creds.email
    username = creds.username
    password = creds.password.get_secret_value()
    with db_helper.session_maker() as session:
        session.add(
            User(
                email=email,
                username=username,
                password_hash=sha256(password.encode('utf-8')).hexdigest(),
            )
        )
        session.commit()


@router.post('/login')
def login(creds: LoginSchema):
    email = creds.email
    password = creds.password.get_secret_value()
    with db_helper.session_maker() as session:
        db_user = session.query(User).filter_by(email=email, password_hash=sha256(password.encode('utf-8')).hexdigest()).first()
        if not db_user:
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        token = auth.create_access_token(uid=str(db_user.id))
        return {'access_token': token}


@router.get('/protected', dependencies=[Depends(auth.get_token_from_request)])
def protected(token: RequestToken = Depends()):
    try:
        auth.verify_token(token=token)

        payload = TokenPayload.decode(token.token, Config.load().auth.secret_key.get_secret_value())
        with db_helper.session_maker() as session:
            db_user = session.query(User).filter_by(id=payload.sub).first()

            return {"message": f'Hello {db_user.username}!'}
    except Exception as e:
        raise HTTPException(401, detail={"message": str(e)}) from e
