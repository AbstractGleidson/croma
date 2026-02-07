from segmentation.exeptions import ImageNotFound, ColorNotSelected, ColorNotFound
from .segmentation import Segmentation
from .getColor import GetColor
from .utils import getPath, readColorYaml
import cv2 as openCV
import click
from pathlib import Path
import os

def segObject(imagePath:str, save:bool, verbose:bool):
    
    path = getPath(imagePath)
    
    img = openCV.imread(
        path
    )
    
    if img is None:
        raise ImageNotFound(f"Não foi possível abrir a imagem. Verifique o caminho: {path}")  
   
    col = GetColor.getColor(img)
        
    if col is None:
        raise ColorNotSelected("Nenhuma cor selecionada.")     
    
    segImage = Segmentation.segObject(img, col["min"], col["max"])
    
    #openCV.imshow("Imagem", img)
    openCV.imshow("Objeto segmentado", segImage)
    
    key = openCV.waitKey(0) & 0xFF
    
    if key == ord('q'):
        openCV.destroyAllWindows()
        
    if save:
        save_path = str(os.path.dirname(path) / Path(f"seg_{os.path.basename(path)}"))
        
        openCV.imwrite(save_path, segImage)
        
        click.echo(f"Imagem salva em: {save_path}")
   
    if verbose:
        # Mostra a cor em HSV usada na segmentacao
        click.echo("\nCor usada na segmentação em HSV: ")
        click.echo(f"\nValores minimos: ")
        click.echo(f"\thue - {col["min"][0]}\n\tsaturation - {col["min"][1]}\n\tvalue - {col["min"][2]}")
        click.echo(f"\nValores máximos: ")
        click.echo(f"\thue - {col["max"][0]}\n\tsaturation - {col["max"][1]}\n\tvalue - {col["max"][2]}")