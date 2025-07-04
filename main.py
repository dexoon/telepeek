from fastapi import FastAPI, HTTPException
from telethon.sync import TelegramClient
from telethon.errors import UsernameNotOccupiedError, UsernameInvalidError
from telethon.tl.types import User
from pydantic import BaseModel
from typing import Optional
import os
import uvicorn
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()

# Environment variables for Telegram API
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
if api_id is None or api_hash is None or bot_token is None:
    raise ValueError("API_ID, API_HASH, and BOT_TOKEN must be set")
port=os.getenv('PORT', 80)

# Telegram client
client = TelegramClient('bot', api_id, api_hash)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await client.start(bot_token=bot_token)
    yield
    # Shutdown
    await client.disconnect()

# FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Data model for User information
class UserData(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: Optional[str] = None
    phone: Optional[str] = None
    is_bot: bool
    verified: bool
    restricted: bool
    scam: bool
    language_code: Optional[str] = None

@app.get("/user/{username}", response_model=UserData)
async def get_user_info(username: str):
    try:
        # Fetch user data from Telegram
        user = await client.get_entity(username)
        
        if not isinstance(user, User):
            raise HTTPException(status_code=404, detail="User not found")

        # Prepare user data
        user_data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone if hasattr(user, 'phone') else None,
            "is_bot": user.bot,
            "verified": user.verified,
            "restricted": user.restricted,
            "scam": user.scam,
            "language_code": user.lang_code
        }

        return user_data

    except UsernameNotOccupiedError:
        raise HTTPException(status_code=404, detail="User not found")
    
    except UsernameInvalidError:
        raise HTTPException(status_code=400, detail="Invalid username format")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(port), reload=True)
