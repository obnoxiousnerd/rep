import asyncio
import os
from jinja2 import Template
from drivers.render.pdf import PDFRenderer
from os import path
from drivers.render.html import HTMLTemplateRenderer
import logging
from driver_class import Config
import click
from drivers import data_drivers
from pipe import data_pipes
from driver_class import log_stream
from base64 import b64encode

generate_logger = logging.getLogger("generate")
generate_logger.addHandler(log_stream)
generate_logger.setLevel(logging.DEBUG)


@click.command()
@click.option(
    "--source", default="csv", help="Specify the source to load the data into the CLI."
)
def generate(source):
    config = Config()
    data_driver_config = config.get("generate").get("data")

    # Check if configuration actually exists.
    if data_driver_config.get(source) is None:
        generate_logger.fatal(
            f"Config does not exist for {source}. Please add configuration for {source} in config/config.yml"
        )
        exit(1)

    # Check if driver for the source actually exists.
    if data_drivers.get(source) is None:
        generate_logger.fatal(
            f"Driver does not exist for {source}. Please double check the source name."
            + " If this was intentional, please check if you have registered the driver correctly."
        )
        exit(1)

    driver = data_drivers[source](data_driver_config.get(source))

    generate_logger.info(f"Using source {source} to load data...")
    data = driver.load()

    generate_logger.info("Passing data through the pipes")
    # Run the data through all the data pipes.
    for pipe in data_pipes:
        data = pipe(data, config.get("generate"))

    if len(data) == 0:
        generate_logger.fatal(
            "Generated data is empty."
            + " Is anything actually getting generated?"
            + " Double check if data is being passed correctly."
        )

    html_renderer_config = config.get("generate")
    # Signature image path is relative to the config directory.
    signature_image_path = path.join(
        "config",
        *path.split(html_renderer_config.get("authority").get("signature_image")),
    )
    if signature_image_path is None:
        generate_logger.info(
            "The signature file is not provided, skipped adding image to report cards."
        )
    else:
        signature_image_file = open(signature_image_path, "rb").read()
        signature_image_b64 = b64encode(signature_image_file).decode("utf-8")
        html_renderer_config["authority"]["signature_image_b64"] = signature_image_b64

    school_name = config.get("generate").get("school_name")
    if not school_name:
        school_name = input("Enter school name: ")
    exam_name = config.get("generate").get("exam_name")
    if not exam_name:
        exam_name = input("Enter exam name: ")

    html_renderer_config["school_name"] = school_name
    html_renderer_config["exam_name"] = exam_name

    html_renderer = HTMLTemplateRenderer(html_renderer_config)
    pdf_renderer = PDFRenderer(config.get("generate"))

    output_folder = config.get("generate")["output"].get("folder", "./out")
    if not path.exists(output_folder):
        os.makedirs(output_folder)

    filename_format_template = config.get("generate")["output"].get(
        "filename_format", "{{ RollNo }}-{{ Name }}.pdf"
    )

    generate_logger.info("Generating PDFs")
    generate_logger.info(f"PDFs will be saved in {output_folder}")
    student_data = data[0]
    for student_data in data:
        rendered_html = html_renderer.render(student_data)
        raw_pdf = asyncio.run(pdf_renderer.render(rendered_html))
        filename = Template(filename_format_template).render(**student_data)
        file_path = path.join(output_folder, filename)
        open(file_path, "wb+").write(raw_pdf)
        generate_logger.info(
            f"Saved PDF report for {student_data['Name']} in {file_path}"
        )
