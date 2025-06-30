"""Implements an experiment that measures the sklearn estimator performance."""

import typing as tp
import textwrap

from varats_oot_lukasklein_bachelor.reports.sklearn_reports import SklearnMeasuringReports
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
import varats.utils.config as cfg

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


class SklearnExperiment(ProjectStep):  # type: ignore
    """Step to call a script that measures the performance of sklearn estimators."""

    NAME = "SklearnExperiment"
    DESCRIPTION = (
        "Call a script that measures the performance of sklearn estimators"
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
        print("Hi")
        workloads = workload_commands(
            #self.project, self.project.binaries[0], [WorkloadCategory.MEDIUM]
            self.project, self.__binary, [WorkloadCategory.MEDIUM]
        )

        if len(workloads) == 0:
            print(
                f"No workload for project={self.project.name} "
                f"binary={self.__binary.name}. Skipping."
            )
            return StepResult.OK

        # report paths
        perf_report_agg = create_new_success_result_filepath(
            self.__experiment_handle, SklearnMeasuringReports,
            self.project, self.__binary, get_current_config_id(self.project)
        )

        with local.cwd(self.project.builddir):
            #run_cmd = workloads.command.as_plumbum(project=self.project)
            run_cmd = workloads[0].command.as_plumbum(project=self.project)
            print(run_cmd.formulate()) # DEBUGGING
            run_cmd(retcode=None)
            cp("scripts/io/mnist/cs_output/perf_measurements.json", perf_report_agg.full_path())

        return StepResult.OK

    def __str__(self, indent: int = 0) -> str:
        return textwrap.indent(
            f"* {self.project.name}: Measure estimator performance ({self.__repetitions} reps)",
            " " * indent
        )


# Please take care when changing this file, see docs experiments/just_compile
class SklearnMeasuring(VersionExperiment, shorthand="SME"):
    """Implements an experiment that measures the sklearn estimator performance."""

    NAME = "SklearnMeasuring"

    REPORT_SPEC = ReportSpecification(SklearnMeasuringReports)

    def actions_for_project(
            self, project: Project) -> tp.MutableSequence[actions.Step]:
        """Returns the specified steps to run the project(s) specified in the
        call in a fixed order."""

        # Only consider the first/main binary
        binary = project.binaries[0]

        analysis_actions = [
            SklearnExperiment(project, self.get_handle(), binary),
            actions.Clean(project)
        ]
        
        return analysis_actions