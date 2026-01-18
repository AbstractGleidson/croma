import click

@click.group()
def chroma():
    pass

@click.command()
def image():
    click.echo("Image")

@click.command()
def webcam():
    click.echo("WebCam")


chroma.add_command(image)
chroma.add_command(webcam)