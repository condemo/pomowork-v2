from lib.views import View

from views.auth.login import LoginView
from views.auth.signup import SignupView

views_list = {
    "login": LoginView,
    "signup": SignupView
}


class ViewController:
    def __init__(self):
        self.current_view: View = None

    def change_view(self, view: str, master) -> None:
        if not self.current_view:
            new_view = views_list[view](master, self)
            new_view.show()
            self.current_view = new_view
        else:
            self.current_view.remove()
            new_view = views_list[view](master, self)
            new_view.show()
            self.current_view = new_view


view_controller = ViewController()
