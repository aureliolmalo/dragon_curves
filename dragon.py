import math
import argparse
import turtle as t

def get_next_line(sys_string:str) -> str:
    l_sys_iter = iter(sys_string)
    new_sys = ''
    for symbol in l_sys_iter:
        if symbol == 'F':
            new_symbol = 'F+G'
        elif symbol == 'G':
            new_symbol = 'F-G'
        else:
            new_symbol = symbol
        new_sys += new_symbol
    return new_sys

def get_system(n_steps:int) -> str:
    return_sys = 'F'
    for step in range(n_steps):
        return_sys = get_next_line(return_sys)
    return return_sys

def draw_curve(turt: t.Turtle, n_steps:int, size:int=5, angle=90) -> None:
    angle = angle
    system = get_system(n_steps)
    for cmd in system:
        if cmd in ('F', 'G'):
            turt.forward(size)
        elif cmd == '+':
            turt.left(angle)
        elif cmd == '-':
            turt.right(angle)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('n_steps', type=int, default=5)
    parser.add_argument('size', type=int, default=5)
    parser.add_argument('angle', type=int, default=90)
    #parser.add_argument('kwargs', type=dict, default={})
    return parser

def build_turtle(color='blue') -> t.Turtle:
    turt = t.Turtle()
    # turt.penup()
    # turt.setx(500)
    # turt.sety(250)
    # turt.pendown()
    turt.color(color)
    turt.speed('fastest')
    return turt

def main():
    parser = build_parser()
    args = parser.parse_args()
    turt = build_turtle()
    draw_curve(turt, args.n_steps, args.size, args.angle)
    t.mainloop()

if __name__ == '__main__':
    main()
    