class community:
    description = None
    name = None
    Admin = None

    def __init__(self, description, name, admin):
        print("i got here too")
        self.description = description
        self.name = name
        self.admin = admin

    
    def Create(self):
        print("i am creating")
        print(self.description)
        print(self.name)
        print(self.admin)
        #if this community with the same name exists
        #save the community to the daabase
        return self
    
    def Delete(self):
        #if the community with the name exists
        #if the admin actually owns the community
        #remove the community and all its dependent entities from the database
        return community
    
    def Update(self):
        #if the community with the name exists
        #if the admin actually owns the community
        #only description of the community can be updated
        return community
    
    def join(self):
        #if the community names exists
        #
        return community
    
    def Exit(self):
        return community
    
    def CreatePost(self):
        return community
    
    def ListAll(self):
        return []