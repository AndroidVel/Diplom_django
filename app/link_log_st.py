# Current user on site
class LoggedStatus:
    def __init__(self):
        self.is_logged_in = False
        self.email = ''

    def log_in(self, email):
        self.is_logged_in = True
        self.email = email

    def log_out(self):
        self.is_logged_in = False
        self.email = ''


log_st = LoggedStatus()


# Status of links on navigation bar
class LinkStatus:
    def __init__(self):
        self.home = ''
        self.products = ''
        self.about = ''
        self.log_in = ''
        self.sign_up = ''
        self.profile_info = ''
        self.cart = ''
        self.log_out = ''


link_st = LinkStatus()
