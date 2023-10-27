#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""password manager"""

__version__: str = "1.0.0"


def main() -> int:
    """entry / main function"""

    print("pwdmgr")

    return 0


if __name__ == "__main__":
    assert main.__annotations__.get("return") is int, "main() should return an integer"
    raise SystemExit(main())
