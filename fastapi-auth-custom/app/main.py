from fastapi import FastAPI
from app.routes import user,auth
from app.config.security import JWTAuth
from starlette.middleware.authentication import AuthenticationMiddleware
app=FastAPI()
app.include_router(user.router)
app.include_router(user.user_router)
app.include_router(auth.auth_router)
app.include_router(auth.router)

# add Middleware
app.add_middleware(AuthenticationMiddleware,backend=JWTAuth())
@app.get("/")
def index():
    return {"title": "Hello Minh dev :)"}