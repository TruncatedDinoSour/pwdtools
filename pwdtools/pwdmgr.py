#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""password manager"""

from __future__ import annotations

import multiprocessing as mp
import sys
from abc import ABC
from dataclasses import dataclass
from typing import List

import armour.pdb

from . import pwdgen, pwdinfo, pwdzxc

__version__: str = "1.0.0"


def log(msg: str) -> None:
    """log a message"""

    print(f" * {msg}", file=sys.stderr)


class Cmds(ABC):
    """function eq to 'external' cmds"""

    def cmd_help(self) -> int:
        """print help"""

        for cmd in dir(self):
            if cmd[:4] == "cmd_":
                log(f"{cmd[4:]} -- {getattr(self, cmd).__doc__ or 'no help provided'}")

        return 0

    def cmd_gen(self, *argv: str) -> int:
        """runs `pwdgen`"""

        p: mp.Process = mp.Process(
            target=lambda: pwdgen.main(
                pwdgen.OPTIONS.parse_args(list(argv))[0].__dict__,
            ),
        )
        p.start()
        p.join()

        return p.exitcode or 0

    def cmd_info(self) -> int:
        """runs `pwdinfo`"""

        p: mp.Process = mp.Process(target=pwdinfo.main)
        p.start()
        p.join()

        return p.exitcode or 0

    def cmd_zxc(self) -> int:
        """runs `pwdzxc`"""

        p: mp.Process = mp.Process(target=pwdzxc.main)
        p.start()
        p.join()

        return p.exitcode or 0


@dataclass
class HomeCmds(Cmds):
    """home mode commands"""


def main() -> int:
    """entry / main function"""

    print(f"welcome to pwdmgr v{__version__} for pDB {armour.pdb.header.VERSION}\n")

    try:
        import readline

        readline.read_init_file()
    except ImportError:
        pass

    ex: int = 0

    cmds: HomeCmds = HomeCmds()

    while True:
        try:
            cmd: str = input(f"[{ex}]> ")
        except EOFError:
            print()
            return ex
        except KeyboardInterrupt:
            print("\n")
            continue

        if not (cmd := cmd.strip()):
            print()
            continue

        argv: List[str] = cmd.split()

        if (cmd_fn := getattr(cmds, f"cmd_{argv[0]}", None)) is None:
            log(f"unkown command {argv[0]!r}\n")
            continue

        try:
            ex = cmd_fn(*argv[1:])
        except Exception as e:
            log(f"error : {e}")
        finally:
            print()


if __name__ == "__main__":
    raise SystemExit(main())
