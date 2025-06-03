def recipe_file_reader(filename: str):
    recipe_list = []
    with open(filename) as recipes:
        recipe = []
        for line in recipes:
            line = line.strip()
            if line == "":
                recipe_list.append(recipe)
                recipe = []
            else:
                recipe.append(line)
        recipe_list.append(recipe)
    return recipe_list   

def search_by_name(filename: str, word: str):
    recipe_list = recipe_file_reader(filename)
    found_recipes = []
    for recipe in recipe_list:
        item = recipe[0]
        if word.lower() in item.lower():
            found_recipes.append(item)
    return found_recipes

def search_by_time(filename: str, prep_time: int):
    recipe_list = recipe_file_reader(filename)
    found_recipes = []
    for recipe in recipe_list:
        time = int(recipe[1])
        if time <= prep_time:
            found_recipes.append(f"{recipe[0]}, preparation time {time} min")
    return found_recipes

def search_by_ingredient(filename: str, ingredient: str):
    recipe_list = recipe_file_reader(filename)
    found_recipes = []
    for recipe in recipe_list:
        ingredients = []
        for item in recipe:
            if item != recipe[0] or item != recipe[1]:
                ingredients.append(item)
        if ingredient in ingredients:
            found_recipes.append(f"{recipe[0]}, preparation time {recipe[1]} min")
    return found_recipes

















if __name__ == "__main__":
    found_recipes = search_by_ingredient("recipes1.txt", "milk")

    for recipe in found_recipes:
        print(recipe)