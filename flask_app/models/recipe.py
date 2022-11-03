from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Recipe:
    db="recipes_schema"
    def __init__(self, data):
        self.id=data["id"]
        self.name=data["name"]
        self.description=data["description"]
        self.instructions=data["instructions"]
        self.under_30=data["under_30"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.creator_id=data["creator_id"]
    
    '''READ ALL'''
    @classmethod
    def select_all(cls):
        query="SELECT * FROM recipes"
        results=connectToMySQL(cls.db).query_db(query)
        return [cls(e) for e in results]

    '''READ ONE'''
    @classmethod
    def select_one(cls, data):
        query="SELECT * FROM recipes JOIN users ON users.id = creator_id WHERE recipes.id=%(id)s"
        result=connectToMySQL(cls.db).query_db(query, data)
        # [{'id': 1, 'description': 'delicious blueberries in a pie crust', 'name': 'blueberry pie', '
        # instructions': 'prepare dough, /nmake filling with blueberries, bake', 'under_30': 'N', 'created_at': datetime.datetime(2022, 3, 8, 9, 36, 23), 'updated_at': datetime.datetime(2022, 3, 8, 9, 36, 23), 
        # 'creator_id': 1, 'users.id': 1, 'first_name': 'blue', 'last_name': 'berry', 'email': 'blueberry@pie.com', 'password': 'Passw0rd!', 'users.created_at': datetime.datetime(2022, 3, 8, 9, 36, 15), 'users.updated_at': datetime.datetime(2022, 3, 8, 9, 36, 15)}]
        
        # HELPFUL FOR EXAM. YOU'RE GOING TO NEED TO JOIN A USER TO SOMETHING
        # create a user instance 
        u = User({
            "id": result[0]["users.id"],
            "first_name": result[0]["first_name"],
            "last_name": result[0]["last_name"],
            "email" : result[0]["email"],
            "password" : result[0]["password"],
            "created_at" : result[0]["users.created_at"],
            "updated_at" : result[0]["users.updated_at"],
        })
        # create a recipe instance, save the user into creator_id
        r = cls({
            "id" : result[0]["id"],
            "name" : result[0]["name"],
            "description" : result[0]["description"],
            "instructions" : result[0]["instructions"],
            "under_30" : result[0]["under_30"],
            "created_at" : result[0]["created_at"],
            "updated_at" : result[0]["updated_at"],
            "creator_id" : u
        })
        return r

    '''CREATE'''
    @classmethod
    def insert(cls, data):
        query="INSERT INTO recipes(name, description, instructions, under_30, creator_id) VALUES(%(name)s, %(description)s, %(instructions)s, %(under_thirty)s, %(creator_id)s)"
        return connectToMySQL(cls.db).query_db(query, data)
        # returns id number

    '''UPDATE'''
    @classmethod
    def update(cls,data):
        query="UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under_30=%(under_thirty)s, creator_id=%(creator_id)s WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query, data)


    '''DELETE'''
    @classmethod
    def delete(cls,data):
        query="DELETE FROM recipes WHERE id=%(id)s"
        return connectToMySQL(cls.db).query_db(query, data)