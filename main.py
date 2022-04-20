from flask import Flask, request, render_template,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime
from gevent import pywsgi

app = Flask(__name__)
db = SQLAlchemy()

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:x29802090@localhost:5432/restaurant"
db.init_app(app)

class Restaurant_model(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    restaurantname = db.Column(
        db.String(255),nullable=False)
    type = db.Column(db.String(255), nullable=False)
    county = db.Column(
        db.String(255), nullable=False)
    state = db.Column(
        db.String(255), nullable=False)
    address = db.Column(
        db.String(255), nullable=False)
    url = db.Column(
        db.String(255), nullable=False)
    comment = db.Column(
        db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, onupdate=datetime.now, default=datetime.now)


    def __init__(self, restaurantname, type, county, state, address,url,comment):
        self.restaurantname = restaurantname
        self.type = type
        self.county = county
        self.state = state
        self.address = address
        self.url = url
        self.comment = comment

@app.route('/')
def home():
    return render_template('Homepage.html')

@app.route("/form_enter", methods=['GET', 'POST'])
def enter_submit():
    if request.method == 'POST':
        data_get = request.form.get
        EnterRestaurantname=data_get('formEnterRestaurantname')
        EnterType=data_get('formEnterType')  
        EnterCounty=data_get('inputCounty')
        EnterState=data_get('inputState')
        Enteraddress=data_get('formEnteraddress')
        EnterURL=data_get('formEnterURL')
        Entercomment=data_get('formEntercomment')
        Restaurantdata=Restaurant_model(EnterRestaurantname,EnterType,EnterCounty,EnterState,Enteraddress,EnterURL,Entercomment)
        # Enterdata=[EnterRestaurantname , EnterType , EnterCounty , EnterState , Enteraddress , EnterURL , Entercomment]
        flash('ok')
        db.session.add_all([Restaurantdata])
        db.session.commit()
        return redirect(url_for('home'))
    return 'error'



@app.route('/result')
def resultpage():
    return render_template('result_page.html')

@app.route("/form_search", methods=['GET', 'POST'])
def send_submit():
    if request.method == 'POST':
        data_get = request.form.get
        searchRestaurantname=data_get('search_name')
        searchType=data_get('search_type')  
        searchCounty=data_get('search_county')
        searchState=data_get('search_state')
        temp_data=[]
        get_data = (db.session.query(Restaurant_model).filter(or_(Restaurant_model.restaurantname == searchRestaurantname,Restaurant_model.type==searchType,Restaurant_model.county==searchCounty,Restaurant_model.state==searchState)).all())
        for i in get_data:
            
            temp=[i.__dict__.pop(key) for key in ['_sa_instance_state','created_at', 'updated_at','id']]
            i=i.__dict__
            temp_data.append([i['restaurantname'],i['type'],i['county'],i['state'],i['address'],i['url'],i['comment']])
        print(temp_data)        
        return render_template('result_page.html',result_data=temp_data) #//form_search 傳送data給前端跳轉後的頁面
    return 'error'



if __name__ == "__main__":
    app.secret_key='restaurant_key'
    app.run(debug=True)