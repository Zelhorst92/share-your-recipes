# Testing and Bugreports

* [Testing](#testing)
    * [Search for recipes 1](#search-for-recipes-1)
    * [Navigation](#navigation)
    * [Registration](#registration)
    * [Login](#login)
    * [View Recipe](#view-recipe)

* [Bugreports](#bugreports)
    * [Feedback Hidden Recipe](#feedback-hidden-recipe)

# Testing

##  Search for recipes 1
(not logged in)
### User Expectation
As a user, I want to search for recipes.
### Intention
The main goal of the application is to search the database for recipes. The homepage does reflect this with the search function in full view. Users of the application do not have to be registered/logged in to use this function. The user can search for recipes along two types of queries; an input field where the user can type in a search term or via the category selector. The input field searches along all recipes if no category is selected and the categoryselector will show all recipes of the selecter category if no further input values are given. The user can also view all recipes by not giving any values to the search-queries. Furthermore the user can be more specific by searching within a selected category by using both queries. The database contains an index on the Name, Category and Small description of the recipes. This will result in that when search with a category alone, that some recipes might be shown which are mentioned as possibly belonging to that category but are classified as something else what would be a better fit. This is because a recipe can only have one category, but could be considered belonging to more than one. When no recipes are found, feedback is given that no recipes are found and should redirect back to the search page. When recipes are found a 'recipe card' is generated and shown to the user.
### Tests
The are 4 recipes present during this test, listed by name and category and one of which is hidden:
Name|Category
-|-
Caramel Bar|Dessert
Mango & yoghurt layer pots|Dessert
Oxtail Stew|Stew
Chicken|Main Course (hidden).


*   No queries test.
    *   By not supplying any queries, the search function should return all recipes present. Three recipes should be shown, as one is hidden.
*   Single input query test.
    *   By searching the word 'Caramel', one recipe should be shown.
    *   By searching the word 'gooey', two recipes should be shown.
    *   By searching the word 'Oxtail', one recipe should be shown.
    *   By searching the word 'Chicken', no recipes should be shown, as this recipe is hidden for public.
*   Single category query test.
    *   By selecting the category 'Stew', one recipe should be shown.
    *   By selecting the category 'Dessert', two recipes should be shown.
    *   By selecting the category 'Main Course', no recipe should be shown, as the Chicken recipe is hidden.
    *   By selecting the category 'Breakfast', the recipe Mango & yoghurt should show up as breakfast is mentioned in the description.
    *   By selecting any other categories, no recipes should be shown.
*   Both queries test.
    *   By searching for 'Caramel' and category 'Dessert', one recipe should be shown.
    *   By searching for 'Caramel' and category 'Stew', no recipe should be shown.
    *   By searching for 'Chicken' and category 'Main Course', no recipe should be shown. As this recipe is hidden for the public.
    *   By searching for 'gooey' and category 'Dessert', two recipes should be shown.
    *   By searching for 'gooey' and category 'Stew', no recipes should be shown.
### Result
*   Searching the word 'chicken', no recipes were shown, but also no feedback was given that there where 'no recipes found'. Also the page was not redirected back to the searchpage.
*   Selecting the category 'Main Course', no recipes were shown, but also no feedback was given that there where 'no recipes found'. Also the page was not redirected back to the searchpage.
*   Searching the word 'chicken' and selecting the category 'Main Course', no recipes were shown, but also no feedback was given that there where 'no recipes found'. Also the page was not redirected back to the searchpage.
*   Rest of the tests were successful. When no recipes were found, feedback was given that there were 'no recipes found' and the page redirected to the searchpage. When recipes were found, the correct ammount of recipe cards were created and shown to the user.
### Bugs
*   No redirect and adequate feedback when queries point into the direction of a hidden recipe. Feedback should be as if no recipes were found. See [Feedback Hidden Recipe](#feedback-hidden-recipe)
### Comments
*   Ofcourse with more recipes present and a public recipe for each category, this bug would not be of a great concern as there would be a recipe to show anyway.

[Back to top](#testing-and-bugreports)

##  Navigation
### User Expectation
* As a user, I want a website that is easy and intuitively to use.
* As a user, I want to see what the website is about at first glance.
* As a user, I want a website that works on all screen sizes.

### Intention
*   Navigation of the website works via two paths. The user has access to the navigationbar on the top of the page. Here the user can find the links to the searchpage, login and registration page if the user is not logged in. When the user is logged in, the links to the login and registration page disappear and the links to the user dashboard, users recipes, add recipe and logout appear.
The other navigation path is via the recipe card. The user can search for recipes via the searchpage, which leads to the found recipes. From here the user can view the individual recipes by clicking on 'view'. If the user is logged in, then also the edit and delete options are available on the recipes that are created by the user.
### Test
*   Follow through every navigation path.
### Result
*   Test passed.
### Bugs
*   None.
### Comments
*   None.

[Back to top](#testing-and-bugreports)

##  Registration
### User Expectation
*   As a user, I want to register to the website.
### Intention
*   The intent is to have a registration form where the user can register with a username, password and an emailaddress. The username and the emailadress will be checked against the database. Either can only be used once. If username and/or emailaddress is already in use, the user will be given feedback. The password will be hashed by a security plugin by werkzeug. Also the form contains basic restrictions on what characters to use and within what length limit. At sussessful registration the user is redirected to users dashboard and a sessioncookie created.
### Tests
*   Try to register with an existing username.
    *   Username: Test01, Email: test09@test.com
*   Try to register with an existing emailaddress.
    *   Username: Test09, Email: test01@test.com
*   Try to register with an existing username and emailadress.
    *   Username: Test01, Email: test01@test.com
*   Try to register a new account with new credentials.
    *   Username: Test09, Email: test09@test.com
*   Check via devtools if a session cookie was created.
### Result
*   All tests passed. Feedback was given if username or emailaddress was already in use. When registration was successful user was redirected to users dashboard.
### Bugs
*   None.
### Comments
*   None.

[Back to top](#testing-and-bugreports)

##  Log in
### User Expectation
*   As a user, I want to login to the website.
### Intention
*   The intent is that the user can login with its login details. The same form as the registration page will be used, with the exception of the email adress. User only has to provide username and password. Feedback will be given if any of the two is wrong, without telling which. This is to delay users with ill intent. After successful login, user will be redirected to user dashboard and a session cookie created.
### Tests
*   Try to login with non-existing username.
*   Try to login with existing username and wrong password.
*   Try to login in with correct credentials.
*   Check via devtools if a session cookie was created.
### Result
*   All tests passed. Feedback was given if username and/or password were incorrect. After successful login user was redirected to users dashboard.
### Bugs
*   None.
### Comments
*   None.

[Back to top](#testing-and-bugreports)

##  View Recipe
### User Expectation
*   As a user, I want to see in a recipe, including but not limited to;
    *   Whats the recipe about, ie. Recipe title.
    *   Recipe ingredients.
    *   Steps to completion.
### Intention
*   The core of the application is that the user can see the recipe and have all the information present to prepare the dish according to the recipe. Therefore it is paramount that on the recipe page, the correct data is being loaded and shown.
### Test
*   View the recipe and check if the correct data of the correct recipe is loaded.
### Result
*   Test passed.
### Bugs
*   None.
### Comments
*   None.

[Back to top](#testing-and-bugreports)

##  Add Recipe
### User Expectation
*   As a user, I want to add my own recipes.
*   I want to decide if my recipes are public or not.
### Intention
*   A registered user has the ability to add recipes to the database. When the user is logged in, in the top right the user can select 'add recipe'. This leads to a form which has all the required fields to add a recipe to the database. Most fields in the form are restricted in the ammount of characters that can be used. 
### Test
*   Add a recipe and then find it via the searchpage.
### Result
*   Test passed.
### Bugs
*   None.
### Comments
*   None.

[Back to top](#testing-and-bugreports)

##  Category Selection
### User Expectation
*   As a user, I want to change my recipes.
*   I want to decide if my recipes are public or not.
### Intention
*   When a registered user has added a recipe, the user also has the ability to edit said recipe. Via the my recipes page or via the searchpage if the user found its own recipe, the user can click on 'Edit' on the recipe card. This loads the same form from adding a recipe, but with the fields already filled in. The user can change all the data in the form and then save the recipe again to the database.
### Test
*   Edit a recipe, making sure the recipe is actually changed and not saved as a new recipe by checking the database before and after editing.
### Result
*   Test passed.
### Bugs
*   None.
### Comments
*   None.

[Back to top](#testing-and-bugreports)

##  Superuser
### Owner story
*   As an owner, I want to maintain the recipes
### Intention
*   If recipes need editing or deleting because of any reason, a superuser should be able to do this. Therefore a user can be flagged as a superuser in the database, which would grant this superuser the ability to edit and delete any recipe. The superuser is also able to view, edit and delete private recipes.
### Test
*   Log in as the admin, which is flagged 'superuser'.
    *   Find the hidden chicken recipe.
    *   Check if the superuser can edit and delete all the recipes.
### Result
*   Tests passed.
### Bugs
*   None.
### Comments
*   None.

[Back to top](#testing-and-bugreports)

##  Deletion
### User Expectation
*   As a user, I want to change my recipes.
### Intention
*   In addition to add and editing recipes, the user is able to delete its recipes. And only the recipes created by the user. Therefore multiple checks are in place to see if the logged in user is trying to delete its own recipe. First of the webpage will not generate the delete button if the logged in user is not the same as the recipes creator. It works the same with the confirmation modal. Then in the backend the logged in user name will be checked again against the recipe creator, before deletion can be executed.
When the user tries to delete a recipe, a modal will pop up asking to confirm to delete said recipe and telling the user that the deletion cannot be undone. Upon confirming, the recipe will be deleted.
### Test
*   Delete a recipe.
### Result
*   Test passed.
### Bugs
*   None.
### Comments
*   None.

[Back to top](#testing-and-bugreports)

---

# Bugreports
## Feedback Hidden Recipe
### Bug
*   No redirect and adequate feedback when queries point into the direction of a hidden recipe. Feedback should be as if no recipes were found.
### Fix
*   
### Conclusion/Result
*   
### Status
*   Unresolved

[Back to top](#testing-and-bugreports)

