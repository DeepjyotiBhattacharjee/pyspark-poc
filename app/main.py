import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import UserController

app = FastAPI()

# CORS Middleware to allow all origins, credentials, methods, and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize API router from RecordController class
user_controller = UserController()
app.include_router(user_controller.router)

# A simple index route
@app.get("/api/")
def index():
    return {"message": "Simple CRUD API with FastAPI and PySpark"}

# Run the application using Uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5001, reload=True)
