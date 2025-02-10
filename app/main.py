from fastapi import FastAPI
from app.api.v1.endpoints import auth, insights, trends

app = FastAPI(title="Epsilon API", version="1.0")

# Ensure the correct prefix "/api/v1"
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(insights.router, prefix="/api/v1/insights", tags=["Insights"])
app.include_router(trends.router, prefix="/api/v1/trends", tags=["Trends"])

@app.get("/")
def root():
    return {"message": "Epsilon API is running!"}
