from element import Element

class Renderer(object):
    """
        Display the Elements using this Renderer
    """
    def start(self, update_cb):
        """
            Start the rendering of the Board

            Args:
                update_cb (function(lib_inst)): called when the Rendering is refreshing
        """
        raise NotImplementedError("start must be implemented")

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
        raise NotImplementedError("add_element must be implemented")

    def get_element(self, name):
        """
            Get Element by name

            Args:
                name (string): name of the element to get
            Returns:
                (Element)
        """
        raise NotImplementedError("get_element must be implemented")

    def get_elements(self):
        """
            Get all the Elements

            Returns:
                (Element[])
        """
        raise NotImplementedError("get_elements must be implemented")
    
    def remove_element(self, name):
        """
            Remove an Element from the rendering queue

            Args:
                name (string): Element name to remove
        """
        raise NotImplementedError("remove_element must be implemented")
