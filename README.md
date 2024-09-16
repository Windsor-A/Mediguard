[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/qgEWmaMc)
# Project A-25

__Name:__Thomas Antal, Kaitlin Cole, Sahlar Salehi, Anuti Shah, Yoon Lee

__Computing ID:__yrz2yy, ftr6fb, rmh7ce, jyr3um, fnb5ww

General Features: 
Welcome to our app, MediGuard. The primary purpose of our website is to serve as a whistleblower app to report medical 
malpractice. You will find a button on the home page of our app that you can click on to submit reports. You may click
on the app logo or MediGuard at the top left of the page at any time to return home. There is a dropdown menu available
on the right side of the header where you can either login (if not already), logout (if logged in), and view your user 
dashboard (if already logged in). On the user dashboard, you will be able to see what type of user you are, as well as
any reports you have submitted, if any. If you would like, you can delete any previously made reports at any time. The
status of your report will be listed along with the Subject of your report. Click on the report card at any time to 
view more details on your report. Once a new report is submitted, you will be taken to a report submitted page, where you 
can either view the details of the report you just made or submit a new report. There is an additional feature you 
can view when looking at the details of a given report. The practice name serves as a link to a practice detail page, 
where you can view the number of reports made and any reports you, as a user, made on said practice. All reports made on 
the practice can be viewed by site admin, but not by common users. 

User Capabilities: 
There are four different types of users that interact with our app: anonymous, common, site admin, and django admin. 
Anonymous users are users who are not logged in yet. When you first click on the link to access our app, you will by 
default be an anonymous user. No information about anonymous users is stored. You can click on the login button at the 
top right of the page to login via a Google account. Logging in this way makes you a common user. A Django admin has 
access to the Django admin page. However, a Django admin is only registered as a common user in the app itself. 
For testing purposes, we have made a Django admin for you. The email is: cs3240.django@gmail.com / user: admin / pass: admin. 
To access the Django admin login/ type in /admin after the URL of the website. As a Django admin, you have the ability to 
elevate the status of any common user to a site admin via a group titled "Site admin" on the Django admin page. Do this 
to test the site admin functionalities. As a site admin, there is an additional "View All Reports" button in the 
center of the header of the app. If you click on this, you can view a list of all the reports made. These reports are 
shown as various "cards." They are sorted from left to right, with "New" reports first, followed by "In Progress," and 
finally, "Resolved." On top of the status sorting, each status is sorted from left to right by time published, with the 
newest showing at the top and furthest to the left. Any of these cards can be clicked on by site admin to view report 
details and resolve the report, with the option of submitting a resolution text along with it. Users who made the report
can then view the status of their report on their user dashboard. 

This is the basic outline of the functionality of our app. 