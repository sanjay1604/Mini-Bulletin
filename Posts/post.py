import Communities.community
class post:
    post_title = None
    post_message = None
    post_id = None
    posting_user = None
    community_id = None

    def __init__(self, post_title, post_message, post_id, posting_user, community_id):
        self.post_title = post_title
        self.post_message = post_message
        self.post_id = post_id
        self.posting_user = posting_user
        self.community_id = community_id


    def delete(self):
        return post
    
    def update(self):
        return post
    
    def react(self):
        return post
    
    def comment(self):
        return post
    