import click
from chroma.utils.utils import PATH_IMAGES
from .core import SegImage, SegWebCam

@click.group()
def chroma():
    pass

@click.command()
@click.option("--image", default=(PATH_IMAGES / "2.jpeg"), help="Caminho da imagem que deseja aplicar o efeito.")
@click.option("--color", default=None, help="Cor do plano de fudo da imagem. No caso default a cor é verde.")
@click.option("--back", default=(PATH_IMAGES / "4.jpg"), help="Imagem que deseja aplicar de plano de fundo. No caso default a cor é preta.")
def image(image, back, color):
   SegImage(image, back, color)

@click.command()
@click.option("--webcam", default=0, help="Index da webcam. Por padrão é 0.")
@click.option("--back", default=None, help="Imagem que deseja aplicar de plano de fundo. No caso default a cor é preta.")
@click.option("--color", default=None, help="Cor do plano de fundo da Webcam. No caso default a cor é verde.")
@click.option("--h", default=640, help="Altura da janela. Por padrão 640px.")
@click.option("--w", default=480, help="Largura da janela. Por padrao 480px")
def webcam(webcam, back, color, h, w):
    SegWebCam(webcam, back, color, h, w)

chroma.add_command(image)
chroma.add_command(webcam)