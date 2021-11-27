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
def cli(ctx: click.Context):
    if ctx.invoked_subcommand is None:
        print(Fore.CYAN + "This is rep." + Fore.RESET)


cli.add_command(generate)

if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        main_logger.fatal("error while running CLI: %s", str(e), exc_info=True)
