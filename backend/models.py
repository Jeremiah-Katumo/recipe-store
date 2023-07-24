from exts import db


# Recipe model 

"""
class Recipe:
    id:int primary key
    title:str
    description:str (text)
"""

class Recipe(db.Model):
    id            = db.Column(db.Integer(), primary_key=True, unique=True)
    title         = db.Column(db.String(), nullable=False)
    description   = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f"<Recipe {self.title} >"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, title, description):
        self.title = title
        self.description = description

        db.session.commit()

# User model
"""
class User:
    id:integer primary_key
    username:string
    email:string
    password:string
"""

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    username = db.Column(db.String(length=100), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.Text(length=30))

    def __repr__(self):
        return f"<User {self.username} >"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
