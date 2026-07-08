from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import router
from app.api.v1.chess import router as chess_router
from app.api.v1.game import router as game_router

app = FastAPI(
    title="Chess Bot AI",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")
app.include_router(chess_router)
app.include_router(game_router)
# @app.get("/")
# def root():
#     return {"message": "Chess Mentor AI Backend Running"}

# @app.get("/health")
# def health():
#     return {"status": "healthy"}