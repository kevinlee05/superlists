import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/kevinlee05/superlists.git'

def deploy():
    site_folder = f'/home/klee05/superlists/'
    site_folder1 = f'/home/{env.user}/sites/{env.host}'
    """env.user will contain the username you’re using to log in to the server;
    env.host will be the address of the server we’ve specified at the command line
    """
    run(f'mkdir -p {site_folder}')
    """
    run is the most common Fabric command. It says "run this shell command on the server".
    The run commands in this chapter will replicate many of the commands we did manually in the last two.

    mkdir -p is a useful flavour of mkdir, which is better in two ways:
    it can create directories several levels deep, and it only creates them if necessary.
    So, mkdir -p /tmp/foo/bar will create the directory bar but also its parent directory foo if it needs to.
    It also won’t complain if bar already exists
    """
    with cd(site_folder):
        """ cd is a fabric context manager that says "run all the following statements inside this working directory"
        """
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()

def _get_latest_source():
    if exists('.git'):
    """ checks whether a directory or file already exists on the server.
    We look for the .git hidden folder to check whether the repo has already been cloned in our site folder.
    """
        run('git fetch')
        """ git fetch inside an existing repository pulls down all the latest commits from the web
        (it’s like git pull, but without immediately updating the live source tree)."""
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    """ invocation to get the ID of the current commit that’s on your local PC.
    That means the server will end up with whatever code is currently checked out on your machine
    (as long as you’ve pushed it up to the server. Another common gotcha!)."""
    run(f'git reset --hard {current_commit}')
    """ We reset --hard to that commit, which will blow away any current changes in the server’s code directory """

def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
    # We look inside the virtualenv folder for the pip executable as a way of checking whether it already exists
        run(f'python3.6 -m venv virtualenv')
    run('./virtualenv/bin/pip install -r requirements.txt')

def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(randon.SystemRandom().choices('adf234qweac1231', k=50))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')






