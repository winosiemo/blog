from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
@login_manager.user_loader
def load_user(user_id):
        return User.query.get (user_id)
class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    upvotes = db.relationship('Upvote',backref = 'user',lazy = "dynamic")
    pitches= db.relationship('Pitch',backref = 'user',lazy = "dynamic")
    downvotes= db.relationship('Downvote',backref = 'user',lazy = "dynamic")
   
    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)
    def __repr__(self):
        return f'User {self.username}'

class blog(db.Model):

    __tablename__ ='pitches'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String)
    description=db.Column(db.Text)
    category=db.Column(db.String(255),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id")) 
    updates = db.relationship('Update',backref = 'blog',lazy = "dynamic")
    
    def save_blog(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_bloges(cls,id):
        bloges = Bloges.query.filter_by(blog_id=id).all()
        return bloges
    def __repr__(self):
        return f'blog {self.description}'

class Comment(db.Model):
    __tablename__='comments'
    
    id = db.Column(db.Integer,primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('bloges.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"Comment : id: {self.id} comment: {self.description}"

class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer,primary_key = True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))