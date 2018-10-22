"""
LAMMPS (sci-physics/lammps) project within gentoo chroot.
"""
from plumbum import local

from benchbuild.projects.gentoo.gentoo import GentooGroup
from benchbuild.utils import downloader, wrapping
from benchbuild.utils.cmd import tar


class Lammps(GentooGroup):
    """
        sci-physics/lammps
    """
    NAME = "lammps"
    DOMAIN = "sci-physics"

    test_url = "http://lairosiel.de/dist/"
    test_archive = "lammps.tar.gz"

    def compile(self):
        self.emerge_env = dict(USE="-mpi -doc")

        super(Lammps, self).compile()

        test_archive = self.test_archive
        test_url = self.test_url + test_archive
        downloader.Wget(test_url, test_archive)
        tar("fxz", test_archive)

    def run_tests(self, runner):
        builddir = self.builddir
        lammps = wrapping.wrap(local.path('/usr/bin/lmp'), self)
        lammps_dir = builddir / "lammps"

        with local.cwd(lammps_dir):
            tests = lammps_dir // "in.*"
            for test in tests:
                runner((lammps < wrapping.strip_path_prefix(test, builddir)))
