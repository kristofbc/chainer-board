from renderer import Renderer

import matplotlib.pyplot as plt

class MatplotlibRenderer(Renderer):
    """
        Render Element(s) using the matplotlib library
        This Renderer can only be used in an graphical interface
    """
    def __init__(self, elements=[]):
        """
            Args:
                elements (Element[]): an array of Element(s) to render
        """
        self._elements = elements
        self._is_initialized = False
        self._update_cb = None

    def start(self, update_cb):
        """
            Start the rendering of the Board

            Args:
                update_cb (function(lib_inst)): called when the Rendering is refreshing
        """
        if not self._is_initialized:
            for i in xrange(len(self._elements)):
                self._elements[i].initialize(plt)
            self._is_initialized = True
            #plt.show()
            plt.draw()
            plt.pause(0.01)
            return

        update_cb()
        for i in xrange(len(self._elements)):
            if self._elements[i].requires_update():
                self._elements[i].render(plt)
            plt.draw()
            plt.pause(0.01)

    def stop(self):
        """
            Stop the rendering of the Board
        """
        raise NotImplementedError("stop must be implemented")

    def add_element(self, element):
        """
            Add a new element to render

            Args:
                element (Element): the element to add
        """
        self._elements.append(element)

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
            del self._elements[i]


