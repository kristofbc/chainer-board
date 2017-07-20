from renderer import Renderer

from bokeh.client import push_session
from bokeh.application.handlers import FunctionHandler
from bokeh.application import Application
from bokeh.server.server import Server
from bokeh.plotting import curdoc
from bokeh.layouts import column
from tornado.ioloop import IOLoop

class BookehWebRenderer(Renderer):
    """
        Render Element(s) using the "bookeh" library
        This Renderer can only be used with a PeriodicBoard
    """
    def __init__(self, name, elements=[], url="localhost", port=5006, refresh_delay=1000):
        """
            Args:
                name (string): name of the bookeh instance
                elements (Element[]): an array of Element(s) to render
                url (string): url for the web server
                port (int): port for the web server
                refresh_delay (int): timer delay for updating the board
        """
        self._name = name
        self._url = url
        self._port = port
        self._elements = elements
        self._refresh_delay = refresh_delay
        self._update_cb = None
        self._is_initialized = None

        self._io_loop = None
        self._server = None
        self._application = None
        self._session = None

    def _modify_doc(self, doc):
        """
            When bookeh server trigger a rendering

            Args:
                doc (bookeh): current document
        """
        # The elements but be first initialized
        if not self._is_initialized:
            plots = []
            for i in xrange(len(self._elements)):
                doc, figure = self._elements[i].initialize(doc)
                plots.append(figure[0])

            doc.add_root(column(plots))
            self._is_initialized = True

            # Add the auto-refresh
            def cb():
                self._modify_doc(curdoc())
            doc.add_periodic_callback(cb, self._refresh_delay)
            return

        # When intialized run the update process
        self._update_cb()
        for i in xrange(len(self._elements)):
            if self._elements[i].requires_update():
                self._elements[i].render(doc)

    def start(self, update_cb):
        """
            Start the rendering of the Board

            Args:
                update_cb (function(lib_inst)): called when the Rendering is refreshing
        """
        self._update_cb = update_cb

        self._io_loop = IOLoop.current()
        self._application = Application(FunctionHandler(self._modify_doc))
        self._server = Server({'/' + self._name: self._application}, io_loop=self._io_loop)
        self._server.start()
        self._io_loop.start()

    def stop(self):
        """
            Stop the rendering of the Board
        """
        if self._server is not None:
            self._server.stop()

    def add_element(self, element):
        """
            Add a new element to render

            Args:
                element (Element): the element to add
        """
        self._elements.append(elements)

    def get_element(self, name):
        """
            Get Element by name

            Args:
                name (string): name of the element to get
            Returns:
                (Element)
        """
        for i in xrange(len(self._elements)):
            if self._elements[i].get_name() == name:
                return self._elements[i]

        return None

    def get_elements(self):
        """
            Get all the Elements

            Returns:
                (Element[])
        """
        return self._elements
    
    def remove_element(self, name):
        """
            Remove an Element from the rendering queue

            Args:
                name (string): Element name to remove
        """
        idx = None
        for i in xrange(len(self._elements)):
            if self._elements[i].get_name() == name:
                idx = i
                break
        if idx is not None:
            del self._elements[idx]
        # @TODO: Need to re-render the list



