
### 1. Team

605078 Relja Paunovic
605052 Sakshyam Panda
604626 Sharbel Dahlan


### 2. Goal

In this project, we build an online javascript game store with the following features
	1. This platform serves both players and developers. 
	2. Developers can sell their games by adding it to the platform with a price tag. 
	3. Players can buy games from a broader range of games and play the purchased games online.
	4. Players can see high score and load/save their current state.
	5. Developers can see sales statistics. 
	6. Login with social media accounts eg. Facebook, G+
	7. API for accesing possible games and game statistics
	8. Develop our own javascript game eg. navigate through maze using touch/mouse
	9. Making the platform responsive (different screen size eg PC, Mobile and Tablets)
	10. Include secure coding practices. 
	11. Social media sharing eg. Facebook
	12. User Experience testing
	13. Maintaing stability of the platform.

	
### 3. Plans

In this section, we describe approaches to be employed to achieve the goals

We plan to use Bootstrap to achieve a responsive and homogenous design. To have a reliable 
and stable application, we want to use django framework's built-in security mechanisms. Additionally,
for secure coding practices, we will use OWASP practices. 

We plan to use REST API to access statistics such as highscores, available games, and game sales. 
For graphs and data visualization, we plan on using D3 JavaScript library.

Our enthusiasm does not stop us from implementing a JavaScript game using multitouch libraries such
as Hammer.js, to create a simple maze game for testing purposes of our platform.

While designing the user interface, we are going to use agile design practices with
user testing to ensure that our design is user friendly.

For development purposes we will use simple sqlLite database,provided by django, and for actual deployent we will
switch to something more reliable eg. Firebase database.


#### 3.1. Pages

Our intended design will have a minimum of five pages (excluding login).
	1. Landing page (home page), where users can browse existing games on platform
	2. Game page, where users can play games if they own it(with a possible commenting and rating the game),
	  trial the game and buy it if they like it (it will take them to a 3. page)
	3. Page for buying the game with a form to enter details.
	4. Dashboard like view for a developer to see sales statistics about his/hers games, add/remove/update games and 
	   update their information
	5. Page for a user where he can see the games he/she purchased and see and change it's information


#### 3.2. Priorities

Our priority is to implement all the mandatory features in our minumum viable product. These include:

  - Developers can upload a game.
  - Users can purchase the game (without trial first).
  - Users can play a game they purchased.
  
In later iterations we can add more functionality discussed such as:
  - Having trials before purchasing the game.
  - Having game statistics such as highscores.
  - Saving/loading a game  
  - Rating and commenting on games 
 
In even later iterations:
  - Filtering games (such as sorting by rating, searching specific games)
  - Categorizing games (action, sports, adventure, strategy, horror, etc.)

  
### 4. Process and Time Schedule

We plan to hold two meetings in person every week to report on the status and discuss next steps.

* Weeks 1-2: Learn about basics, come up with a rough structure of the system using the MVC model and 
				establishing the connection with the database. Deploy the project to Heroku to check
				if it works.

* MILESTONE 1: Connection of model with the database is established.

* Weeks 3-4: Establish communication between different elements using REST API

* MILESTONE 2: Communication among MTV is working and games are accessible.

* Weeks 5-6: Testing and user experience enhancement. Work will be done on Bootstrap and CSS 

* MILESTONE 3: Prototype is refined based on User testing.

* Friday, Feb 17th: Mental breakdown after project suddenly stops working

* Sunday, Feb 19th: Celebration of successful project completion with beers


### 5. Testing

As addressed in the Plans section, small testing will be done during each week, based on which the design 
will be updated. Then a larger test will be done during weeks 5 and 6 with users.  
