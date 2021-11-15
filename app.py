import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def home():
    categories = mongo.db.categories.find().sort("recipe_category", 1)
    return render_template("components/home.html", categories=categories)


@app.route("/search", methods=["GET", "POST"])
def search():
    inputquery = request.form.get("inputquery")
    categoryquery = request.form.get("categoryquery")
    try:
        if session["user"]:
            is_superuser = bool(
                mongo.db.users.find_one(
                    {'username': session["user"], 'superuser': True}))
    except:
        is_superuser = False
    finally:
        if inputquery == "" and categoryquery == "":
            recipes = list(mongo.db.recipes.find().sort("recipe_name", 1))
        elif inputquery == "":
            recipes = list(mongo.db.recipes.find(
                {"$text": {"$search": categoryquery}}).sort("recipe_name", 1))
        else:
            recipes = list(mongo.db.recipes.find(
                {"$text": {"$search": inputquery}}).sort("recipe_name", 1))
    return render_template(
        "pages/recipes.html", recipes=recipes, is_superuser=is_superuser)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Registers an account for the user.
    Checks if there is a sessioncookie.
    Cannot register if user is already logged in.
    Gives feedback that user is already logged in.
    Redirects to dashboard if user is  already logged in.
    Checks if username and/or emailadress are already in use.
    Cannot register with same username or emailadress.
    Gives feedback if username and/or email adress is already in use.
    After registration is successfull,
    creates session cookie and redirects to users dashboard.
    """
    try:
        if session["user"]:
            flash('You are already logged in, no need to register again')
        return redirect(url_for(
            "dashboard", username=session["user"]))

    except:
        if request.method == "POST":
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})
            existing_email = mongo.db.users.find_one(
                {"email": request.form.get("email").lower()})

            if existing_user:
                flash("Username already in use, please try again")

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

        return render_template("components/forms/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login function with username and password.
    Checks if there is a sessioncookie.
    Cannot log in if user is already logged in.
    Gives feedback that user is already logged in.
    Redirects to dashboard if user is  already logged in.
    Checks if username and password are a correct match.
    Gives feedback if username and/or password is incorrect.
    After login is successfull,
    creates session cookie and redirects to user dashboard.
    """
    try:
        if session["user"]:
            flash('You are already logged in')
        return redirect(url_for(
            "dashboard", username=session["user"]))

    except:
        if request.method == "POST":
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})
            if existing_user:
                if check_password_hash(
                    existing_user["password"], request.form.get(
                        "password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(request.form.get("username")))
                    return redirect(url_for(
                        "dashboard", username=session["user"]))
                else:
                    flash("That's incorrect, please try again.")
                    return redirect(url_for("login"))
            else:
                flash("That's incorrect, please try again.")
                return redirect(url_for("login"))

        return render_template("components/forms/login.html")


@app.route("/dashboard/<username>", methods=["GET", "POST"])
def dashboard(username):
    """
    Checks if there is a sessioncookie.
    Gives feedback that user needs to be logged in to see dashboard.
    Redirects to log in page if user is not logged in.
    Show correct dashboard according to session cookie.
    If there is no session cookie, redirects to log in page.
    """
    try:
        if session["user"]:
            username = mongo.db.users.find_one(
                {"username": session["user"]})["username"]
            return render_template("pages/dashboard.html", username=username)
    except:
        flash('You need to be logged in to see your dashboard')
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """
    Removes user session cookie.
    Gives feedback that user has been logged out.
    Redirects to log in page.
    """
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/view_recipe", methods=["GET", "POST"])
def view_recipe():
    """
    Finds full recipe with recipe id.
    """
    full_recipe = request.form.get("full_recipe")
    recipe = list(mongo.db.recipes.find({"_id": ObjectId(full_recipe)}))
    return render_template("pages/recipe.html", recipes=recipe)


@app.route("/my_recipes")
def my_recipes():
    """
    Checks if there is a sessioncookie.
    Gives feedback that user needs to be logged in to see its recipes.
    Redirects to log in page if user is not logged in.
    If logged in, shows all recipes created by user.
    """
    try:
        if session["user"]:
            recipes = list(mongo.db.recipes.find(
                {"$text": {"$search": session["user"]}}).sort(
                    "recipe_name", 1))
            return render_template("pages/recipes.html", recipes=recipes)
    except:
        flash('You need to be logged in to see your recipes')
        return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    """
    Checks if there is a sessioncookie.
    Gives feedback that user needs to be logged in to add a recipe.
    Redirects to log in page if user is not logged in.
    If logged in, renders page to add recipe.
    When form is submitted, saves new recipe to database.
    Gives feedback that new recipe has been saved.
    """
    try:
        if session["user"]:
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

    except:
        flash('You need to be logged in to add a recipe')
        return redirect(url_for("login"))


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    """
    Checks if there is a sessioncookie.
    Gives feedback that user needs to be logged in to change a recipe.
    Redirects to log in page if user is not logged in.
    If logged in, renders page to change recipe.
    Loads recipe data into form.
    When form is submitted, saves revised recipe to database.
    """
    try:
        if session["user"]:
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

            recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
            categories = mongo.db.categories.find().sort("recipe_category", 1)
            return render_template(
                "components/forms/edit_recipe.html",
                recipe=recipe, categories=categories)

    except:
        flash('You need to be logged in to change a recipe')
        return redirect(url_for("login"))


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    """
    Checks if there is a sessioncookie.
    Gives feedback that user needs to be logged in to delete a recipe.
    Redirects to log in page if user is not logged in.
    If user is logged in;
    checks if recipe is created by logged in user.
    checks if logged in user is superuser.
    If yes on one, deletes recipe.
    If not, user is not able to delete recipe.
    Gives feedback that logged in user is not able to delete recipe.
    """
    try:
        if session["user"]:
            is_superuser = bool(
                mongo.db.users.find_one(
                    {'username': session["user"], 'superuser': True}))
            is_mine_to_delete = bool(
                mongo.db.recipes.find_one(
                    {'created_by': session["user"], '_id': ObjectId(recipe_id)}))
            if is_mine_to_delete:
                mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})
                flash("Recipe Successfully Deleted")
                return redirect(url_for("my_recipes"))
            elif is_superuser:
                mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})
                flash("Recipe Successfully Deleted by admin")
                return redirect(url_for("my_recipes"))
            else:
                flash('This is not your recipe to delete')
                return redirect(url_for("my_recipes"))

    except:
        flash('You need to be logged in to delete a recipe')
        return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=os.environ.get("DEBUG"))
