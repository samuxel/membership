# membership
membership approval flask application

If you would like to use this Flask application for yourself: 
1. Install FLASK
2. Install the requirements.txt file and run the run.py file
3. configure the email connection in the views.py file
4. add a membership.csv file to the membership list folder

FYI: for now it is still possible to brute force the token but since its a UUID4 token it would take years to do so.

This Flask application is meant to let you check memberships.
Its responsive and its content can therefore be viewed on all kind of devices

When starting the application for the first time it creates an empty database.
It then browses user objects in a .csv file for an email adress and then generates token for each of them. The latter is then sent to the user and he can use the token to access the file upload
The token is stored in a cookie and once entered will automatically be filled into the token-input bar
The upload is limited by multiple criteria such as the file ending (.jpg , .png etc.)
From the backend which for now is unsecured (its a url that requires a hardcoded token to access), the upload of each member can either be confirmed or rejected --> The user will then receive a final email

Possible improvements:
Better backend
Advanced error catching






