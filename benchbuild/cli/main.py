"""Main CLI unit of BenchBuild."""
import os
from plumbum import cli

from benchbuild import settings
from benchbuild.utils import log


class BenchBuild(cli.Application):
    """Frontend for running/building the benchbuild study framework."""

    VERSION = str(settings.CFG["version"])
    _list_env = False

    verbosity = cli.CountOf('-v', help="Enable verbose output")
    debug = cli.Flag('-d', help="Enable debugging output")

    def main(self, *args):
        self.verbosity = self.verbosity if self.verbosity < 6 else 5
        if self.debug:
            self.verbosity = 3
        verbosity = int(os.getenv('BB_VERBOSITY', self.verbosity))

        settings.CFG["verbosity"] = verbosity
        settings.CFG["debug"] = self.debug

        log.configure()
        log.set_defaults()

        if settings.CFG["db"]["create_functions"]:
            from benchbuild.utils.schema import init_functions, Session
            init_functions(Session())

        if args:
            print("Unknown command {0!r}".format(args[0]))
            return 1
        if not self.nested_command:
            self.help()
