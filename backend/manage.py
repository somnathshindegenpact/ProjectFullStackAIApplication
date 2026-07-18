import click
from app import create_app, db
from flask_migrate import init as _init, migrate as _migrate, upgrade as _upgrade, downgrade as _downgrade, revision as _revision, stamp as _stamp

app = create_app()


@click.group()
def cli():
    """Management commands for database migrations."""
    pass


@cli.command('db-init')
def db_init():
    """Initialize the migrations directory."""
    with app.app_context():
        _init()
        click.echo('migrations directory initialized')


@cli.command('db-migrate')
@click.option('--message', '-m', default='auto migration')
def db_migrate(message):
    """Autogenerate a new migration."""
    with app.app_context():
        _migrate(message=message)
        click.echo('migration generated')


@cli.command('db-revision')
@click.option('--message', '-m', default='revision')
def db_revision(message):
    """Create an empty revision with a message."""
    with app.app_context():
        _revision(message=message, autogenerate=False)
        click.echo('empty revision created')


@cli.command('db-upgrade')
@click.option('--rev', default='head')
def db_upgrade(rev):
    """Apply migrations up to given revision (default: head)."""
    with app.app_context():
        _upgrade(rev)
        click.echo(f'upgraded to {rev}')


@cli.command('db-downgrade')
@click.argument('rev')
def db_downgrade(rev):
    """Downgrade to a given revision."""
    with app.app_context():
        _downgrade(rev)
        click.echo(f'downgraded to {rev}')


@cli.command('db-stamp')
@click.option('--rev', default='head')
def db_stamp(rev):
    """Stamp the revision in the database without running migrations."""
    with app.app_context():
        _stamp(rev)
        click.echo(f'stamped {rev}')


if __name__ == '__main__':
    cli()
