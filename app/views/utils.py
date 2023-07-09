from lib.views import View


class ViewController:
    def __init__(self):
        self.current_view: View = None

    def change_view(self, new_view: View) -> None:
        if not self.current_view:
            new_view.show()
            self.current_view = new_view
        else:
            self.current_view.remove()
            new_view.show()
            self.current_view = new_view


view_controller = ViewController()
