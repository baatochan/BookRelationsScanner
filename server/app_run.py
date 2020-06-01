import click
from app.services.app import app as flask_app
import app

@click.group()
def cli():
    pass


@cli.command()
def run():
    flask_app.app_context().push()
    flask_app.run(debug=True)


if __name__ == '__main__':
    cli()
