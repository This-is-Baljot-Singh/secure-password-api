from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import secrets
import string

app = FastAPI()

# Input model with default values
class PasswordRequest(BaseModel):
    length: int = 12
    include_symbols: bool = True
    include_numbers: bool = True
    include_uppercase: bool = True

@app.get("/")
def home():
    return {"message": "Secure Password Generator API is running!"}

@app.post("/generate-password")
def generate_password(data: PasswordRequest):
    # Safety check: prevent users from asking for massive strings that crash the server
    if data.length < 4 or data.length > 128:
        raise HTTPException(status_code=400, detail="Length must be between 4 and 128 characters.")
    
    # 1. Build the character pool based on user preferences
    chars = string.ascii_lowercase # Always include lowercase
    
    if data.include_uppercase:
        chars += string.ascii_uppercase
    if data.include_numbers:
        chars += string.digits
    if data.include_symbols:
        chars += string.punctuation

    # 2. Generate a cryptographically secure password
    # secrets.choice is safer than random.choice for security tools
    password = ''.join(secrets.choice(chars) for _ in range(data.length))
    
    return {
        "password": password,
        "length": data.length,
        "complexity": "High" if data.include_symbols and data.length > 10 else "Standard"
    }