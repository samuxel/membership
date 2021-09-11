# membership
membership approval flask application

If you would like to use this repository: 
1. Install the requirements.txt file and run the run.py file
2. configure the email connection in the views.py file
3. add a membership.csv file to the membership list folder

FYI: for now it is still possible to brute force the token but since its a UUID4 token it would take years to do so.

This Flask application is meant to let you check memberships.

When starting the application for the first time it creates an empty database.
It then browses user objects in a .csv file for an email adress and then generates token for each of them. The latter is then sent to the user and he can use the token to access the file upload
The token is stored in a cookie and once entered will automatically be filled into the token-input bar
The upload is limited by multiple criteria such as the file ending (.jpg , .png etc.)
From the backend which for now is unsecured, the upload of each member can either be confirmed or rejected --> The user will then receive a final email





