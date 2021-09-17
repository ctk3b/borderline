from pathlib import Path

import pytest

import borderline
from borderline import ModuleImports


class TestReportBuilder(ModuleImports):
    module = "reporting.report_builder"
    public_submodules = ("reporting.report_builder.api",)
    external_modules = ("reporting",)
    external_dependencies = (
        "reporting.review.api",
        "reporting.common",
    )

    grandfather_filedir = Path(__file__).parent.joinpath("borderline")
    record_grandfather = False

    def test_module(self):
        with pytest.raises(borderline.ModuleImportViolation) as violation:
            super().test_module()

        expected_violations = (
            [
                (
                    "reporting.report_builder.__init__.py",
                    "Import(names=[alias(name='reporting.review.this_is_a_violation', asname=None)])",
                ),
                (
                    "reporting.report_builder.api.py",
                    "ImportFrom(module='reporting.review', names=[alias(name='this_is_a_violation', asname=None)], level=0)",
                ),
                (
                    "reporting.api.py",
                    "Import(names=[alias(name='reporting.report_builder.this_is_a_violation', asname=None)])",
                ),
            ],
        )
        assert violation.value.args == expected_violations
