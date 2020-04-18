#!/usr/bin/env python
# -*- coding: utf-8 -*-

from golsat import Life

def test_glider():
    life = Life(9, 9)
    board = life.step_time(5)
    board.from_array([
        # [False, True, False] + [False] * 7,
        # [False, False, True] + [False] * 7,
        # [True, True, True] + [False] * 7,
        [False] * 9,
        [False] * 9,
        [False] * 9,
        [False]*3 + [False, True, False] + [False]*3,
        [False]*3 + [False, False, True] + [False]*3,
        [False]*3 + [True, True, True] + [False]*3,
        [False] * 9,
        [False] * 9,
        [False] * 9,
        #[False]*7 + [False, True, False],
        #[False]*7 + [False, False, True],
        #[False]*7 + [True, True, True],
    ])

    value = 5
    for board in life.boards[::-1]:
        constraint = board.as_vec().bit_sum() <= value
        life.model.add_assert(constraint)
        value += 2

    if life.solve():
        for next_board in life.boards:
            print(str(next_board))
