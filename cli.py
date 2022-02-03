from commands.generate import generate
import logging
import click
import colorama
from colorama.ansi import Fore
from driver_class import log_stream

# Initialise ANSI colors.
colorama.init()


main_logger = logging.getLogger("main")
main_logger.addHandler(log_stream)
main_logger.setLevel(logging.DEBUG)


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--source", default="csv", help="Specify the source to load the data into the CLI."
)
@click.option(
    "--email-method",
    help="Specify the email method to use for sending the email."
    + " Emails won't be sent if this is not specified.",
)
def cli(_, source, email_method):
    """
    This is rep.
    rep is a CLI for generating PDFs and sending them via email.
    """
    if _.invoked_subcommand is None:
        generate(source, email_method)


if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        main_logger.fatal("error while running CLI: %s", str(e), exc_info=True)
