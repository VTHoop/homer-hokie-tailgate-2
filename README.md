# homer-hokie-tailgate-2

http://homer-hokie-tailgate.herokuapp.com/

### Summary
This web application is designed to allow users to register and interact socially with the other members of their specific tailgate.  A website was initially launched in 2010 and this is the second iteration of the website.

### Technology
* Python
* Flask
* Jinja2
* MongoDB
* Mailgun (in the near future)
* Bootstrap CSS and jQuery

Currently hosted on free tier of heroku as a QA box.

### Features

##### Score Prediction Game 
Users can enter their score predictions and based on the point system will get their leaderboard updated as the games occur
##### Game Information
Information for the game is scraped from the Virginia Tech Football website and displayed to the users
##### Attendance
Users will indicate their attendance and the summary of that attendance is listed for each gaem
##### Ticket Marketplace
Users can list new tickets and needed tickets to exchage with the tailgate
##### Game Menu Planner
Users can list menu items that they will bring to the game

### Folder Structure
* Dev  
  This folder is used strictly for offline testing and file transfer when not on main developmemnt machine
* Src  
  This is the main source folder
  *  Common  
     Used for global utilities
  *  Models  
     Standard folders for Python objects and their Flask views
  *  Static  
     Images, JS, CSS
  *  Templates  
      Standard folders for Jinja templating based on each Python object
