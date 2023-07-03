from bs4 import BeautifulSoup

class HTMLReportGenerator:
    def __init__(self):
        self.html = BeautifulSoup('<html><head></head><body></body></html>', 'html.parser')
        self.head = self.html.head
        self.body = self.html.body

    def add_style(self, style):
        style_tag = self.html.new_tag('style')
        style_tag.string = style
        self.head.append(style_tag)

    def add_script(self, script):
        script_tag = self.html.new_tag('script')
        script_tag.string = script
        self.body.append(script_tag)

    def generate_html(self):
        return str(self.html)

    def save_html_file(self, filename):
        html = self.generate_html()
        with open(filename, "w") as file:
            file.write(html)


# 使用示例
report_generator = HTMLReportGenerator()

style = """
/* 样式内容 */
"""

script = """
/* 脚本内容 */
"""

report_generator.add_style(style)
report_generator.add_script(script)

report_generator.save_html_file("report.html")
