import Comments.comments
class CommentReaction:
    reacting_user = None
    reacting_id = None
    comment_id = None

    def __init__(self, reacting_user, reacting_id, comment_id):
        self.reacting_id = reacting_id
        self.reacting_user = reacting_user
        self.comment_id = comment_id

    def upvote(self):
        return CommentReaction
    
    def downvote(self):
        return CommentReaction
    
    def remove_reaction(self):
        return CommentReaction

    








