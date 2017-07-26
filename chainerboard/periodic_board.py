import time

from board import Board

# @TODO: must be completed
class PeriodicBoard(Board):
    """
        The PeriodicBoard refresh the renderer every n ms
    """
    def __init__(self, renderer, update_cb=None, refresh_delay=1000):
        super(PeriodicBoard, self).__init__(renderer, update_cb)
        self._refresh_delay = refresh_delay
        self._running = False


    def run(self):
        """
            Execute the Board process every n ms
        """
        self._running = True
        while self._running:
            super(PeriodicBoard, self).run()
            time.sleep(self._refresh_delay/1000)

    def stop(self):
        """
            Stop the Board process
        """
        self._running = False
        super(PeriodicBoard, self).stop()
