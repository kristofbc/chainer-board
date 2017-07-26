# Chainer board
Inspired by Tensorboard, follow metrics in real-time while training a Neural Network

This package provide 2 ways of displaying data:
1. By using Matplotlib: can only work locally, periodically update your data
2. By using Bokeh: can be used on a webserver (data are available on a web page), periodically update your data

## Board
2 types of Board exists:
1. Board: default board without any functionnalities, controlled by the chosen Renderer
2. PeriodicBoard: update periodically (x ms) the board with new data

## Installation
```bash
$ pip install git+ssh://git@github.jp.honda-ri.com/Research/chainer-board.git
```

## Examples
2 examples are provided for Bokeh and Matplotlib in the `examples` folder
```bash
$ python example.py
```
To test different Renderer (Bokeh, Matplotlib ...) uncomment the specific lines in `example.py`
