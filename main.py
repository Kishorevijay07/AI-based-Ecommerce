from fastapi import FastAPI
from routes import product_routes
from routes import user_routes,all_product_routes
from config import connect_db, close_db

app = FastAPI(title="AI E-Commerce API")

# Register routes
app.include_router(all_product_routes.router)
app.include_router(product_routes.router)
app.include_router(user_routes.router)




@app.on_event("startup")
async def startup_event():
    await connect_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()

@app.get("/")
async def root():
    return {"message": "Welcome to AI E-Commerce API"}
