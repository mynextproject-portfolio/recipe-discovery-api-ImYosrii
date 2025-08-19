from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


# Recipe Model
class Recipe(BaseModel):
    id: int | None = None
    title: str
    ingredients: list[str]
    steps: list[str]
    prepTime: str
    cookTime: str
    difficulty: str
    cuisine: str


# In-memory database
recipes = [
]

@app.get("/ping")
async def root():
    return "pong"

@app.get("/recipes")
async def get_recipes():
    return JSONResponse(content=[recipe.dict() for recipe in recipes], status_code=200)

@app.get("/recipes/{id}")
async def get_recipe(id: int):
    if 0 <= id < len(recipes):
        return JSONResponse(content=recipes[id].dict(), status_code=200)
    raise HTTPException(status_code=404, detail="Recipe not found")

# Create recipe
@app.post("/recipes")
async def create_recipe(recipe: Recipe):
    recipe.id = len(recipes)
    recipes.append(recipe)
    return JSONResponse(content=recipe.dict(), status_code=201)