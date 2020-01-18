
from flask_restful import Resource,reqparse
from flask_jwt import JWT,jwt_required
from models.item import ItemModel

class Item(Resource):

    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = 'This field cannot be left blank')

    parser.add_argument('store_id',
        type = float,
        required = True,
        help = 'Every item must have stores id')

    #identity function is not called unless we decorate our endpoint with @jwt_required
    @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name) 
        if item: 
            return item.json()
        return {'message' : 'Item not found'},404
    
    
        
    def post(self,name):
        if ItemModel.find_by_name(name) :
            return {'message' : "An item with name '{}' already exists.".format(name)},400 #400 is for Bad request
       
        data = Item.parser.parse_args()
        #data = request.get_json()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message" : "an error ocurred inserting this item"},500 #Internal server errro

        return item.json(),201
         #return item,201 #201 to indicate object has been created and added to database.
    
         

    def delete(self,name) :
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message" : "Item deleted"}

    def put(self,name):
        #in put request previously , if we explicitly mention name as well it will update , hence we are using parser for this issue
        #also , to make sure price argument is passed and no other argument can be passed
        
        data = Item.parser.parse_args()
        #data = request.get_json()

        item = ItemModel.find_by_name(name)
        
        if item == None:
            item = ItemModel(name,**data)
        else:
            item.price = data['price']
        
        item.save_to_db()

        return item.json()

    
class ItemList(Resource): 
    def get(self):
       # return {"items" : [item.json for item in ItemModel.query.all()]}
       return {"items" : list(map(lambda x : x.json(),ItemModel.query.all()))}

    def post(self,name):
        pass