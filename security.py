from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username,password) : 
    user = UserModel.find_by_username(username) #if username is not present return none
    if user and safe_str_cmp(user.password,password):#safe_str_cpm : safe string comparison : to check if user.password == password. we used this to resolve unicode issue
        return user

def identity(payload) : #inbuilt module for JWT , payload is content for JWT token
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)