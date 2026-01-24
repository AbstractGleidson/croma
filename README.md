# Módulo Segmentation
O módulo Segmentation é uma ferramenta voltada para experimentação de técnicas de segmentação por cor, permitindo isolar objetos, aplicar chroma key e analisar cores em imagens e vídeo.

# Funcionalidades

- Chroma key em imagens

- Chroma key em tempo real (webcam)

- Segmentação de objetos por cor

- Leitura de cor (HSV) a partir de imagens


# chroma
Aplica o efeito chroma key em uma imagem, removendo uma cor específica e substituindo por um fundo.

```bash
seg chroma --front=path --back=path --color=color
```

Parâmetros principais:

- ``--front``: imagem principal
- ``--back``: imagem de fundo (opcional)
- ``--color``: cor a ser removida (opcional)


# object
Segmenta um objeto em uma imagem com base em uma cor selecionada.

```bash
seg object --image=path --color=color
```
Esse comando é utilizado para isolar regiões da imagem que correspondem à cor informada.

# webcam 
Aplica o efeito chroma key em tempo real utilizando a webcam.
```bash
seg webcam --back=path --color=color
```
Permite substituir o fundo capturado pela câmera por uma imagem ou por uma cor sólida.

# Color 
Realiza a leitura de uma cor em uma imagem e exibe os valores no espaço de cores HSV.

```
seg color --image=path
```


# Instalação

```
git clone "https://github.com/AbstractGleidson/croma.git"

cd croma 

python -m venv .env

# Linux/Mac
source .env/bin/activate

# Windows
.env\Scripts\activate

pip install -e .

seg --help
```