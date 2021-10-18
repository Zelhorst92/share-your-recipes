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
    return render_template("home.html", categories=categories)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    query2 = request.form.get("query2")
    if query == "" and query2 == "":
        recipes = list(mongo.db.recipes.find().sort("recipe_name", 1))
        return render_template("recipes.html", recipes=recipes)
    elif query == "":
        recipes = list(mongo.db.recipes.find({"$text": {"$search": query2}}).sort("recipe_name", 1))
        return render_template("recipes.html", recipes=recipes)
    else:
        recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}).sort("recipe_name", 1))
        return render_template("recipes.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        # check if email already exists in db
        existing_email = mongo.db.users.find_one(
            {"email": request.form.get("email").lower()})

        if existing_user:
            flash("Username already in use, please try again")
            return redirect(url_for("register"))

        elif existing_email:
            flash("Email already in use, please try again")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "email": request.form.get("email").lower(),
            "superuser": False
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successfull")
        return redirect(url_for(
            "dashboard", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # check if input password matches hashed password
            if check_password_hash(existing_user["password"], request.form.get(
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

    return render_template("login.html")


@app.route("/dashboard/<username>", methods=["GET", "POST"])
def dashboard(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("dashboard.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # Remove user session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/view_recipe", methods=["GET", "POST"])
def view_recipe():
    full_recipe = request.form.get("full_recipe")
    recipe = list(mongo.db.recipes.find({"_id": ObjectId(full_recipe)}))
    return render_template("recipe.html", recipes=recipe)


@app.route("/my_recipes")
def my_recipes():
    if session["user"]:
        recipes = list(mongo.db.recipes.find({"$text": {"$search": session["user"]}}).sort("recipe_name", 1))
        return render_template("my_recipes.html", recipes=recipes)
    else:
        flash('You need to be logged in to see your recipes')
        return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        is_public = True if request.form.get("is_public") else False
        recipe_ingredients = request.form.get("recipe_ingredients").split(",")
        recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "recipe_category": request.form.get("recipe_category"),
            "recipe_img": request.form.get("recipe_img"),
            "servings": request.form.get("servings"),
            "cook_time": request.form.get("cook_time"),
            "recipe_description": request.form.get("recipe_description"),
            "recipe_ingredients": recipe_ingredients,
            "recipe_method": request.form.get("recipe_method"),
            "is_public": is_public,
            "last_updated": date.today().strftime("%B %d, %Y"),
            "created_by": session["user"]
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe successfully added")
        # Dont forget to change url below to my recipes when ready
        return redirect(url_for("add_recipe"))

    categories = mongo.db.categories.find().sort("recipe_category", 1)
    return render_template("add_recipe.html", categories=categories)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":
        is_public = True if request.form.get("is_public") else False
        recipe_ingredients = request.form.get("recipe_ingredients").split(",")
        updated_recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "recipe_category": request.form.get("recipe_category"),
            "recipe_img": request.form.get("recipe_img"),
            "servings": request.form.get("servings"),
            "cook_time": request.form.get("cook_time"),
            "recipe_description": request.form.get("recipe_description"),
            "recipe_ingredients": recipe_ingredients,
            "recipe_method": request.form.get("recipe_method"),
            "is_public": is_public,
            "last_updated": date.today().strftime("%B %d, %Y"),
            "created_by": session["user"]
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, updated_recipe)
        flash("Recipe successfully Edited!")
        # Dont forget to change url below to my recipes when ready
        
        return redirect(url_for("my_recipes"))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = mongo.db.categories.find().sort("recipe_category", 1)
    return render_template(
        "edit_recipe.html", recipe=recipe, categories=categories)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
