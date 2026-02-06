from pathlib import Path
import yaml

PATH_ASSETS = Path(__file__).parent.parent / "config"
PATH_HOME = Path.home() 
PATH_COLORS = PATH_ASSETS / "colors.yaml"

def hsvToOpenCV(hue:int, saturation:int, value:int):
    """
    Converte valores HSV de ângulos e porcentagens para valores equivalente reconhecidos pela lib openCV
    
    Args:
        hue (int): ângulo do matiz
        saturation (int): porcetagem de saturação
        value (int): porcetagem de brilho

    Returns:
        _type_: tupla com os parametros em HSV para o openCV
    """
    
    n_hue = hue // 2
    n_saturation = int((saturation / 100) * 255)
    n_value = int((value / 100) * 255)
    
    return (n_hue, n_saturation, n_value)

def getPath(path:str):
    return str(PATH_HOME / path)

def readColorYaml(color:str):
    
    with open(PATH_COLORS, "r") as file:
        
        config = yaml.safe_load(file)
        return config.get(color)