from plumbum import local

from benchbuild import project
from benchbuild.settings import CFG
from benchbuild.utils import compiler, download, run, wrapping
from benchbuild.utils.cmd import cp, make


@download.with_git(
    "git://git.videolan.org/x264.git", refspec="HEAD", limit=5)
class X264(project.Project):
    """ x264 """

    NAME = "x264"
    DOMAIN = "multimedia"
    GROUP = 'benchbuild'
    VERSION = 'HEAD'
    SRC_FILE = 'x264.git'

    inputfiles = {
        "tbbt-small.y4m": [],
        "Sintel.2010.720p.raw": ["--input-res", "1280x720"]
    }

    src_uri = "git://git.videolan.org/x264.git"

    def compile(self):
        self.download()
        testfiles = [local.path(self.testdir) / x for x in self.inputfiles]
        for testfile in testfiles:
            cp(testfile, self.builddir)

        clang = compiler.cc(self)

        with local.cwd(self.SRC_FILE):
            configure = local["./configure"]

            with local.env(CC=str(clang)):
                run.run(configure["--disable-thread", "--disable-opencl",
                                  "--enable-pic"])

            run.run(make["clean", "all", "-j", CFG["jobs"]])

    def run_tests(self, runner):
        x264 = wrapping.wrap(local.path(self.src_file) / "x264", self)

        tests = [
            "--crf 30 -b1 -m1 -r1 --me dia --no-cabac --direct temporal --ssim --no-weightb",
            "--crf 16 -b2 -m3 -r3 --me hex --no-8x8dct --direct spatial --no-dct-decimate -t0  --slice-max-mbs 50",
            "--crf 26 -b4 -m5 -r2 --me hex --cqm jvt --nr 100 --psnr --no-mixed-refs --b-adapt 2 --slice-max-size 1500",
            "--crf 18 -b3 -m9 -r5 --me umh -t1 -A all --b-pyramid normal --direct auto --no-fast-pskip --no-mbtree",
            "--crf 22 -b3 -m7 -r4 --me esa -t2 -A all --psy-rd 1.0:1.0 --slices 4",
            "--frames 50 --crf 24 -b3 -m10 -r3 --me tesa -t2",
            "--frames 50 -q0 -m9 -r2 --me hex -Aall",
            "--frames 50 -q0 -m2 -r1 --me hex --no-cabac",
        ]

        for ifile in self.inputfiles:
            testfile = local.path(self.testdir) / ifile
            for _, test in enumerate(tests):
                runner(x264[testfile, self.inputfiles[ifile], "--threads", "1",
                            "-o", "/dev/null",
                            test.split(" ")])
