import click
from slims_lisp.slims import Slims

@click.group()
def cli():
    """ \b
A high-level CLI for SLIMS REST API
    """
    pass

@cli.command()
@click.option('--url',
    help = 'Slims REST URL. ex: https://<your_slims_address>/rest/rest',
    required = True)
@click.option('--proj',
    help = 'Project name (if any).',
    required = False)
@click.option('--exp',
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
@click.option('--attm',
    help = 'Attachment name.',
    required = True)
@click.option('--linked',
    help = 'Search only linked or unlinked attachments (or both).',
    type = click.Choice(['true', 'false', 'both'],
        case_sensitive = False),
    default = 'true',
    required = False,
    show_default = True)
@click.option('--output',
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
def fetch(url, username, pwd, proj, exp, step, active, attm, linked, output):
    """\b
Download a file from a slims experiment attachment step.


Return:

    Returns the HTTP GET request response.


Output:

    Generates two files (by default in the working directory):

        -<output>               The requested file\n
        -<output>_metadata.txt  Associated metadata in a JSON format


Example:

    $ slims-lisp fetch --url <your_slims_url> \
--proj <your_project_name> --exp <your_experiment_name> \
--step <your_attachment_step_name> --attm <your_attachment_name>
    """

    slims = Slims(url = url,
        username = username,
        pwd = pwd)
    response = slims.download_attachment(proj = proj,
        exp = exp,
        step = step,
        active = active,
        attm = attm,
        linked = linked,
        output = output
    )
    return response

@cli.command()
@click.option('--url',
    help = 'Slims REST URL. ex: https://<your_slims_address>/rest/rest',
    required = True)
@click.option('--proj',
    help = 'Project name (if any).',
    required = False)
@click.option('--exp',
    help = 'Experiment name.',
    required = True)
@click.option('--step',
    default = 'results',
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
@click.option('--file',
    help = 'Path to the file that will be uploaded.',
    required = True)
@click.option('--attm',
    help = 'A name to give to the attachement that will be created. [default: same as --file]',
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
def add(url, username, pwd, proj, exp, step, active, file, attm):
    """\b
Upload a file to a slims experiment attachment step.


Return:

    Returns the HTTP POST request response.


Example:

    $ slims-lisp add --url <your_slims_url> --proj <your_project_name> \
--exp <your_experiment_name> --step <your_attachment_step_name> \
--file <path/to/your/file>
    """

    slims = Slims(url = url,
        username = username,
        pwd = pwd)
    response = slims.upload_attachment(proj = proj,
        exp = exp,
        step = step,
        active = active,
        file = file,
        attm = attm
    )
    return response

if __name__ == '__main__':
    cli()
