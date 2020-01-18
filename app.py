from flask import Flask
from flask_restful import Resource,Api
from flask_jwt import JWT
from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.stores import Stores,StoresList
from dbmain import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'Omii'
api = Api(app)

jwt = JWT(app,authenticate,identity) # /auth

@app.before_first_request
def create_table():
    db.create_all()

#api.add_resource(Student , '/student/<string:name>') #http://127.0.0.1:5000/student/Rolf
api.add_resource(Stores,'/store/<string:name>')
api.add_resource(Item , '/item/<string:name>')
api.add_resource(ItemList , '/items')
api.add_resource(StoresList, '/stores')
api.add_resource(UserRegister, '/register')

#suppose we import app.py in user.py , in that case all the methods such as app.run, app.secret_key in app.py 
#will execute . And we dont want app to start when we import app.py in user.py 
#hence to prevent such case, we use __name_- =='__main__'.
#Whenever we execute as -> python app.py , python sets new name to app.py ie __main__ , so it knows which is executable file.
if __name__ == '__main__' : 
    db.init_app(app) 
    app.run(port=5000, debug = True)