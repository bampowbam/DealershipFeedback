from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'
   
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:*******@localhost/dealership'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xkbosnnjreognb:9a4eac938ed3590f1931315bd185efa3f8d98ce6c6ace26160c298402ae19be8@ec2-54-235-104-136.compute-1.amazonaws.com:5432/dckefpmha2quh8'

app.config['SQLALCHEMY_TRACK_MODICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/')
#design pattern in Python that allows a user to add 
#new functionality to an existing object without modifying its structure.
def index():
    return render_template('index.html')

#@app.route("/") is a decorator which adds an endpoint to the app object. 
#It doesn't actually modify any behavior of the function, and is instead sugar to simplify the process.
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        print(id, customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html',
            message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, dealer, rating, comments)
            return render_template('success.html')
        return render_template('index.html',
            message='You have already submitted feedback')

if __name__ == '__main__': 
    
    app.run()
