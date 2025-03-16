import pdfkit
import markdown2


class Url2Pdf:
    def __init__(self, wkhtmltopdf_path):
        self.config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        self.options = {
            "page-size": "A4",
            "encoding": "UTF-8",
            "dpi": "96",
            "image-dpi": "600",
            "image-quality": "94",
            "footer-font-size": "80",
            "no-outline": None,
            "zoom": 2,
        }

    def url_to_pdf(self, url, title):
        pdfkit.from_url(
            url, "{}.pdf".format(title), configuration=self.config, options=self.options
        )


class Html2Markdown:
    def convert(self, html_content, title):
        md_content = markdown2.markdown(html_content)
        with open(f"{title}.md", "w", encoding="utf-8") as f:
            f.write(md_content)
