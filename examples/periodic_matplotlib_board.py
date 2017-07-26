import numpy as np

from chainerboard.periodic_board import PeriodicBoard
from chainerboard.element import Element
from chainerboard.matplotlib_renderer import MatplotlibRenderer

def main():
    N_STEP = [1] # int cannot be passed by ref, object yes
    t = np.arange(0.0, 2.0, 0.01)
    s1 = np.sin(2*np.pi*t)
    s2 = np.sin(4*np.pi*t)

    """ Define the Element(s) used in the Renderer """
    # Here, 2 elements are defined and create a sigmoid plot
    # These functions are made to be used with bookeh
    def sigmoid_initializer(**kwargs):
        def init_cb(lib_inst, data):
            fig = lib_inst.figure()
            ax = fig.add_subplot(111)
            line, = ax.plot(data[0], data[1], **kwargs)

            return (fig, ax, line)
        return init_cb

    def sigmoid_updater(steps):
        def update_cb(lib_inst, figure_instance, previous_data, next_data):
            fig, ax, line = figure_instance

            # Don't clear the whole graph for efficiency
            x = line.get_xdata() + next_data[0]
            y = line.get_ydata() + next_data[1]

            line.set_xdata(x)
            line.set_ydata(y)

            fig.canvas.draw()
            return (fig, ax, line)
        return update_cb

    elements = [
        Element("plot1", sigmoid_initializer(color="red"), sigmoid_updater(N_STEP), [t, s1]), # This one will not change
        Element("plot2", sigmoid_initializer(color="blue"), sigmoid_updater(N_STEP), [t, s2])
    ]

    """ Define the Renderer """
    renderer = MatplotlibRenderer(elements)

    """ Define the Board """
    def board_updater(steps):
        # Simulate an update
        def updater(board):
            plot1 = board.get_renderer().get_element("plot1")
            plot2 = board.get_renderer().get_element("plot2")
            
            plot1.update([t*steps[0], s1*steps[0]])
            plot2.update([t*steps[0], s2*steps[0]])

            steps[0] +=1
        return updater

    board = PeriodicBoard(renderer, board_updater(N_STEP))

    """ Start the Board """
    board.run()

if __name__ == '__main__':
    main()
