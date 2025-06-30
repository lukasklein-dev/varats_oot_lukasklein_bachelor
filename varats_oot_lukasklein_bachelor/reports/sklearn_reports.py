"""Empty report implementation for testing."""

from varats.report.report import BaseReport


class SklearnMeasuringReports(BaseReport, shorthand="SMR", file_type="txt"):
    """
    An empty report for testing.

    Nothing gets printed into the report and the result file has no file type.
    """
    