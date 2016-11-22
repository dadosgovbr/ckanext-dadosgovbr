# CKANext DadosAbertos


## Requisitos

- Instalação limpa do Ubuntu 16.04
- Nenhum serviço trabalhando nas portas: 8080, 8888, 8800, 80, 5000
- Não ter o Apache2 e o NGINX previamente instalado


## Instalação CKANext DadosAbertos

\# | Command
--- | ---
1 |  `su -s /bin/bash - ckan -c ". /usr/lib/ckan/default/bin/activate && pip install -e git+https://github.com/ckan/ckanext-pages.git#egg=ckanext-pages"`
2 | `su -s /bin/bash - ckan -c ". /usr/lib/ckan/default/bin/activate && pip install -r /usr/lib/ckan/default/src/ckanext-dadosabertos/pip-requirements.txt"`
3 | `sed -i 's/dadosabertos/ /g' /etc/ckan/default/development.ini`
4 | `sed -i 's/stats text_view image_view recline_view/stats text_view image_view recline_view dadosabertos /g' /etc/ckan/default/development.ini`
5 | `su -s /bin/bash - ckan -c ". /usr/lib/ckan/default/bin/activate && cd /usr/lib/ckan/default/src/ckanext-dadosabertos && python setup.py develop"`

### Inicie o servidor

\# | Desenvolvimento (porta: 5000)
--- | ---
1 | `sudo easyckan server`

\# | Produção (porta: 80)
--- | ---
1 | `sudo easyckan deploy`


## Configuração adicional

Para o recurso do WordPress funcionar, é necessário instalar nele o plugin: [WordPress REST API](https://br.wordpress.org/plugins/rest-api/)
Depois de instalado, será necessário alterar o domínio do site em WordPress:

**Arquivo:**
`/usr/lib/ckan/default/src/ckanext-dadosabertos/ckanext/dadosabertos/plugin.py`

    # Altere o método "def wordpress_posts" para a URL do WordPress desejada:
    url = "http://SEU_WORDPRESS_AQUI/ ...
