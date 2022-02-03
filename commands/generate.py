import asyncio
import os
from jinja2 import Template
from drivers.render.pdf import PDFRenderer
from os import path
from drivers.render.html import HTMLTemplateRenderer
import logging
from driver_class import Config
from drivers import data_drivers, email_drivers
from pipe import data_pipes
from driver_class import log_stream
from base64 import b64encode

generate_logger = logging.getLogger("generate")
generate_logger.addHandler(log_stream)
generate_logger.setLevel(logging.DEBUG)


def generate(source, email_method):
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

    pdf_html_renderer_config = config.get("generate")
    # Signature image path is relative to the config directory.
    signature_image_path = path.join(
        "config",
        *path.split(pdf_html_renderer_config.get("authority").get("signature_image")),
    )
    if signature_image_path is None:
        generate_logger.info(
            "The signature file is not provided, skipped adding image to report cards."
        )
    else:
        with open(signature_image_path, "rb") as file:
            signature_image_file = file.read()
            signature_image_b64 = b64encode(signature_image_file).decode("utf-8")
            pdf_html_renderer_config["authority"][
                "signature_image_b64"
            ] = signature_image_b64

    school_name = config.get("generate").get("school_name")
    if not school_name:
        school_name = input("Enter school name: ")
    exam_name = config.get("generate").get("exam_name")
    if not exam_name:
        exam_name = input("Enter exam name: ")

    pdf_html_renderer_config["school_name"] = school_name
    pdf_html_renderer_config["exam_name"] = exam_name

    pdf_html_renderer = HTMLTemplateRenderer(pdf_html_renderer_config)
    pdf_renderer = PDFRenderer(config.get("generate"))

    output_folder = config.get("generate")["output"].get("folder", "./out")
    if not path.exists(output_folder):
        os.makedirs(output_folder)

    filename_format_template = config.get("generate")["output"].get(
        "filename_format", "{{ RollNo }}-{{ Name }}.pdf"
    )

    generate_logger.info("Generating PDFs")
    generate_logger.info(f"PDFs will be saved in {output_folder}")

    for student_data in data:
        rendered_html = pdf_html_renderer.render(student_data)
        raw_pdf = asyncio.run(pdf_renderer.render(rendered_html))
        filename = Template(filename_format_template).render(**student_data)
        file_path = path.join(output_folder, filename)
        with open(file_path, "wb+") as file:
            file.write(raw_pdf)
            generate_logger.info(
                f"Saved PDF report for {student_data['Name']} in {file_path}"
            )
        student_data["pdf_path"] = file_path
    generate_logger.info("Generation complete")

    # Send emails, if flag is set.
    if email_method:
        email_config = config.get("email")
        email_config["generate"] = config.get("generate")
        generate_logger.info("Sending emails")
        if email_method not in email_drivers:
            generate_logger.fatal(
                f"Email driver {email_method} does not exist. Please double check the email driver name."
                + " If this was intentional, please check if you have registered the driver correctly."
            )
            exit(1)
        email_driver = email_drivers[email_method](email_config)
        template_path = email_config.get("template")
        if template_path is None:
            generate_logger.fatal(
                "Email template is not provided. Please double check the configuration."
            )
            exit(1)

        for student_data in data:
            email_driver.send(student_data)

        generate_logger.info("Email sending complete")
