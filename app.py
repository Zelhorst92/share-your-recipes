import os
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def home():
    """
    Renders searchbar with appropriate recipe categories.
    """
    categories = mongo.db.categories.find().sort("recipe_category", 1)
    return render_template("components/home.html", categories=categories)


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Search function that find recipes from the database with 2 parameters.
    """
    inputquery = request.form.get("inputquery")
    categoryquery = request.form.get("categoryquery")
    if session.get("user"):
        is_superuser = bool(
            mongo.db.users.find_one(
                {'username': session["user"], 'superuser': True}))
    else:
        is_superuser = False

    if inputquery == "" and categoryquery == "":
        recipes = list(mongo.db.recipes.find().sort("recipe_name", 1))
    elif inputquery == "":
        recipes = list(mongo.db.recipes.find(
            {"$text": {"$search": categoryquery}}).sort("recipe_name", 1))
    elif categoryquery == "":
        recipes = list(mongo.db.recipes.find(
            {"$text": {"$search": inputquery}}).sort("recipe_name", 1))
    else:
        inputresult = list(mongo.db.recipes.find(
            {"$text": {"$search": inputquery}}).sort("recipe_name", 1))
        categoryresult = list(mongo.db.recipes.find(
            {"$text": {"$search": categoryquery}}).sort("recipe_name", 1))
        if inputresult == "":
            recipes = categoryresult
        elif categoryresult == "":
            recipes = inputresult
        else:
            recipes = inputresult + categoryresult

    print(bool(recipes))
    if bool(recipes) is True:
        return render_template(
            "pages/recipes.html", recipes=recipes, is_superuser=is_superuser)
    else:
        flash('No recipes found!')
        return redirect(url_for('home'))


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Registers an account for the user.
    Checks if username and/or emailadress are already in use.
    Creates session cookie and redirects to users dashboard.
    """
    if session.get("user"):
        flash('You are already logged in, no need to register again')
        return redirect(url_for(
            "dashboard", username=session["user"]))
    else:
        if request.method == "POST":
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})
            existing_email = mongo.db.users.find_one(
                {"email": request.form.get("email").lower()})

            if existing_user:
                flash("Username already in use, please try again")
                return redirect(url_for("register"))

            elif existing_email:
                flash("Email already in use, please try again")
                return redirect(url_for("register"))

            to_register = {
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(
                    request.form.get("password")),
                "email": request.form.get("email").lower(),
                "superuser": False
            }
            mongo.db.users.insert_one(to_register)
            session["user"] = request.form.get("username").lower()
            flash("Registration Successfull")
            return redirect(url_for(
                "dashboard", username=session["user"]))

        registration = True
        return render_template(
            "components/forms/validate.html", registration=registration)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login function with username and password.
    Checks if username and password are a correct match.
    Creates session cookie and redirects to user dashboard.
    """
    if session.get("user"):
        flash('You are already logged in')
        return redirect(url_for(
            "dashboard", username=session["user"]))
    else:
        if request.method == "POST":
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})
            if existing_user:
                if check_password_hash(
                    existing_user["password"], request.form.get(
                        "password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "dashboard", username=session["user"]))
                else:
                    flash("That's incorrect, please try again.")
                    return redirect(url_for("login"))
            else:
                flash("That's incorrect, please try again.")
                return redirect(url_for("login"))
        return render_template("components/forms/validate.html")


@app.route("/dashboard/<username>", methods=["GET", "POST"])
def dashboard(username):
    """
    Show correct dashboard according to session cookie.
    If there is no session cookie, redirects to log in page.
    """
    if session.get("user"):
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        return render_template("pages/dashboard.html", username=username)
    else:
        flash('You need to be logged in to see your dashboard')
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """
    Removes user session cookie.
    Redirects to log in page.
    """
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/recipe/view/<recipe_id>", methods=["GET", "POST"])
def view_recipe(recipe_id):
    """
    Finds recipe with recipe id.
    """
    recipe = list(mongo.db.recipes.find({"_id": ObjectId(recipe_id)}))
    return render_template("pages/recipe.html", recipe=recipe)


@app.route("/my_recipes")
def my_recipes():
    """
    If logged in, shows all recipes created by user.
    """
    if session.get("user"):
        recipes = list(mongo.db.recipes.find(
            {"$text": {"$search": session["user"]}}).sort(
                "recipe_name", 1))
        return render_template("pages/recipes.html", recipes=recipes)
    else:
        flash('You need to be logged in to see your recipes')
        return redirect(url_for("login"))


@app.route("/recipe/add", methods=["GET", "POST"])
def add_recipe():
    """
    Renders page to add a recipe.
    When form is submitted, saves new recipe to database
    and redirects user to my_recipes page.
    """
    if session.get("user"):
        if request.method == "POST":
            is_public = True if request.form.get("is_public") else False
            recipe_ingredients = request.form.get(
                "recipe_ingredients").split(";")
            recipe = {
                "recipe_name": request.form.get("recipe_name"),
                "recipe_category": request.form.get("recipe_category"),
                "recipe_img": request.form.get("recipe_img"),
                "servings": request.form.get("servings"),
                "cook_time": request.form.get("cook_time"),
                "recipe_description": request.form.get(
                    "recipe_description"),
                "recipe_ingredients": recipe_ingredients,
                "recipe_method": request.form.get("recipe_method"),
                "is_public": is_public,
                "last_updated": date.today().strftime("%B %d, %Y"),
                "created_by": session["user"]
            }
            mongo.db.recipes.insert_one(recipe)
            flash("Recipe successfully added")
            return redirect(url_for("my_recipes"))

        categories = mongo.db.categories.find().sort("recipe_category", 1)
        return render_template(
            "components/forms/add_recipe.html", categories=categories)

    else:
        flash('You need to be logged in to add a recipe')
        return redirect(url_for("login"))


@app.route("/recipe/edit/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    """
    Renders page to change recipe.
    Loads recipe data into form.
    When form is submitted, saves revised recipe to database
    and redirects user to my_recipes page.
    """
    if session.get("user"):
        if request.method == "POST":
            is_public = True if request.form.get("is_public") else False
            recipe_ingredients = request.form.get(
                "recipe_ingredients").split(";")
            updated_recipe = {
                "recipe_name": request.form.get("recipe_name"),
                "recipe_category": request.form.get("recipe_category"),
                "recipe_img": request.form.get("recipe_img"),
                "servings": request.form.get("servings"),
                "cook_time": request.form.get("cook_time"),
                "recipe_description": request.form.get(
                    "recipe_description"),
                "recipe_ingredients": recipe_ingredients,
                "recipe_method": request.form.get("recipe_method"),
                "is_public": is_public,
                "last_updated": date.today().strftime("%B %d, %Y"),
                "created_by": request.form.get("recipe_creator")
            }
            mongo.db.recipes.update(
                {"_id": ObjectId(recipe_id)}, updated_recipe)
            flash("Recipe successfully Edited!")
            return redirect(url_for("my_recipes"))

        edit = True
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
        categories = mongo.db.categories.find().sort("recipe_category", 1)
        return render_template(
            "components/forms/add_recipe.html",
            recipe=recipe, categories=categories, edit=edit)

    else:
        flash('You need to be logged in to change a recipe')
        return redirect(url_for("login"))


@app.route("/recipe/delete", methods=["POST"])
def delete_recipe():
    """
    Checks if user created recipe or is superuser.
    If yes on one, deletes recipe.
    If not, user is not able to delete recipe.
    """
    if session.get("user"):
        if request.method == "POST":
            recipe_to_delete_id = request.form.get("recipe_to_delete")
            is_superuser = bool(
                mongo.db.users.find_one(
                    {'username': session["user"], 'superuser': True}))
            is_mine_to_delete = bool(
                mongo.db.recipes.find_one(
                    {'created_by': session["user"], '_id': ObjectId(
                        recipe_to_delete_id)}))
            if is_mine_to_delete:
                mongo.db.recipes.delete_one(
                    {"_id": ObjectId(recipe_to_delete_id)})
                flash("Recipe Successfully Deleted")
                return redirect(url_for("my_recipes"))
            elif is_superuser:
                mongo.db.recipes.delete_one(
                    {"_id": ObjectId(recipe_to_delete_id)})
                flash("Recipe Successfully Deleted by admin")
                return redirect(url_for("my_recipes"))
            else:
                flash('This is not your recipe to delete')
                return redirect(url_for("my_recipes"))
    else:
        flash('You need to be logged in to delete a recipe')
        return redirect(url_for("login"))


@app.errorhandler(404)
def not_found(error):
    """
    404 error handler
    """
    flash('Something went wrong')
    return render_template("pages/error.html", error=error), 404


@app.errorhandler(500)
def server_error(error):
    """
    500 error handler
    """
    flash('Something went wrong')
    return render_template("pages/error.html", error=error), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("DEBUG"))
