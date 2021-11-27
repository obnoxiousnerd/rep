from os import path
from driver_class import Renderer
from jinja2 import Template


class HTMLTemplateRenderer(Renderer):
    def render(self, student_data: dict) -> str:
        template_config = self.config.get("template")
        if template_config is None:
            self.logger.fatal(
                f"Configuration does not exist for templates. "
                + "Please add configuration for template paths in config/config.yml."
            )

        # The template path is relative to the config directory
        pdf_template_path = path.join(
            "config", *path.split(template_config.get("pdf"))  # type:ignore
        )
        # template_config is already checked to be not None, so this error can be ignored.
        pdf_template = Template(open(pdf_template_path, "r").read())
        rendered_html = pdf_template.render(student=student_data, config=self.config)
        return rendered_html
