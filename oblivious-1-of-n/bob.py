#!/usr/bin/env python3

from oblivious import step_1 as choose
from oblivious import step_3 as get_msg
from utils import jencode, jdecode


if __name__ == "__main__":
    # Read {g, pk}
    a = jdecode(input("pk: "))
    b = int(input("b: "))
    a.update({"b": b})

    a.update(jdecode(input("x: ")))

    print(jencode(choose(a)))

    a.update(jdecode(input("m': ")))

    print(jencode(get_msg(a)))
