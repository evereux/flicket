from flicket_application.flicket_models import FlicketTicket, FlicketPost

class FlicketUserDetails():
    """
    class returns various details about user from user object input.
    """

    def __init__(self, user_obj):
        self.user = user_obj
        self.id = user_obj.id

    @property
    def num_assigned(self):
        """ return number of tickers assigned to user """
        return FlicketTicket.query.filter_by(assigned=self.user).count()

    @property
    def num_posts(self):
        """ return number of post made by user """

        return FlicketTicket.query.filter_by(started_id = self.id).count() + FlicketPost.query.filter_by(user_id=self.id).count()
