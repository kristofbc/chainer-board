from board import Board

# @TODO: must be completed
class PeriodicBoard(Board):
    """
        The PeriodicBoard refresh the renderer every n ms
    """
    def __init__(self, renderer, update_cb=None):
        super(PeriodicBoard, self).__init__(renderer, update_cb)
