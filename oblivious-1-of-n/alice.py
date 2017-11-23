#!/usr/bin/env python3

from oblivious import step_0 as gen_xs
from oblivious import step_2 as gen_msgs
from utils import jencode, jdecode


if __name__ == "__main__":
    # Read {g, pk}
    a = jdecode(input("sk: "))
    a.update(jdecode(input("m: ")))

    print(jencode(gen_xs(a)))

    a.update(jdecode(input("v: ")))

    print(jencode(gen_msgs(a)))
