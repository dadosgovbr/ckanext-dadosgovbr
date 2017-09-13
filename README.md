# ckanext-dadosgovbr
Plugin / Tema do Portal de Dados Abertos do Governo Federal - Brasil

## Requisitos

- CKAN 2.5.x / 2.6.x
- Um grupo criado com o "name" igual a "dados-em-destaque"
- Plugin: ckanext-scheming


## Instalação ckanext-dadosgovbr

Ative o virtualenv:
```
# Entre no usuário onde o CKAN foi instalado
su ckan

# Ative o virtualenv
. /usr/lib/ckan/default/bin/activate 

# Acesse o diretório de plugins
cd /usr/lib/ckan/default/src
```

Instale o ckanext-dadosgovbr e as dependências:
```
# Instale o ckanext-dadosgovbr (última versão Beta)
pip install -e git+https://github.com/dadosgovbr/ckanext-dadosgovbr.git@beta#egg=ckanext-dadosgovbr

# Instale as dependências
pip install -r /usr/lib/ckan/default/src/ckanext-dadosgovbr/pip-requirements.txt

# Configure o plugin
cd /usr/lib/ckan/default/src/ckanext-dadosgovbr && python setup.py develop
```


## Configuração adicional

### Wordpress
- O Wordpress precisa estar na versão 4.7 ou superior.
- O plugin [WP-API/rest-filter](https://github.com/WP-API/rest-filter) precisa estar instalado e ativado no Wordpress.
- Adicione a URL do seu Wordpress em "get_domain()" no arquivo `/usr/lib/ckan/default/src/ckanext-dadosgovbr/ckanext/dadosgovbr/helpers/wordpress.py`

### Scheming
Adicione no arquivo `/etc/ckan/default/development.ini` as seguintes linhas, abaixo da definição dos plugins:
```
scheming.dataset_schemas = ckanext.dadosgovbr:schema_aplicativo.json
			   ckanext.dadosgovbr:schema_inventario.json
			   ckanext.dadosgovbr:schema_concurso.json
```
