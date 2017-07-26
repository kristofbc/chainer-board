import numpy as np

from chainerboard.board import Board
from chainerboard.element import Element
from chainerboard.bookeh_renderer import BookehWebRenderer

from bokeh.plotting import figure

def main():
    N_STEP = [1] # int cannot be passed by ref, object yes
    x = np.linspace(0, 4*np.pi, 80)
    y = np.sin(x)

    """ Define the Element(s) used in the Renderer """
    # Here, 2 elements are defined and create a sigmoid plot
    # These functions are made to be used with bookeh
    def sigmoid_initializer(**kwargs):
        def init_cb(lib_inst, data):
            p = figure()
            r = p.line(data[0], data[1], **kwargs) 

            return [p, r]
        return init_cb

    def sigmoid_updater(steps):
        def update_cb(lib_inst, figure_instance, previous_data, next_data):
            print("update")
            figure_instance[1].data_source.data["y"] = next_data[1]
            figure_instance[1].glyph.line_alpha = 1 - 0.8 * abs(steps[0])

            return figure_instance
        return update_cb

    elements = [
        Element("plot1", sigmoid_initializer(color="firebrick"), sigmoid_updater(N_STEP), [[0, 4*np.pi], [-1, 1]]), # This one will not change
        Element("plot2", sigmoid_initializer(color="navy"), sigmoid_updater(N_STEP), [x, y])
    ]

    """ Define the Renderer """
    url = "localhost"
    port = 5006
    refresh_delay = 1000
    renderer = BookehWebRenderer("periodic_bokeh_board", elements, url, port, refresh_delay)

    """ Define the Board """
    def board_updater(steps):
        # Simulate an update
        # Update only the second plot
        def updater(board):
            ell = board.get_renderer().get_element("plot2")
            ell.update([x, y*steps[0]])

            steps[0] +=1
        return updater

    board = Board(renderer, board_updater(N_STEP))

    """ Start the Board """
    board.run()

if __name__ == '__main__':
    main()
