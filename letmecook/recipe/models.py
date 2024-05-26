from typing import Optional

from letmecook.core.LetMeCookBaseModel import LetMeCookBaseModel

class Ingredient(LetMeCookBaseModel):
    id: int
    amount: float
    unit: str

class Recipe(LetMeCookBaseModel):
    id: Optional[int]
    title: str
    image: str
    usedIngredientCount: int
    missedIngredients: list[Ingredient]
    usedIngredients: list[Ingredient]

class SingleSimilarRecipe(LetMeCookBaseModel):
    id: int
    title: str
    readyInMinutes: int


class SimilarRecipe(LetMeCookBaseModel):
    recipes: list[SingleSimilarRecipe]


class RecipeInformation(LetMeCookBaseModel):
    id: int
    title: str
    vegetarian: bool
    vegan: bool
    glutenFree: bool
    dairyFree: bool
    veryHealthy: bool
    veryPopular: bool
    lowFodmap: bool
    readyInMinutes: int
    image: str
    instructions: str
    similar: Optional[SimilarRecipe] = []
    
    
class RecipeRandomResponse(LetMeCookBaseModel):
    id: int
    title: str
    vegetarian: bool
    vegan: bool
    glutenFree: bool
    dairyFree: bool
    veryHealthy: bool
    veryPopular: bool
    lowFodmap: bool
    readyInMinutes: int
    image: str
    instructions: str

class SearchRecipeSingleModel(LetMeCookBaseModel):
    id: int
    title: str
    image: str

class SearchRecipeResponse(LetMeCookBaseModel):
    results: list[SearchRecipeSingleModel] = []



