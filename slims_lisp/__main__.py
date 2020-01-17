import click
from slims_lisp.slims import Slims

@click.group()
def cli():
    pass

@cli.command(help="Download a file and its associated metadata from a slims experiment attachment step.")
@click.option('--url',
    help = 'Slims REST URL. ex: https://<your_slims_address>/rest/rest',
    required = True)
@click.option('--proj',
    help = 'Project name (if any).',
    required = False)
@click.option('-e', '--exp',
    help = 'Experiment name.',
    required = True)
@click.option('-s', '--step',
    default = 'data_collection',
    help = 'Experiment step name.',
    required = True,
    show_default = True)
@click.option('-a', '--attm',
    help = 'Attachment name.',
    required = True)
@click.option('--active',
    help = 'Search only in active or inactive steps (or in both).',
    type = click.Choice(['true', 'false', 'both'],
        case_sensitive = False),
    default = 'true',
    required = False,
    show_default = True)
@click.option('-l', '--linked',
    help = 'Search only linked or unlinked attachments (or both).',
    type = click.Choice(['true', 'false', 'both'],
        case_sensitive = False),
    default = 'true',
    required = False,
    show_default = True)
@click.option('-o', '--output',
    help = 'Output file name. [default: same as --attm]',
    required = False)
@click.option('-u', '--username',
    prompt = "User",
    help = 'User name (prompted).',
    required = True)
@click.option('-p', '--pwd',
    prompt = "Password",
    hide_input = True,
    help = 'Password (prompted).',
    required = True)
def fetch(url, username, pwd, proj, exp, step, attm, active, linked, output):
    slims = Slims(url = url,
        username = username,
        pwd = pwd)
    slims.download_attachment(proj = proj,
        exp = exp,
        step = step,
        attm = attm,
        active = active,
        linked = linked,
        output = output
    )

@cli.command(help="Upload a file to a slims experiment attachment step.")
@click.option('--url',
    help = 'Slims REST URL. ex: https://<your_slims_address>/rest/rest',
    required = True)
@click.option('--proj',
    help = 'Project name (if any).',
    required = False)
@click.option('-e', '--exp',
    help = 'Experiment name.',
    required = True)
@click.option('--step',
    default = 'data_collection',
    help = 'Experiment step name.',
    required = True,
    show_default = True)
@click.option('--active',
    help = 'Search only in active or inactive steps (or in both).',
    type = click.Choice(['true', 'false', 'both'],
        case_sensitive = False),
    default = 'true',
    required = False,
    show_default = True)
@click.option('--source',
    help = 'Path to the file that will be uploaded.',
    required = True)
@click.option('-t', '--target',
    help = 'A name to give to the attachement that will be created. [default: same as --source]',
    required = False)
@click.option('-u', '--username',
    prompt = "User",
    help = 'User name (prompted).',
    required = True)
@click.option('-p', '--pwd',
    prompt = "Password",
    hide_input = True,
    help = 'Password (prompted).',
    required = True)
def add(url, username, pwd, proj, exp, step, active, source, target):
    slims = Slims(url = url,
        username = username,
        pwd = pwd)
    slims.upload_attachment(proj = proj,
        exp = exp,
        step = step,
        active = active,
        source = source,
        target = target
    )

if __name__ == '__main__':
    cli()
