## Organização do Projeto

O código do primeiro e do segundo exercício estão na pasta com caminho: src/   
A documentação está na mesma pasta em formato notebook jupyther com nome: notebook.ipynb

Você pode rodar o notebook Jupyter diretamente com o comando:

    jupyter notebook

Ou utilizando a extensão do VSCode ou da sua IDE em questão.

## Pré-requisitos

Antes de rodar o projeto, é recomendado criar um ambiente virtual para gerenciar as dependências do Python de forma isolada.
### Criando um ambiente virtual

Se ainda não tiver o virtualenv instalado, você pode instalá-lo com o seguinte comando:

    pip install virtualenv

Agora, crie e ative o ambiente virtual. Execute o comando abaixo para criar o ambiente:

    virtualenv .venv

Depois de criar o ambiente, ative-o com o comando:

    source .venv/bin/activate

### Instalando dependências

Com o ambiente virtual ativado, instale as dependências do projeto utilizando o arquivo requirements.txt.

Para isso, execute o seguinte comando:

    pip install -r requirements.txt

Após a instalação, todas as dependências necessárias estarão disponíveis para rodar o projeto.
