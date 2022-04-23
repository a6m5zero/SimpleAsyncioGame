import time
import curses
import random
import asyncio
from curses_tools import draw_frame, read_controls

""""""""""""
begin_x = 2;
begin_y = 1
height = 15;
width = 50
""""""""""""



frame1 = '''
  |
 .".
 |O|
<'O'>
|< >|
|-O-|
-(|)-
  )  
-(|)- 
'''

frame2 = """
  |
 .".
 |O|
<'O'>
|< >|
|-O-|
  ( 
-(|)- 
  ) 
"""


async def refresh_canvas(canvas):
    while True:
        canvas.refresh()
        curses.curs_set(False)
        await asyncio.sleep(0)


async def keyboard_loop(canvas):
    while True:
        char = canvas.getch()
        await asyncio.sleep(0)
        if char == ord('q'):
            exit(0)

        rows_direction = columns_direction = 0
        space_pressed = False
        if char == ord('w'):
            rows_direction = -1

        if char == ord('s'):
            rows_direction = 1

        if char == ord('a'):
            columns_direction = -1

        if char == ord('d'):
             columns_direction = 1

        return rows_direction, columns_direction, space_pressed


async def blink(canvas, row, column, symbol='*'):
    while True:
        # canvas.refresh()
        if canvas.inch(row,column) not in (ord(' '), ord(symbol)):
            return
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(random.uniform(0.1, 1))

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(random.uniform(0.1, 1))

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(random.uniform(0.1, 1))

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(random.uniform(0.1, 1))


async def draw_spaceship(canvas, row, coloumn):
    while True:
        rows_direction, columns_direction, space_pressed = await keyboard_loop(canvas)
        row += rows_direction
        coloumn += columns_direction
        draw_frame(canvas, row, coloumn, frame1, negative=False)
        await asyncio.sleep(0.1)
        draw_frame(canvas, row, coloumn, frame1, negative=True)
        await asyncio.sleep(0)
        rows_direction, columns_direction, space_pressed = await keyboard_loop(canvas)
        row += rows_direction
        coloumn += columns_direction
        draw_frame(canvas, row, coloumn, frame2, negative=False)
        await asyncio.sleep(0.1)
        draw_frame(canvas, row, coloumn, frame2, negative=True)


async def draw(_):

    curses.curs_set(0)
    canvas = curses.newwin(height, width, begin_y, begin_x)
    canvas.border()
    canvas.refresh()
    canvas.nodelay(True)

    await asyncio.gather(
                         refresh_canvas(canvas),
                         draw_spaceship(canvas,3,24),
                         *(blink(canvas, random.randrange(1, 14),
                                 random.randrange(1, 49),
                                 symbol=random.choice([':', '|', '*', '+'])) for _ in range(60)))
    time.sleep(5)


if __name__ == '__main__':
    curses.update_lines_cols()
    asyncio.run(curses.wrapper(draw))
