from fastapi import FastAPI
from app.api_v1.user.service import router as user_router
from app.api_v1.org.service import router as org_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(user_router, prefix="/v1/user", tags=["admin"])
app.include_router(org_router, prefix="/v1/org", tags=["org"])