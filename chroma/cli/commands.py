import click
from chroma.utils.utils import PATH_IMAGES
from .core import SegImage, SegWebCam

@click.group()
def chroma():
    pass

@click.command()
@click.option("--image", default=(PATH_IMAGES / "2.jpeg"), help="Caminho da imagem que deseja aplicar o efeito.")
@click.option("--color", default=None, help="Cor do plano de fudo da imagem. No caso default a cor é verde.")
@click.option("--back", default=(PATH_IMAGES / "4.jpg"), help="Imagem que deseja aplicar de plano de fundo. No caso defaul a cor é preta")
def image(image, back, color):
   SegImage(image, back, color)

@click.command()
def webcam():
    SegWebCam()

chroma.add_command(image)
chroma.add_command(webcam)