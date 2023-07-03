from bs4 import BeautifulSoup


class HTMLReportGenerator:
    def __init__(self):
        self.soup = BeautifulSoup(features="html.parser")
        self.table = self.soup.new_tag("table", id="results-table")
        self.soup.append(self.table)
        self.add_table_head()
        self.tbody = self.soup.new_tag("tbody", class_="Failed results-table-row")
        self.table.append(self.tbody)

    def add_table_head(self):
        thead = self.soup.new_tag("thead", id="results-table-head")
        self.table.append(thead)
        tr = self.soup.new_tag("tr")
        thead.append(tr)
        headers = ["Timestamp", "Test Class", "Result", "Duration (s)"]
        for header in headers:
            th = self.soup.new_tag("th", col=header.lower().replace(" ", "-"))
            th.string = header
            tr.append(th)
        not_found_row = self.soup.new_tag("tr", hidden="true", id="not-found-message")
        thead.append(not_found_row)
        not_found_data = self.soup.new_tag("th", colspan="5")
        not_found_data.string = "No results found. Try to check the filters"
        not_found_row.append(not_found_data)

    def add_test_case(self, timestamp, test_class, result, duration):
        tr = self.soup.new_tag("tr")
        self.tbody.append(tr)

        td_timestamp = self.soup.new_tag("td", class_="col-time")
        td_timestamp.string = timestamp
        tr.append(td_timestamp)

        td_test_class = self.soup.new_tag("td", class_="col-test-class")
        td_test_class.string = test_class
        tr.append(td_test_class)

        td_result = self.soup.new_tag("td", class_="col-result")
        td_result.string = result
        tr.append(td_result)

        td_duration = self.soup.new_tag("td", class_="col-duration")
        td_duration.string = duration
        tr.append(td_duration)

    def add_test_steps_table(self, test_case, test_steps):
        tr = self.soup.new_tag("tr")
        self.tbody.append(tr)

        td_extra = self.soup.new_tag("td", class_="extra", colspan="5")
        tr.append(td_extra)

        div = self.soup.new_tag("div")
        td_extra.append(div)

        test_cases_table = self.soup.new_tag("table", class_="test_cases")
        div.append(test_cases_table)

        thead = self.soup.new_tag("thead", class_="test_case_header")
        test_cases_table.append(thead)

        tr = self.soup.new_tag("tr")
        thead.append(tr)

        headers = ["Timestamp", "TestCase", "Duration (s)", "Result", ""]
        for header in headers:
            th = self.soup.new_tag("th")
            th.string = header
            tr.append(th)

        tbody = self.soup.new_tag("tbody")
        test_cases_table.append(tbody)

        test_case_row = self.soup.new_tag("tr", class_="Passed results-table-row")
        tbody.append(test_case_row)

        for data in test_case:
            td = self.soup.new_tag("td")
            td.string = data
            test_case_row.append(td)

        details_row = self.soup.new_tag("tr", class_="details")
        tbody.append(details_row)

        td_details = self.soup.new_tag("td", colspan="6")
        details_row.append(td_details)

        test_steps_table = self.soup.new_tag("table", class_="test_steps")
        td_details.append(test_steps_table)

        thead = self.soup.new_tag("thead")
        test_steps_table.append(thead)

        tr = self.soup.new_tag("tr", class_="test_step_header")
        thead.append(tr)

        headers = ["Timestamps", "TestSteps", "Action", "Expect", "Actual", "Result"]
        for header in headers:
            th = self.soup.new_tag("th")
            th.string = header
            tr.append(th)

        tbody = self.soup.new_tag("tbody")
        test_steps_table.append(tbody)

        for step_data in test_steps:
            tr = self.soup.new_tag("tr", class_=step_data["result"])
            tbody.append(tr)

            for data in step_data["data"]:
                td = self.soup.new_tag("td")
                td.string = data
                tr.append(td)

    def generate_html(self, file_path):
        with open(file_path, "w") as file:
            file.write(self.soup.prettify())


# Usage example
generator = HTMLReportGenerator()

generator.add_test_case("2023-06-03 17:45:59.798782", "TestClassName", "Failed", "0.0046")

test_steps_data = [
    {
        "result": "Passed",
        "data": ["2023-06-03 17:45:59.798874", "Step 1", "Check if the array is equal",
                 "Expect1", "Expect1", "Passed"]
    },
    {
        "result": "Failed",
        "data": ["2023-06-03 17:45:59.803128", "Step 3", "Action3", "Expect3", "Actual4", "Failed"]
    }
]

generator.add_test_steps_table(["2023-06-03 17:45:59.798834", "TestCase1", "0.0001", "Passed"], test_steps_data)

generator.generate_html("report.html")
