import dragon

import turtle as t
import argparse
import math

import numpy as np

def prep_turtle_for_next_dragon(turt:t.Turtle, new_color='red') -> t.Turtle:
    turt.penup()
    turt.setx(0)
    turt.sety(0)

    rad_angle = math.sqrt(2)
    deg_angle = math.degrees(rad_angle)
    turt.right(deg_angle)
    turt.color(new_color)
    turt.pendown()
    return turt

def build_parser() -> argparse.ArgumentParser:
    parser = dragon.build_parser()
    parser.add_argument('n_dragons', type=int, default=2)
    return parser    

def get_new_color() -> tuple:
    rgb_array = np.random.randint(0, 250, (3, ))
    rgb_tuple = tuple(rgb_array)
    return rgb_tuple

def main():
    parser = build_parser()
    args = parser.parse_args()
    turt = dragon.build_turtle()
    for d in range(args.n_dragons):
        dragon.draw_curve(turt=turt, n_steps=args.n_steps, size=args.size)
        rgb_color = get_new_color()
        turt = prep_turtle_for_next_dragon(turt=turt, new_color=rgb_color)



if __name__ == '__main__':
    main()
