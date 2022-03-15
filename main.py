import typer
from jinja2 import Template
from auxiliary import parse_yaml
from enum import Enum
import docker
import random
import string
import os
import shutil
import datetime

app = typer.Typer()


@app.command("template")
def template():
    with open('templates/YAML/example.yaml') as fp:
        print(fp.read())


@app.command("up")
def main(path_to_yaml, copy: str = None, deploy: bool = False, build: str = '', dockerfile_base_path: str = '/tmp') -> str:
    """
    Build a container from a manifest tile
    """
    yaml_data = parse_yaml(path_to_yaml)

    # typer.echo(yaml_data)


    build_timestamp = datetime.datetime.now().astimezone()
    if build_timestamp == 0:
        sign = "Z"
        diff = ""
    else:
        diff = build_timestamp.utcoffset().seconds / 3600
        if diff > 0:
            sign = "+"
        else:
            sign = "-"

    build_date = "{0}T{1}{2}{3}".format(
        build_timestamp.strftime("%Y-%m-%d"),
        build_timestamp.strftime("%H:%M:%S"),
        sign,
        diff
    )

    base_image = yaml_data['spec']['base']['name']

    with open('templates/Dockerfiles/{0}.j2'.format(base_image)) as fp:
        dockerfile = Template(fp.read()).render(yaml_data=yaml_data, build_date=build_date)

    typer.secho("Setting up the build environment", fg='blue')


    dockerfile_path = "{0}/container-{1}".format(
        dockerfile_base_path,
        ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
    )

    os.mkdir(dockerfile_path)

    dockerfile_filename = "{0}/{1}".format(
        dockerfile_path,
        "Dockerfile"
    )

    with open(dockerfile_filename, "w") as fp:
        fp.write(dockerfile)

    # init file
    with open("{0}/init".format(dockerfile_path), 'w') as fp:
        fp.write(yaml_data['spec']['entrypoint'])

    typer.secho("Building the container", fg='blue')

    client = docker.from_env()
    client.images.build(path=dockerfile_path, rm=True)

    typer.secho("The image has been built succesfully")

    if deploy:
        client.images.push('rutgerhartog/lift', tag='latest')


    typer.secho("Cleaning up...", fg='blue')
    shutil.rmtree(dockerfile_path)

    typer.secho("All done!", fg='green')

app()
