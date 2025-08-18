from fastapi import FastAPI

app = FastAPI()

# In-memory database
recipes = [("Pasta", "Boil water, add pasta, cook for 10 minutes."), ("Pizza", "Bake dough, add toppings, cook for 15 minutes."), ("Salad", "Chop vegetables, mix with dressing.")]

@app.get("/ping")
async def root():
    return "pong"


@app.get("/recipes")
async def get_recipes():
    return recipes, 200

@app.get("/recipes/{id}")
async def get_recipe(id: int):
    if 0 <= id < len(recipes):
        return recipes[id], 200
    return {"error": "Recipe not found"}, 404