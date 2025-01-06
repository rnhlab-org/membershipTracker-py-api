# Import necessary modules
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel

# Define a Pydantic model for input validation
class Member(BaseModel):
    name: str
    email: str

# Initialize FastAPI app
app = FastAPI()

# Connect to MongoDB
client = MongoClient("mongodb://mongo.default.svc.cluster.local:27017/")
db = client["membership_db"]
collection = db["members"]

# Endpoint to fetch all members
@app.get("/members")
async def get_members():
    members = list(collection.find({}, {"_id": 0}))
    return members

# Endpoint to add a new member
@app.post("/members")
async def add_member(member: Member):
    if collection.find_one({"email": member.email}):
        raise HTTPException(status_code=400, detail="Email already exists")
    collection.insert_one(member.dict())
    return {"message": "Member added"}
