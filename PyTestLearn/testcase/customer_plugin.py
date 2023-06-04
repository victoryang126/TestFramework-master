import pytest

def pytest_html_report_title(report):
    report.title = "My very own title!"


def pytest_configure(config):
    config._metadata["foo"] = "bar"


# This plugin exposes the following hooks:

# def pytest_html.hooks.pytest_html_report_title(report):
#
#     Called before adding the title to the report
#
# pytest_html.hooks.pytest_html_results_summary(prefix, summary, postfix, session)
# Called before adding the summary section to the report
#
# pytest_html.hooks.pytest_html_results_table_header(cells)
# Called after building results table header.
#
# pytest_html.hooks.pytest_html_results_table_html(report, data)
# Called after building results table additional HTML.
#
# pytest_html.hooks.pytest_html_results_table_row(report, cells)
# Called after building results table row.