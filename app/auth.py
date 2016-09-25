class User():
    id = 
    nickname = 
    email = 
    posts = 

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)  # python 2

    def __repr__(self):
        return '<User %r>' % (self.nickname)