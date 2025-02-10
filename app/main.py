from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from app.api.v1.endpoints import auth, insights, trends
import uvicorn

# Define OAuth2 scheme for Bearer Token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Initialize FastAPI app
app = FastAPI(
    title="Epsilon API",
    version="1.0",
    description="A FastAPI backend for healthcare analytics.",
    docs_url="/docs",
    openapi_url="/openapi.json",
    swagger_ui_parameters={"persistAuthorization": True},  # Keep token after login
)

# Register API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(insights.router, prefix="/api/v1/insights", tags=["Insights"])
app.include_router(trends.router, prefix="/api/v1/trends", tags=["Trends"])

# ✅ Safe OpenAPI Override to Fix Missing Version Field
def custom_openapi():
    try:
        if app.openapi_schema:  # Return existing schema if already generated
            return app.openapi_schema
        
        openapi_schema = app.openapi()  # Generate OpenAPI schema

        # Ensure OpenAPI version field exists
        if "openapi" not in openapi_schema:
            openapi_schema["openapi"] = "3.0.2"  # Explicitly set OpenAPI version

        # Ensure 'components' key exists before modifying
        if "components" not in openapi_schema:
            openapi_schema["components"] = {}

        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }

        app.openapi_schema = openapi_schema
        return app.openapi_schema
    except Exception as e:
        print(f"Error generating OpenAPI schema: {e}")
        return None  # Prevent crashing the app if OpenAPI generation fails

# ✅ Override FastAPI's OpenAPI generation safely
# app.openapi = custom_openapi

@app.get("/")
def root():
    return {"message": "Epsilon API is running!"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
