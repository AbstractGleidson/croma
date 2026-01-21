# Modulo Chroma 
Modulo para a experimentação da modalidade de segmentação por cor, fornece métodos simples de segmentação por cor. Entretanto, o diferencial é ser uma ferramenta de linha de comando que dispõe de uma ferramenta de leitura de cor intuitiva e que fornece o resultado dessa leitura de forma imediata. 

# image
```bash
chroma image --front=path --back=path --color=color
```

# webcam

```bash
chroma webcam --back=path --color=color
```

# color 
```bash
chroma color --image=path
```

# Instalação

```
git clone "https://github.com/AbstractGleidson/croma.git"

cd croma 

python -m venv .env

pip install -e .

cd ..

chroma hello
```