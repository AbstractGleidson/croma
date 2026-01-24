import click
from segmentation.src.utils import getPath
from segmentation.src.getColor import GetColor
from segmentation.src.chroma.chromaImage import chromaImage
from segmentation.src.chroma.chromaWebcam import chromaWebcam
from segmentation.src.segObject import segObject
from segmentation.exeptions import ImageNotFound, ColorNotSelected, ColorNotFound, UnableOpenWebcam

@click.group(help="Ferramenta de segmentação de imagens e vídeo usando cores (chroma key, segmentação e análise HSV).")
def seg():
    pass

@click.command(
    help=
    """
        Aplica o efeito chroma key em uma imagem.

        Permite substituir o fundo de uma imagem a partir de uma cor selecionada,
        utilizando outra imagem ou uma cor sólida como plano de fundo.

        Exemplos:
        seg chroma --front pessoa.png --back fundo.jpg
        seg chroma --front pessoa.png --color green --save
    """
)

@click.option(
    "-f", "--front",
    default=None,
    type=str,
    help="Caminho para a imagem principal (foreground) que receberá o efeito."
)
@click.option(
    "-c", "--color",
    default=None,
    type=str,
    help="Cor do plano de fundo. Se não for informada, uma janela será aberta para seleção da cor."
)
@click.option(
    "-b", "--back",
    default=None,
    type=str,
    help="Caminho para a imagem de plano de fundo. Se não for informada, será utilizado fundo preto."
)
@click.option(
    "-s", "--save",
    is_flag=True,
    help="Salva a imagem resultado."
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="Exibe os parâmetros de cor usado na segmentação no espaço de cores HSV."
)
def chroma(front, back, color, save, verbose):
    
    try:
        if front is not None:
            image_path = getPath(front)
            
            back_path = back
            if back_path is not None:
                back_path = getPath(back_path)
            
            chromaImage(image_path, back_path, color, save, verbose)

        else:
            click.echo("Nenhuma imagem foi informada.\n")
            click.echo("Utilize o parâmetro --front para definir o caminho da imagem na qual o filtro será aplicado.\n")
            click.echo("Exemplo de uso:")
            click.echo("\tseg chroma --front=caminho/para/imagem.png\n")
            click.echo("Substitua 'caminho/para/imagem.png' pelo local onde sua imagem está salva.")

    except ImageNotFound as error:
        click.echo(error)
    
    except ColorNotSelected as error:
        click.echo(error)
        
    except ColorNotFound as error:
        click.echo(error)
        
        
@click.command(
    help=
    """
        Segmenta um objeto em uma imagem com base em uma cor selecionada.

        Esse comando isola regiões da imagem que correspondem à cor informada,
        gerando uma imagem segmentada.

        Exemplos:
        seg object --image objeto.png --color blue
        seg object --image objeto.png --save --verbose
    """
)

@click.option(
    "-i", "--image",
    default=None,
    type=str,
    help="Caminho para a imagem na qual o efeito será aplicado."
)
@click.option(
    "-c", "--color",
    default=None,
    type=str,
    help="Cor do plano de fundo. Se não for informada, uma janela será aberta para a escolha da cor."
)
@click.option(
    "-s", "--save",
    is_flag=True,
    help="Salva a imagem resultado."
)
@click.option(
    "-v", "--verbose",
    is_flag=True,
    help="Exibe os parâmetros de cor usado na segmentação no espaço de cores HSV."
)
def object(image, color, save, verbose):
    
    try:
        if image is not None:
            image_path = getPath(image)
            
            segObject(image_path, color, save, verbose)

        else:
            click.echo("Nenhuma imagem foi informada.\n")
            click.echo("Utilize o parâmetro --image para definir o caminho da imagem na qual o filtro será aplicado.\n")
            click.echo("Exemplo de uso:")
            click.echo("\tseg object --image=caminho/para/imagem.png\n")
            click.echo("Substitua 'caminho/para/imagem.png' pelo local onde sua imagem está salva.")
            
    except ImageNotFound as error:
        click.echo(error)
    
    except ColorNotFound as error:
        click.echo(error)
    
    except ColorNotSelected as error:
        click.echo(error)

@click.command(
    help=
    """
        Aplica o efeito chroma key em tempo real usando a webcam.

        Permite remover o fundo capturado pela câmera e substituí-lo
        por uma imagem ou por uma cor sólida.

        Exemplos:
        seg webcam
        seg webcam --webcam 0 --color green
        seg webcam --back fundo.jpg --w 800 --h 600
    """
)

@click.option(
    "--webcam",
    default=0,
    type=int,
    help="Índice da webcam a ser utilizada. Por padrão, é 0."
)
@click.option(
    "--back",
    default=None,
    type=str,
    help="Caminho para a imagem de plano de fundo. Se não for informada, será utilizado fundo preto."
)
@click.option(
    "--color",
    default=None,
    type=str,
    help="Cor do plano de fundo da webcam. Se não for informada, a cor padrão será verde."
)
@click.option(
    "--h",
    default=640,
    type=int,
    help="Altura da janela em pixels. Por padrão, 640."
)
@click.option(
    "--w",
    default=480,
    type=int,
    help="Largura da janela em pixels. Por padrão, 480."
)
def webcam(webcam, back, color, h, w):
    try:
        chromaWebcam(webcam, back, color, h, w)
    except UnableOpenWebcam as error:
        click.echo(error)
    
    except ImageNotFound as error:
        click.echo(error)
    
    except ColorNotFound as error:
        click.echo(error)
        
    
@click.command(
    help=
    """
        Realiza a leitura de uma cor em uma imagem e exibe seus valores no espaço HSV.

        Útil para descobrir os limites mínimo e máximo de uma cor
        antes de utilizá-la na segmentação ou no chroma key.

        Exemplo:
        seg color --image imagem.png
    """
)

@click.option(
    "-i", "--image",
    default=None,
    type=str,
    help="Caminho para a imagem que será utilizada para análise de cor."
)
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
        click.echo("Nenhuma imagem foi informada.\n")
        click.echo("Utilize o parâmetro --image para definir o caminho da imagem que será estudada.\n")
        click.echo("Exemplo de uso:")
        click.echo("\tseg color --image=caminho/para/imagem.png\n")
        click.echo("Substitua 'caminho/para/imagem.png' pelo local onde sua imagem está salva.")

seg.add_command(color)
seg.add_command(chroma)
seg.add_command(webcam)
seg.add_command(object)