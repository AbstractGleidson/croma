import click
from chroma.utils.utils import getPath
from chroma.utils.getColor import GetColor
from .core import SegImage, SegWebCam

@click.group()
def chroma():
    pass

@click.command()
@click.option("--front", default=None, help="Caminho da imagem que deseja aplicar o efeito.")
@click.option("--color", default=None, help="Cor do plano de fudo da imagem. No caso default abre uma janela pra escolha da cor.")
@click.option("--back", default=None, help="Imagem que deseja aplicar de plano de fundo. No caso default a cor é preta.")
def image(front, back, color):
    
    if front is not None:
        image_path = getPath(front)
        
        back_path = back
        if back_path is not None:
            back_path = getPath(back_path)
        
        SegImage(image_path, back_path, color)

    else:
        click.echo("Utilize o parâmetro --image para definir o caminho da image para aplicar o filtro")
        click.echo("exemplo: ")
        click.echo("\n\tchrome image --image=path\n")
        click.echo("path deve ser o caminho onde está a sua imagem.")

@click.command()
@click.option("--webcam", default=0, help="Index da webcam. Por padrão é 0.")
@click.option("--back", default=None, help="Imagem que deseja aplicar de plano de fundo. No caso default a cor é preta.")
@click.option("--color", default=None, help="Cor do plano de fundo da Webcam. No caso default a cor é verde.")
@click.option("--h", default=640, help="Altura da janela. Por padrão 640px.")
@click.option("--w", default=480, help="Largura da janela. Por padrao 480px")
def webcam(webcam, back, color, h, w):
    SegWebCam(webcam, back, color, h, w)
    
@click.command()
@click.option("--image", default=None, help="Imagem para estudar a cor.")
def color(image):
    
    if image is not None:
        color = GetColor.getColor(
            getPath(image)
        )
        
        if color is not None:
            click.echo("A cor lidar na escala HSV foi: ")
            click.echo(f"\nValores minimos: ")
            click.echo(f"\thue - {color["min"][0]}\n\tsaturation - {color["min"][1]}\n\tvalue - {color["min"][2]}")
            click.echo(f"\nValores máximos: ")
            click.echo(f"\thue - {color["max"][0]}\n\tsaturation - {color["max"][1]}\n\tvalue - {color["max"][2]}")
        else:
            click.echo("Você não selecionou nenhuma cor.")
        
        
    else:
        click.echo("Utilize o parâmetro --image para definir o caminho da image para estudar a cor.")
        click.echo("exemplo: ")
        click.echo("\n\tchrome color --image=path\n")
        click.echo("path deve ser o caminho onde está a sua imagem.")

@click.command()
def hello():
    click.echo("\nChroma funcionando!")
    click.echo("Teste: ")
    click.echo("\n\tchroma color --image=path")
    click.echo("\npath deve ser o caminho onde está a sua imagem.")

chroma.add_command(hello)
chroma.add_command(color)
chroma.add_command(image)
chroma.add_command(webcam)