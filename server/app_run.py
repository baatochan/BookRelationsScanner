import click
from app import app


@click.group()
def cli():
    pass


@cli.command()
def run():
    app.app_context().push()
    app.run()


if __name__ == '__main__':
    cli()
