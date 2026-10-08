from app.api.v0.router import api_router
from fastapi import FastAPI

description: str = """
API du projet SAE VRAG Crop

"""

app : FastAPI = FastAPI(
    title="AspectAPI", 
    description=description,
    version="0.1.0",
    contact={"name": "LEVITRE Mathys", "email": "mathys.levitre@etu.univ-littoral.fr"}
)
app.include_router(api_router, prefix="/api")

