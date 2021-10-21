#!usr/bin/python

"""
Misc Experiments:
+ graphing techniques
+ Maths Equations
"""
# PYLINT: ENTIRE SCOPE
# pylint: disable=missing-function-docstring
# pylint: disable=use-list-literal

# IMPORTS
# Order: Std, 3rdParty, CustomLocal
import matplotlib.pyplot as plt
import numpy as np

DEF_ENCODING = 'utf-8'

def plot_2d_cartesian(
        x_list, y_list, title=None, xlabel=None, ylabel=None,
        figwidth=10, figheight=4, out_path=None, only_show=True
    ):
    fig = plt.figure()
    fig.set_figwidth(figwidth)
    fig.set_figheight(figheight)
    plt.title(title if title else '')
    plt.xlabel(xlabel if xlabel else '')
    plt.ylabel(ylabel if ylabel else '')
    plt.plot(x_list, y_list)
    if out_path and not only_show:
        plt.savefig(out_path)
    else:
        plt.show()
    # plt.savefig(out_path) if (out_path and not only_show) else plt.show()

def plot_2d_cartesian_multiple(
        x_list, y_arrays, y_labels=None, title=None, xlabel=None, ylabel=None,
        figwidth=10, figheight=4, out_path=None, only_show=True
    ):
    fig = plt.figure()
    fig.set_figwidth(figwidth)
    fig.set_figheight(figheight)
    plt.title(title if title else '')
    plt.xlabel(xlabel if xlabel else '')
    plt.ylabel(ylabel if ylabel else '')
    y_colours = { 0: 'red', 1: 'green', 2: 'blue', 3: 'orange', 4: 'purple'}
    for index, y_list in enumerate(y_arrays):
        p_colour = y_colours.get(index) if index < len(y_arrays) else y_colours.get(0)
        y_label = str(y_labels[index]) if (y_labels and index < len(y_arrays)) else 'default'
        plt.plot(x_list, y_list, color=p_colour, label=y_label)
    plt.legend()
    if out_path and not only_show:
        plt.savefig(out_path)
    else:
        plt.show()

def main():
    """ Misc Experiments, testing modules """

    # Graph a FootBall FreeKick: As a Quadratic Equation:
    # y = d(-a(x + b)^2 + c)
    # where a < 1.0, b ~= 10m, c ~=3m, d ~=1/40

    # xData
    length_to_goal = 30
    x_list = list(np.arange(0, length_to_goal+1, 1))
    print(f'DEBUG: x_list: array: {x_list}')

    # yInfo
    # pylint: disable=unused-variable
    # pylint: disable=invalid-name
    a_possibles = [0.3, 0.4, 0.5, 0.6, 0.7]
    b_possibles = [-24, -22, -20, -18, -16]
    c_possibles = [135, 140, 142, 145, 150]
    d_possibles = [0.020, 0.021, 0.022, 0.023, 0.024] # wall: 2.0 - 2.5m, goal: 1.8 - 2.0m
    a = 0.36
    b = -20.0
    c = 142
    d = 0.020
    dpi = 3

    # Experiment with ranges, identify most realistic/True
    y_arrays = list()
    y_variables = ['c', c_possibles]
    print(f'DEBUG: default variables: a: {a}, b: {b}, c: {c}, d: {d}')
    for c in y_variables[1]:
        y_list = [round((d * (-a * (x_val + b)**2 + c)), dpi) for x_val in x_list]
        print(f'DEBUG: c: {c} y_list: array: {y_list}')
        y_arrays.append(y_list)

    # Plot: Cartesian, Line: Multiple
    heading = 'Experiment: A FootBall FreeKick as a MATHS Equation: y = d(-a(x+b)^2+c): var=c'
    x_desc = 'Length on FootBallPitch, metres'
    y_desc = 'Height off Ground, metres'
    graph_fpath = './data/football_freekick.png'
    fwidth = 10
    fheight = 4
    plot_2d_cartesian_multiple(
        x_list, y_arrays, y_labels=y_variables[1], title=heading, xlabel=x_desc, ylabel=y_desc,
        figwidth=fwidth, figheight=fheight, out_path=graph_fpath,
        only_show=False
    )

    # Plot: Cartesian, Line: Med(ian)
    heading = 'Experiment: A FootBall FreeKick as a MATHS Equation: y = d(-a(x+b)^2+c): med'
    graph_fpath = './data/football_freekick_med.png'
    med = int((len(y_arrays) - 1) / 2)
    plot_2d_cartesian(
        x_list, y_arrays[med], title=heading, xlabel=x_desc, ylabel=y_desc,
        figwidth=fwidth, figheight=fheight, out_path=graph_fpath,
        only_show=False
    )

if __name__ == '__main__':
    main()
