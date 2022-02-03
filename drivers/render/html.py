from os import path
from driver_class import Renderer
from jinja2 import Template


class HTMLTemplateRenderer(Renderer):
    def render(self, student_data: dict) -> str:
        template_file_path = self.config.get("template")
        if template_file_path is None:
            self.logger.fatal("Template file path is not provided.")

        # The template path is relative to the config directory
        template_path = path.join(
            "config", *path.split(template_file_path)  # type:ignore
        )
        # template_config is already checked to be not None, so this error can be ignored.
        with open(template_path, "r") as template_file:
            template = Template(template_file.read())
            rendered_html = template.render(student=student_data, config=self.config)
        return rendered_html
