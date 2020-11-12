from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



# This is because OAuth2 uses "form data" for sending the username and password.



@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}