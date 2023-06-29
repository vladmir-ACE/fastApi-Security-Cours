from pydantic import BaseModel
from datetime import date

class Produit(BaseModel):
    id:int
    nom:str
    date_fabrique:date
    date_expiration:date

    class Config:
        orm_mode = True


class Categorie(BaseModel):
    id:int
    nom_categorie:str

class ProduitVendu(BaseModel):
    id:int
    quantiter:int

class Vente(BaseModel):
    id:int
    dateVente:date
    matricule_vente:str

class Client(BaseModel):
    id:int
    nom:str
    prenom:str
    tel:str

class Gerant(BaseModel):
    id:int
    nom:str
    prenom:str
    email:str
    tel:str

class User(BaseModel):
    id: int
    fullname: str
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str