from renderer import Renderer

class Board(object):
    """
        The board is a simple interface used to display a Renderer instance
    """
    def __init__(self, renderer, update_cb=None):
        """
            Args:
                renderer: the Renderer instance
                update_cb (function(board):Element[]): when the board is rendering call this function
        """
        if not isinstance(renderer, Renderer):
            raise ValueError("renderer should be instance of Renderer")

        self._renderer = renderer
        self._update_cb = update_cb

    def run(self):
        """
            Execute the Board process
        """
        def noop(board):
            ell = board.get_renderer()
            return ell

        def update():
            if self._update_cb is None:
                self.noop(self)
            else:
                self._update_cb(self)

        self._renderer.start(update)

    def get_renderer(self):
        return self._renderer

