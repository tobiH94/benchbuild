"""
The 'compilestats' experiment.

This experiment is a basic experiment in the benchbuild study. It simply runs
all projects after compiling it with -O3 and catches all statistics emitted
by llvm.

"""
from benchbuild.experiment import RuntimeExperiment
from benchbuild.extensions import ExtractCompileStats

class CompilestatsExperiment(RuntimeExperiment):
    """The compilestats experiment."""

    NAME = "cs"

    def actions_for_project(self, p):
        p.compiler_extension = ExtractCompileStats(p, self, {})
        return CompilestatsExperiment.default_compiletime_actions(p)


class PollyCompilestatsExperiment(RuntimeExperiment):
    """The compilestats experiment with polly enabled."""

    NAME = "p-cs"

    def actions_for_project(self, p):
        p.cflags = ["-O3",
                    "-Xclang", "-load",
                    "-Xclang", "LLVMPolly.so",
                    "-mllvm", "-polly"]
        p.compiler_extension = ExtractCompileStats(p, self, {})
        return CompilestatsExperiment.default_compiletime_actions(p)
