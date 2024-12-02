import Communities.communityDB as commdb    
class community:
    description = None
    name = None
    Admin = None

    def __init__(self):
        return None
    
    def SetProperties(self, description, name, admin):
        self.description = description
        self.name = name
        self.admin = admin

    
    def Create(self):
        cdb = commdb.communityDB()
        cdb.insert(self.description, self.name, self.admin)
        return self
    
    def Delete(self, name):
        cdb = commdb.communityDB()
        cdb.removeMembers(name)
        cdb.remove(name)
    
    def Update(self,name, newDesc):
        cdb = commdb.communityDB()
        cdb.update(name, newDesc)

    def Get(self, name):
        cdb = commdb.communityDB()
        return cdb.get(name)

    
    def join(self, name, username):
        cdb = commdb.communityDB()
        cdb.addMember(name,username)
    
    def Exit(self,name,username):
        cdb = commdb.communityDB()
        cdb.removeMember(name,username)
    
    def ListAll(self, username):
        cdb = commdb.communityDB()
        listOfAll = cdb.retrieve(username)
        return listOfAll
    
    def listOne(self, admin):
        cdb = commdb.communityDB()
        listOfOne = cdb.userRetrieve(admin)
        return listOfOne
    
    def listComm(self,name):
        cdb = commdb.communityDB()
        commName = cdb.getCommunityName(name)
        return commName
    
    def adminSeek(self,username):
        cdb = commdb.communityDB()
        adminName = cdb.adminRetrieve(username)
        return adminName
    
