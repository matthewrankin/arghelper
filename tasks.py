from invoke import run, task

TESTPYPI = "https://testpypi.python.org/pypi"


@task
def lint():
    """Run flake8 to lint code"""
    run("python setup.py flake8")


@task(lint)
def test():
    """Lint, unit test, and check setup.py"""
    run("nosetests")
    run("python setup.py check")


@task()
def release(start=False, finish=False, deploy=False, test=False, version=''):
    """Release arghelper and deploy to PyPI
    """
    if test:
        run("python setup.py check")
        run("python setup.py register sdist upload --dry-run")

    if start:
        if version:
            run("git flow release start v{ver}".format(
                ver=version))
    if finish:
        run("python setup.py check")
        if deploy:
            if version:
                run("python setup.py sdist")
                run("git flow release finish -m '{ver}' v{ver}".format(
                    ver=version), echo=True)
                run("git push --tags")
                run("git checkout master")
                run("python setup.py register sdist upload")
                run("git checkout develop")
                """Run flake8 to lint code"""
        else:
            print("* Have you updated the version in arghelper.py?")
            print("* Have you updated CHANGES.md?")
            print("* Have you fixed any last minute bugs?")
            print("If you answered yes to all of the above questions,")
            print("then run `invoke release --finish --deploy -vX.YY`")
