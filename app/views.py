from sqlalchemy.sql.elements import Null
from werkzeug.utils import redirect
from app import app
from flask import render_template, session
from flask import request
from flask import url_for,flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
import csv
from uuid import uuid4
from flask_mail import Mail , Message
from sqlalchemy import null


app.secret_key="token"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['IMAGE_UPLOADS'] = "/Users/samuelstockhausen/Desktop/mymembership.nl/app/static/uploads"
app.config['ALLOWED_IMAGE_EXTENSIONS'] = ["PNG","JPEG", "JPG"]

db = SQLAlchemy(app)

#emails
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT'] =587
app.config['MAIL_USE_TLS']= True
app.config['MAIL_USERNAME'] = 'noreply.uros@gmail.com'
app.config['MAIL_PASSWORD'] = ''
mail=Mail(app)


class users(db.Model):

    _id = db.Column("id",db.Integer, primary_key=True)
    first_name = db.Column("first_name",db.String())
    middle_name = db.Column("middle_name",db.String())
    last_name = db.Column("last_name",db.String())
    token = db.Column("token",db.String())
    upload = db.Column("upload",db.String())
    email = db.Column("email",db.String())
    authenticated = db.Column("authenticated",db.Boolean())
    submitted = db.Column("submitted",db.Boolean())

    

    def __init__(self,first_name,last_name,token,authenticated,middle_name,email,submitted):
        self.first_name = first_name
        self.last_name = last_name
        self.token = token
        self.authenticated = authenticated
        self.middle_name = middle_name
        self.email = email
        self.submitted = submitted

db.create_all()
db.session.commit() 




class mymail():

    def send_introduction_mail(user):
        msg=Message('Upload a proof of UM-Sports membership',recipients=[user.email],sender='noreply.uros@gmail.com')
        msg.body=f''' 
Dear {user.first_name},
   
Thank you for being a member of UROS. To make sure that you fulfill all the requirements for the upcoming year we would like to ask you to upload a screenshot of your UM-Sports membership.
Please click on the link below and follow the indtructions.

{url_for('index',token = user.token ,_external=True)}  

The deadline for the upload is the 29. of october.

Thank you in advance!

Kind regards, 
Met vriendelijke groet,

Jorine van Vugt
MSAV Uros
Secretary
bestuur@uros.nl
www.uros.nl

Sportpark Jekerdal, Mergelweg 120, 6212 XK Maastricht 
Postbus 616, 6200 MD t.a.v. Jorine van Vugt
T +31 6 41 77 47 78

    '''
        mail.send(msg)

    def submitted(user):

        msg=Message('Screenshot succesfully submitted',recipients=[user.email],sender='noreply.uros@gmail.com')
        msg.body=f''' 
Dear {user.first_name},

Thank you for uploading your proof. You will soon receive an email with the results of the evaluation.

Kind regards, 
Met vriendelijke groet,

Jorine van Vugt
MSAV Uros
Secretary
bestuur@uros.nl
www.uros.nl

Sportpark Jekerdal, Mergelweg 120, 6212 XK Maastricht 
Postbus 616, 6200 MD t.a.v. Jorine van Vugt
T +31 6 41 77 47 78

'''
        mail.send(msg)

    def membership_confirmed(user):
        msg=Message('UM-Sports membership confirmed',recipients=[user.email],sender='noreply.uros@gmail.com')
        msg.body=f''' 
Dear {user.first_name},

Congratulations. Your membership has just been approved by a board member!

You don't have to do anything anymore.

Kind regards, 
Met vriendelijke groet,

Jorine van Vugt
MSAV Uros
Secretary
bestuur@uros.nl
www.uros.nl

Sportpark Jekerdal, Mergelweg 120, 6212 XK Maastricht 
Postbus 616, 6200 MD t.a.v. Jorine van Vugt
T +31 6 41 77 47 78

'''
        mail.send(msg)


    def membership_rejected(user):
        msg=Message('UM-Sports membership rejected',recipients=[user.email],sender='noreply.uros@gmail.com')
        msg.body=f''' 
Dear {user.first_name},
   
you uploaded screenshot has been rejected as a proof of your membership. Please purchase the correct one and use the link below to upload a proof once again.

{url_for('index',token = user.token ,_external=True)}  

if you have any questions, you can always contact us via bestuur@uros.nl.

Kind regards, 
Met vriendelijke groet,

Jorine van Vugt
MSAV Uros
Secretary
bestuur@uros.nl
www.uros.nl

Sportpark Jekerdal, Mergelweg 120, 6212 XK Maastricht 
Postbus 616, 6200 MD t.a.v. Jorine van Vugt
T +31 6 41 77 47 78

'''
        mail.send(msg)

with open('app/static/membership list/Members_list.csv','r') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0]!='Title'and (row[4]!='Old Member' and row[4]!='Alumni') :
            first_name=row[2]
            middle_name=row[1]
            email = row[3]
            date_of_birth = row[5]
            last_name=row[0]

            
            #token generator
            token = uuid4()
            token = str(token)
            user_exist = db.session.query(users).filter_by(first_name=first_name,middle_name =middle_name, last_name=last_name,email=email).one_or_none()


            #makes sure that users dont get added twice to the database
            if user_exist == None:
                user_read= users( first_name=first_name,middle_name =middle_name, last_name=last_name,email=email,authenticated = False, token = token,submitted = False)
                db.session.add(user_read)
                db.session.commit()
                #mymail.send_introduction_mail(user_exist) 


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".",1)[1]
    
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False



@app.route("/", methods = ["POST","GET"])
def index():
    token = None
    permission = False
    user = None

    #extracts token as GET parameter
    token = request.args.get("token")
    if token:
        session["token"] = token

    if request.files:
        image = request.files["image"]

        if image.filename =="":
            flash('THE FILE MUST CONTAIN A FILENAME!')
            return redirect(request.url)

        if not allowed_image(image.filename):
            flash('THAT IMAGE EXTENSION IS NOT ALLOWED!')
            return redirect(request.url)   
        else: 
            filename = secure_filename(image.filename)
            location = os.path.join(app.config["IMAGE_UPLOADS"], filename)

            if token is session["token"] is None:
                return redirect('index.html')

            else:
                location = location.split('app')[1]
                user = db.session.query(users).filter_by(token = session["token"]).first()
                user.upload = location
                user.submitted = True
                db.session.commit()

            image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            mymail.submitted(user)
            flash('IMAGE SUCCESFULLY UPLOADED. YOU WILL RECEIVE AN EMAIL ONCE YOUR MEMBERSHIP IS CONFIRMED!')
            return redirect(url_for('index',permission = False,user=user))

    elif request.method == "POST":
        token = request.form["token"]
        session["token"] = token
        user = db.session.query(users).filter_by(token = session["token"]).first()

        token_found = users.query.filter_by(token=token).first()
        if token_found:
            session["token"] = token_found.token
            permission = True
        
        elif token == "":
            flash('PLEASE ENTER YOUR TOKEN!')
            return redirect(url_for('index'))

        else:
            flash('TOKEN NOT VALID. PLEASE TRY AGAIN!')
            return redirect(url_for('index'))    

    else:
        if "token" in session:
            token = session["token"]
            
                    
    return render_template('index.html',token=token,permission=permission,user=user)



@app.route("/backend-eed8eebb-8cae-4ab7-b8a1-61b6b807436f",methods =['GET','POST'] )
def backend():
   
    
    
    if request.method == "POST":


        accept= request.form.get('accept', None)
        reject = request.form.get('reject', None)

        if accept:
            update = db.session.query(users).filter_by(token = accept).first()
            update.authenticated = True
            db.session.commit()
            
            mymail.membership_confirmed(update)

            
            flash('YOUR MEMBERSHIP HAS BEEN CONFIRMED!')
            return redirect(request.url)

        elif reject:
            update = db.session.query(users).filter_by(token = reject).first()
            mymail.membership_rejected(update)
            flash('MEMBERSHIP REJECTED. PLEASE PURCHASE THE CORRECT ONE AND REUPLOAD A PROOF!')
            update.submitted = False
            update.upload = null()
            db.session.commit()

            return redirect(request.url)


    return render_template("backend.html")


