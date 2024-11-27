import Users.userdb as userdb
class users:
    user_password = None
    user_name = None

    def __init__(self):
        return None
    
    def setProperties(self, user_name, user_password):
        self.user_name = user_name
        self.user_password = user_password
    
    def create_user(self):
        udb = userdb.userDB()
        udb.insert_user(self.user_name, self.user_password)
    
    def login(self,user_name,user_password):
        udb = userdb.userDB()
        return udb.user_login(user_name,user_password)

    def Get(self, username):
        udb = userdb.userDB()
        return udb.get(username)