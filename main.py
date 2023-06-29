from fastapi import FastAPI, Path, Query, Depends
import uvicorn
from db.connection import session
from db.models import User as DBUser
from sqlalchemy.orm import Session
from pydantic_files.models import Produit as PyProduit, User as PyUser, TokenResponse
from db.models import Produit as DBProduit
from auth.hash_password import HashPassword
from auth.authenticate import authenticate
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token

app = FastAPI()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}

'''
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}'''

@app.get("/hello/{name}/{age}")
async def get_name_with_age(name: str, age: int):
    return {"name": name, "age": age}

@app.get("/hello/{name}")
async def get_name_with_age( age: int=Query(gt=2), name: str=Path(min_length=2)):
    return {"name": name, "age": age}

@app.post("/add-new")
async def add_new(produit: PyProduit, db: Session = Depends(get_db), user: str = Depends(authenticate)):
    prod = DBProduit(id= produit.id, nom=produit.nom,
                     date_fabrique=produit.date_fabrique,
                     date_expiration=produit.date_expiration)
    db.add(prod)
    db.commit()
    db.refresh(prod)

    return DBProduit(**prod.dict())

@app.post("/signup")
async def signup(user : PyUser, db : Session = Depends(get_db)):
    hashPassword = HashPassword()
    hashed_password = hashPassword.create_hash(user.password)
    user.password = hashed_password
    dbUser = DBUser(id=user.id, username=user.username, 
                    password=hashed_password, fullname=user.fullname)
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)

    return {
        "message": "User created successfully"
    }

@app.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> dict:
    
    user_exist = db.query(DBUser).filter(DBUser.username == user.username).first()
    #user_exist = await DBUser.filter(DBUser.username == user.username)
    
    #user_exist = db.

    print(user_exist)

    hashPassword = HashPassword()

    if hashPassword.verify_hash(user.password, user_exist.password):
        access_token = create_access_token(user_exist.username)
    return {
    "access_token": access_token,
    "token_type": "Bearer"
    }


@app.get("/get-produits")
async def get_produits(db: Session = Depends(get_db)):
    prods = db.query(DBProduit).all()

    return prods


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)