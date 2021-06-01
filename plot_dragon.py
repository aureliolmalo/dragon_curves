import os
import sys

import argparse
import cmath
import math
from uuid import uuid4
import logging as lg

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt

from dragon import get_system

def set_up_main_logger(level:int):
    logger = lg.getLogger('main')
    handler = lg.FileHandler('plot_dragon.log', 'w')
    if logger.hasHandlers():
        logger.handlers.clear()
    
    fmt_str = '%(levelname)s @ %(funcName)s - line %(lineno)d | %(message)s'
    formatter = lg.Formatter(fmt=fmt_str)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.setLevel(level)
    logger.addHandler(handler)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('n_steps', type=int, default=5)
    parser.add_argument('angle', type=float, default=0.0)
    #parser.add_argument('size', type=int, default=5)
    #parser.add_argument('loglevel', type=int, default=0)
    parser.add_argument('color', type=str, default='blue')
    #parser.add_argument('angle', type=int, default=90)
    #parser.add_argument('kwargs', type=dict, default={})
    return parser

def init_ary(length:int) -> np.ndarray:
    ary = np.full(shape=(length +1, ), fill_value=np.nan, dtype=np.float64)
    return ary

def next_z(z:complex, sym_iter, angle:float, size:float) -> complex:
    logger = lg.getLogger('main')
    logger.debug(f'starting z-value: {z}')
    sym = ''
    r_step = math.cos(angle)
    i_step = math.sin(angle)
    
    logger.debug('starting find loop')
    while sym not in ('F', 'G'):
        sym = next(sym_iter)
        logger.debug(f'found symbol: {sym}')
        if sym == '+':
           r_step = math.cos(angle)
           i_step = math.sin(angle)
        elif sym == '-':
           r_step = math.cos((-1)*angle)
           i_step = math.sin((-1)*angle)
        angle += math.tau / 4
        logger.debug(f'changed angle value to {angle: .2f}')
        logger.debug(f'step in real direction: {r_step: .2f}')
        logger.debug(f'step in imaginary direction: {i_step: .2f}')

    next_z = complex(z.real + r_step * size, z.imag + i_step * size)
    if next_z.imag < 0:
        cpx_sign = '-'
    else:
        cpx_sign = '+'
    logger.debug(f'next z-value: {next_z.real :.2f}{cpx_sign}{abs(next_z.imag) :.2f}i')
    return next_z, angle

def get_coords(n_steps:int, size:float, angle:float):
    logger = lg.getLogger('main')
    system_string = get_system(n_steps)
    system_iter = iter(system_string)
    length = len(system_string)
    x, y = init_ary(length), init_ary(length)
    z = 0 + 0j
    x[0] = z.real
    y[0] = z.imag
    
    check_stop = False
    idx = 1
    
    while not check_stop:
        try:
            logger.info('finding next z value')
            z, angle = next_z(z=z, angle=angle, sym_iter=system_iter, size=size)
            #logger.info(f'found next z value {z} with angle {angle}')
        except StopIteration:
            check_stop = True
        x[idx] = z.real
        y[idx] = z.imag
        idx += 1
    x = pd.Series(x).dropna()
    y = pd.Series(y).dropna()
        
    return x, y

def make_plot(x, y, **kwargs):
    fig, ax = plt.subplots()
    ax.plot(x, y, **kwargs)
    return fig, ax

def get_name():
    id_string = uuid4().hex
    name = 'dragon_{ids}.png'.format(ids=id_string[:4])
    return name 

def main():
    parser = build_parser()
    args = parser.parse_args()
    set_up_main_logger(0)
    angle = math.radians(args.angle)
    x, y = get_coords(n_steps = args.n_steps, size=1, angle=angle)
    kwargs = {'c': args.color}
    fig, ax = make_plot(x, y, **kwargs)
    # lims = (-1, max(x.max(), y.max()) + 1)
    # ax.set_ylim(lims)
    # ax.set_xlim(lims)
    ax.axis('off')
    name = get_name()
    print(name)
    fig.savefig(dpi=1000, fname=name)
    pd.DataFrame(np.vstack((x, y)).transpose(), columns=['x', 'y']).to_csv(name.replace('png', 'csv'))

if __name__ == '__main__':
    main()