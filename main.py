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
    return JSONResponse(content=[recipe.dict() for recipe in recipes if recipe is not None], status_code=200)



# Search by Query
@app.get("/recipes/search")
async def search_recipes(q: str):
    if len(q):
        results = [recipe.dict() for recipe in recipes if recipe is not None and q.lower() in recipe.title.lower()]
        if results:
            return JSONResponse(content=results, status_code=200)
    return JSONResponse(content=[], status_code=200)

# Get Recipe by ID
@app.get("/recipes/{id}")
async def get_recipe(id: int):
    if 0 <= id < len(recipes) and recipes[id] is not None:
        return JSONResponse(content=recipes[id].dict(), status_code=200)
    raise HTTPException(status_code=404, detail="Recipe not found")

# Create recipe
@app.post("/recipes")
async def create_recipe(recipe: Recipe):
    recipe.id = len(recipes)
    recipes.append(recipe)
    return JSONResponse(content=recipe.dict(), status_code=201)

# Update recipe
@app.put("/recipes/{id}")
async def update_recipe(id: int, recipe: Recipe):
    if 0 <= id < len(recipes):
        recipe.id = id
        recipes[id] = recipe
        return JSONResponse(content=recipe.dict(), status_code=200)
    raise HTTPException(status_code=404, detail="Recipe not found")
    
# Delete recipe
@app.delete("/recipes/{id}")
async def delete_recipe(id: int):
    if 0 <= id < len(recipes) and recipes[id] is not None:
        recipes[id] = None
        return JSONResponse(status_code=204)
    raise HTTPException(status_code=404, detail="Recipe not found")


