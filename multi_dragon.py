import dragon

import turtle as t
import argparse
import math

import numpy as np

def prep_turtle_for_next_dragon(turt:t.Turtle, new_color='red') -> t.Turtle:
    turt.penup()
    turt.setx(0)
    turt.sety(0)
    turt.settiltangle(0)

    # rad_angle = math.sqrt(2)
    # deg_angle = math.degrees(rad_angle)
    deg_angle = 180
    turt.right(deg_angle)
    turt.color(new_color)
    turt.pendown()
    return turt

def build_parser() -> argparse.ArgumentParser:
    parser = dragon.build_parser()
    parser.add_argument('n_dragons', type=int, default=2)
    return parser      

def get_new_color(n_dragons:int) -> tuple:
    # rgb_array = np.random.randint(0, 255, (3, ))
    # rgb_tuple = tuple(rgb_array)
    base_triple = np.random.randint(0, 256, (3, ))
    for col in np.linspace(0.4, 1.0, num=n_dragons):
        rgb_array = (base_triple * col).astype(np.int64)
        rgb_tuple = tuple(rgb_array)
        yield rgb_tuple

    

def main():
    t.colormode(255)
    parser = build_parser()
    args = parser.parse_args()

    colors = get_new_color(n_dragons=args.n_dragons)
    color = next(colors)
    
    turt = dragon.build_turtle(color=color)
    
    dragon.draw_curve(turt=turt, n_steps=args.n_steps, size=args.size)
    
    for d in range(args.n_dragons-1):
        rgb_color = next(colors)
        turt = prep_turtle_for_next_dragon(turt=turt, new_color=rgb_color)
        dragon.draw_curve(turt=turt, n_steps=args.n_steps, size=args.size)
        
    
    t.mainloop()

if __name__ == '__main__':
    main()
