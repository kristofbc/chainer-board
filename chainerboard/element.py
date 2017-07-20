
class Element(object):
    """
        An Element contain the previous data, next data to be rendered,
        but also the callback for the creation and rendering of the Element
    """
    def __init__(self, name, init_cb, render_cb, previous_data=None):
        """
            Args:
                name (string): name of the Element
                init_cb(lib_inst, previous_data):lib_inst: called once, when initializing the Element
                render_cb(lib_inst, figure_instance, previous_data, next_data):lib_inst: called everytime when new data must be rendered
                previous_data (mixed): initial data of this element
        """
        self._name = name
        self._init_cb = init_cb
        self._render_cb = render_cb
        self._previous_data = previous_data
        self._next_data = None
        self._figure_instance = None

    def update(self, data):
        """
            Update the data of the Element
            To visualize the change, render() must be called
            
            Args:
                data (mixed): data needed to render the element
        """
        self._next_data = data

    def initialize(self, lib_inst):
        """
            Initialize this element using the rendering library instance

            Args:
                lib_inst: the rendering library instance
            Returns:
                (lib_instance, figure_instance)
        """
        self._figure_instance = self._init_cb(lib_inst, self._previous_data)
        return lib_inst, self._figure_instance
        
    def render(self, lib_inst):
        """
            Render this element using the library instance used to draw the figure
            
            Args:
                lib_inst: the instance of the library
            Returns:
                (lib_inst, figure_instance)
        """
        self._figure_instance = self._render_cb(lib_inst, self._figure_instance, self._previous_data, self._next_data)
        self._previous_data = self._next_data
        self._next_data = None

        return lib_inst, self._figure_instance
    
    def requires_update(self):
        """
            Check if the Element requires update

            Returns:
                (bool)
        """
        return self._next_data is not None

    def get_name(self):
        return self._name



