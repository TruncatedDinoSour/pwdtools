#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""password info"""


def main() -> int:
    """entry / main function"""

    print("pwdinfo")

    return 0


if __name__ == "__main__":
    assert main.__annotations__.get("return") is int, "main() should return an integer"
    raise SystemExit(main())
