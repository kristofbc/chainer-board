from renderer import Renderer

from bokeh.client import push_session, pull_session
from bokeh.application.handlers import FunctionHandler, Handler
from bokeh.application import Application
from bokeh.server.server import Server
from bokeh.plotting import curdoc
from bokeh.layouts import column
from tornado.ioloop import IOLoop
from bokeh.document import without_document_lock
from tornado import gen
from functools import partial

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

    @gen.coroutine
    def _init_doc(self, doc):
        # The elements but be first initialized
        #if self._is_initialized:
        plots = []
        for i in xrange(len(self._elements)):
            doc, figure = self._elements[i].initialize(doc)
            plots.append(figure[0])

        doc.add_root(column(plots))

        if not self._is_initialized:
            @gen.coroutine
            def cb():
                def next_tick():
                    try:
                        doc.remove_timeout_callback(cb)
                    except:
                        pass
                    self._modify_doc(doc)
                    doc.add_timeout_callback(cb, self._refresh_delay)
                doc.add_next_tick_callback(next_tick)
            doc.add_timeout_callback(cb, self._refresh_delay)
            #self._is_initialized = True

    @gen.coroutine
    def _modify_doc(self, doc):
        """
            When bookeh server trigger a rendering

            Args:
                doc (bookeh): current document
        """
        # When the elements are initialized, update them
        try:
            #def update(doc):
            #    #if not self._is_initialized:
            #    #    def cb():
            #    #        print(doc.session_context._document)
            #    #        self._modify_doc(doc)
            #    #    doc.add_periodic_callback(cb, self._refresh_delay)
            #    #    self._is_initialized = True

            #    self._update_cb()
            #    for i in xrange(len(self._elements)):
            #        if self._elements[i].requires_update():
            #            self._elements[i].render(doc)
            #doc.session_context.with_locked_document(update)
            
            self._update_cb()
            for i in xrange(len(self._elements)):
                if self._elements[i].requires_update():
                    self._elements[i].render(doc)
        except:
            print("@TODO: fix trying to write at the same time")
            pass

    def start(self, update_cb):
        """
            Start the rendering of the Board

            Args:
                update_cb (function(lib_inst)): called when the Rendering is refreshing
        """
        self._update_cb = update_cb

        self._io_loop = IOLoop.current()
        #self._application = Application(CustomHandler(self, self._init_doc), FunctionHandler(self._modify_doc))
        self._application = Application(CustomHandler(self, self._init_doc))
        self._server = Server({'/' + self._name: self._application}, io_loop=self._io_loop, check_unused_sessions_milliseconds=1000, unused_session_lifetime_milliseconds=1000)

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


class CustomHandler(Handler):
    def __init__(self, renderer, session_created_cb):
        super(CustomHandler, self).__init__()
        self._renderer = renderer
        self._session_created_cb = session_created_cb

    def on_session_created(self, session_context):
        # Use the same session, for everyone
        sessions = self._renderer._server.get_sessions('/' + self._renderer._name)
        #if len(sessions) == 0:

            #push_session(session_context._document, session_context.id, url='http://' + self._renderer._url + ':' + str(self._renderer._port) + '/' + self._renderer._name, app_path='/' + self._renderer._name)

        #    push_session(sessions[0].document)
            #session_context._set_session(sessions[0])
        #session_context._set_session(pull_session(session_id=self._app_name, url=self._url))
        #session_context.with_locked_document(self._session_created_cb)
        self._session_created_cb(session_context._document)

