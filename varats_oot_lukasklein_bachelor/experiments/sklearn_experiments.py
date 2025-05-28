"""Implements an empty experiment that just compiles the project."""

import typing as tp
import textwrap

from varats_oot_lukasklein_bachelor.reports.sklearn_report import SklearnReport
from varats_oot_lukasklein_bachelor.projects.sklearn import SklearnLKBachelor
from benchbuild import Project
from benchbuild.utils import actions
from benchbuild.utils.cmd import cp

from varats.experiment.experiment_util import (
    VersionExperiment,
    ExperimentHandle,
    create_new_success_result_filepath,
)
from varats.project.varats_project import VProject
from varats.report.report import ReportSpecification
from varats.utils.config import get_current_config_id

from benchbuild.utils.actions import ProjectStep, StepResult
from benchbuild.command import cleanup
from varats.experiment.workload_util import (
    workload_commands,
    WorkloadCategory,
)
from plumbum import local

from varats.experiment.experiment_util import (
    VersionExperiment,
    create_new_success_result_filepath,
    ExperimentHandle,
)
if tp.TYPE_CHECKING:
    from varats.project.project_util import ProjectBinaryWrapper
    from varats.project.varats_project import VProject


class SklearnMeasuringEstims(ProjectStep):  # type: ignore TODO: Class name etc. anpassen an mein Experiment
    """Step to sample call stack with perf and measure total execution using GNU
    Time."""

    NAME = "SklearnMeasuringEstims"
    DESCRIPTION = (
        "Sample call stack using perf and measure total execution time"
    )

    project: "VProject"

    def __init__(
        self,
        project: "VProject",
        experiment_handle: ExperimentHandle,
        binary: "ProjectBinaryWrapper",
        repetitions: int = 1,
        sampling_rate: int = 997
    ):
        super().__init__(project=project)
        self.__experiment_handle = experiment_handle
        self.__binary = binary
        self.__repetitions = repetitions
        self.__sampling_rate = sampling_rate

    def __call__(self) -> StepResult:
        # get workload to use
        workloads = workload_commands(
            self.project, self.project.binaries[0], [WorkloadCategory.EXAMPLE]
        )
        if len(workloads) == 0:
            print(
                f"No workload for project={self.project.name} "
                f"binary={self.__binary.name}. Skipping."
            )
            return StepResult.OK

        # report paths
        perf_report_agg = create_new_success_result_filepath(
            self.__experiment_handle, SklearnReport,
            self.project, self.__binary, get_current_config_id(self.project)
        )

        with local.cwd(self.project.builddir):
            #run_cmd = workload.command.as_plumbum(project=project)
            run_cmd = workloads.command.as_plumbum(project=SklearnLKBachelor) # TODO: This or above?
            run_cmd(retcode=None)
            cp("PATH", perf_report_agg.full_path()) # TODO: PATH = case_study_MNIST.py output file

        return StepResult.OK

    def __str__(self, indent: int = 0) -> str:
        return textwrap.indent(
            f"* {self.project.name}: Measure with time and sample with perf ({self.__repetitions} reps)",
            " " * indent
        )


# Please take care when changing this file, see docs experiments/just_compile
class JustCompileTest(VersionExperiment, shorthand="JCT"):
    """Generates empty report file."""

    NAME = "JustCompileTest"

    REPORT_SPEC = ReportSpecification(SklearnReport)

    def actions_for_project(
            self, project: Project) -> tp.MutableSequence[actions.Step]:
        """Returns the specified steps to run the project(s) specified in the
        call in a fixed order."""

        analysis_actions = []
        #analysis_actions.append(EmptyAnalysis(project, self.get_handle())) # TODO: Mein Experiment callen
        analysis_actions.append(actions.Clean(project))
        print("Setting steps")

        return analysis_actions
