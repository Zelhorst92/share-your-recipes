# Share your Recipes!

# Introduction

Welcome...

# Table of Content
- [User Experience](#user-experience)
  * [Site Owner Goal](#site-owner-goal)
  * [User Goals](#user-goals)
  * [User Stories](#user-stories)
  * [User Requirements](#user-requirements)
  * [User Expectations](#user-expectations)
- [Design](#design)
  * [Wireframes](#wireframes)
  * [Design Choices](#design-choices)
    * [The Structure](#the-structure)
    * [Fonts](#fonts)
    * [Colours](#colours)
  * [Database Structure](#database-structure)
  * [Logic Flowchart](#logic-flowchart)
- [Features](#features)
  * [Existing Features](#existing-features)
  * [Future Features](#future-features)
- [Technologies](#technologies)
  * [Languages](#languages)
  * [Libraries and Tools](#libraries-and-tools)
- [Testing](#testing)
- [Deployment](#deployment)
  * []
- [Credits](#credits)
  * [Code](#code)
  * [Thanks](#thanks)
  * [Afterword](#afterword)

# User Experience
## Site Owner Goal
* Having users find, add and share recipes.
* A way to maintain all the recipes , ie an admin/superuser role.

---

## User Goals
* A website where you can find and share recipes
* A website that is easy to use on all screen sizes with appropriate responsiveness.
* A website where I can register and login to.
* Having a dashboard with all my own recipes

---

## User Stories
As a user;
* I want a website that is easy and intuitively to use.
* I want to see what the website is about at first glance.
* I want a website that works on all screen sizes.
* I want to register to the website.
* I want to login to the website.
* I want to be able to search for more specific recipes.
* I want to add my own recipes.
* I want to decide if my recipes are public or not.
* I want to change my recipes.
* I want to see in a recipe, including but not limited to;
    * Whats the recipe about, ie. Recipe title.
    * Recipe ingredients.
    * Steps to completion.
* ~~I want the recipe maker know that I cooked their dish today/liked their recipe.~~

[Back to top](#table-of-content)

---

## User Requirements
* Easy navigation.
* Intuitively know what the website is about.
* The ability to register.
* The ability to login and therefore access there own recipe dashboard.
* The ability to search for recipes.
* The ability to add/remove (own) recipes.

## User Expectation
* A user dashboard for navigation to own recipes, add or change recipes.
* An overview of all own recipes.
* A form to add/change a recipe.
* The ability to filter down search parameters to find a more specific recipe.

[Back to top](#table-of-content)

---

# Design
## Wireframes
I have made wireframes for the sizes Mobile, Tablet and Desktop.
As per Bootstrap order, from small to large. To make the wireframes I have used the program [Balsamig Wireframes](https://balsamiq.com/wireframes/ "Link to Balsamig Wireframes").

#### Mobile Wireframes
* [Mobile Wireframe Home](/wireframes/home-mobile.png)
* [Mobile Wireframe User Dashboard](/wireframes/user-dashboard-mobile.png)
* [Mobile Wireframe Own Recipe Overview](/wireframes/own-recipes-overview-mobile.png)
* [Mobile Wireframe View Recipe](/wireframes/view-recipe-mobile.png)
#### Tablet Wireframes
* [Tablet Wireframe Home](/wireframes/home-tablet.png)
* [Tablet Wireframe User Dashboard](/wireframes/user-dashboard-tablet.png)
* [Tablet Wireframe Own Recipe Overview](/wireframes/own-recipes-overview-tablet.png)
* [Tablet Wireframe View Recipe](/wireframes/view-recipe-tablet.png)
#### Desktop Wireframes
* [Desktop Wireframe Home](/wireframes/home-desktop.png)
* [Desktop Wireframe User Dashboard](/wireframes/user-dashboard-desktop.png)
* [Desktop Wireframe Own Recipe Overview](/wireframes/own-recipes-overview-desktop.png)
* [Desktop Wireframe View Recipe](/wireframes/view-recipe-desktop.png)
#### Other Wireframes
* [Wireframe Register/Login](/wireframes/register-login.png)
* [Wireframe Add or Change Recipe](/wireframes/add-change-recipe.png)

[Back to top](#table-of-content)

## Design Choices
The goal of this site is that users can find, view and add recipes. So readability is paramount with not much other distractions.

### The structure
For the structure of the website I will use the framework [Bootstrap](https://getbootstrap.com/ "Link to bootstrap").
This framework allows for a proper responsive website which is build up from a mobile-first perspective.
The grid-system that Bootstrap provides is very usefull to have a well working responsive website.
Furthermore Bootstrap has a wide browser compatibility, is quite easy to use and is very customizable.

As a starting point I will begin with the template provided by [Startbootstrap](startbootstrap.com/ "Link to startbootstrap"), specifically the [Landingpage](https://startbootstrap.com/previews/landing-page "Link to startbootstrap landingpage"). This will be heavily modified to suit my needs.

### Fonts
I will be using a font from [Google Fonts](https://fonts.google.com/ "Google Fonts"), specifically the [Nanum Gothic](https://fonts.google.com/specimen/Nanum+Gothic "Nanum Gothic").
An easy to read, compact, professional looking font.

### Colours
I have chosen for a colour scheme that goes easy on the eyes, as most of what the user will be doing is reading the recipes. With that it is not desirable to have colours which are to bright, hampering readability.

![Colour Pallette Scheme](https://github.com/Zelhorst92/share-your-recipes/blob/main/wireframes/colourpallette.png?raw=true "Colour Pallette Scheme")

The colour pallette exists out of 5 colours, with a mix of colour inbetween marked with a *. The * colours are only to be used if the five main colours do not fit very well.

* #375412: Dark Moss Green
* #718161: Xanadu*
* #ABADB0: Silver Chalice 
* #D5D6D8: Light Grey*
* #FFFFFF: White
* #8C8C8C: Battleship Grey*
* #191919: Eerie Black
* #97271B: Falu Red*
* #D9351C: Vermilion 

[Back to top](#table-of-content)

---

## Database Structure

#### User
Key|Value
-|-
_id|ObjectId
username|String
password|String
email|String
is_superuser|Boolean

#### Recipe
Key|Value
-|-
_id|ObjectId
recipe_name|String
recipe_category|String
recipe_description|String
servings|String
cooking_minutes|String
recipe_img|String
recipe_ingredients|Array
recipe_method|Array
is_public|Boolean
created_by|String

#### Category
Key|Value
-|-
_id|ObjectId
recipe_category|String

[Back to top](#table-of-content)

---

## Logic Flowchart

[Back to top](#table-of-content)

---

# Features
## Existing Features

## Future Features

[Back to top](#table-of-content)

---

# Technologies
## Languages
*   [HTML](https://en.wikipedia.org/wiki/HTML "Link to the HTML wikipedia page")
*   [CSS](https://en.wikipedia.org/wiki/CSS "Link to the CSS wikipedia page")
*   [JavaScript](https://en.wikipedia.org/wiki/JavaScript "Link to the JavaScript wikipedia page")

## Libraries and Tools
### Libraries & Frameworks
*   ~~[Bootstrap](https://getbootstrap.com/ "Link to bootstrap")~~
*   ~~[Fontawsome](https://fontawesome.com/ "Link to fontawesome")~~
*   [Googlefonts](https://fonts.google.com/ "Link to googlefonts") 
*   [Open Trivia Database](https://opentdb.com/ "Link to open trivia database")

### Tools
*   [Gitpod](https://www.gitpod.io/ "Link to gitpod")
*   [Github](https://github.com/ "Link to github")
*   [Git](https://git-scm.com/ "Link to git")
*   [Tinypng](https://tinypng.com/ "Link to tinypng") 
*   [Balsamiq Wireframes](https://balsamiq.com/wireframes/ "Link to balsamiq wireframes")
*   [W3C Css-validator](https://jigsaw.w3.org/css-validator/ "Link to the w3 css validator")
*   [W3C Markup-validator](https://validator.w3.org/ "Link to w3c markup validator")
*   [Techsini](http://techsini.com/ "techsini.com")
*   [Favicon.cc](https://www.favicon.cc/)

[Back to top](#table-of-content)

---

# Testing
This is done in a seperate file:

[TESTING.md](https://github.com/Zelhorst92/share-your-recipes/blob/main/TESTING.md "Link to tests and bugs file")

---

# Deployment
## Deployment via GitHub Pages
The website was deployed via GitHub by following the steps below:
-   Go to the repository you want to deply on github.
-   Click on the **Settings** tab
-   Go to **Pages** on the left side navigation
-   In the **Source** section, there is a dropdown menu; select the **master** branch and **root**. Click **save**.
-   Within a short moment the website is live.
    You will see a link on the top of the GitHub Pages section, either in a blue or green field.
    -   Example on how the **link** will look like and coincidently the link to the current website: [https://zelhorst92.github.io/GeKnoQu/](https://zelhorst92.github.io/GeKnoQu/ "Link to the deployed website")
-   Any time you will push to Github, the update will be visible after a short while.

## Deployment of the website locally:
-   Click on the dropdown menu which says **Code** on the Github Repository.
-   You will see several options; 
    -   **Clone with a link**, 
    -   **Open with GitHub Desktop** 
    -   **download ZIP**

#### Clone with a link
-   When you want to clone; use the **Clone with HTTPS option**, copy the link displayed.
-   Open your IDE and go to the terminal.
-   Change the working directory to the location where the cloned directory is to go.
-   Use the **git clone** command and paste the url copied in the second step.

#### Open with GitHub Desktop
-   If you have GitHub Desktop installed, you can click on this and it will import and clone the repository for you, after selecting where it needs to go.

#### Download the ZIP
-   You can also download the whole repository in a zip file and use the IDE software you want.

[Back to top](#table-of-content)

# Credits
## Code
###
###

## Thanks

## Afterword

...

Robert L. Zelhorst

[Back to top](#table-of-content)