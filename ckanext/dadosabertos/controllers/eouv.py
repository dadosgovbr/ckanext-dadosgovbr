# -*- coding: utf-8 -*-

import ckan.plugins as p
import urllib2
from ckan.lib.base import c, g, h, render, model
import ckan.lib.base as base
from pylons import request, response
from pylons.controllers.util import redirect
import requests

from ckan.common import OrderedDict, config

''' Integração com a Ouvidoria do Governo Federal Brasileiro

Para cada "organization", é necessário adicionar o atributo "siorg"
com o código do órgão correspondente.

É necessário adicionar no "production.ini" as seguintes linhas:

## E-Ouv
eouv.url  = http://URL_DA_OUVIDORIA_AQUI.gov.br
eouv.user = USUARIO_AQUI
eouv.pass = SENHA_AQUI

'''

class EouvController(base.BaseController):
    def simple(self):
        return 'mensagem de teste'
    
    def check_package_eouv(self, package_id):
        ''' Cria tupla do eouv no package_extra se não existir.
            
            @params package_id
        '''

        # Para adcionar as tuplas com os contadores de like de dislike é necessário ter o banco eouv
        # nesta etapa verificamos se esta tabela existe e se não existir criamos ela

        query_revision = "select exists (select * from pg_tables where tablename = 'eouv') as exist"
        result_exist_table_eouv = model.Session.execute(query_revision)

        for row in result_exist_table_eouv:
            exist_table_eouv = row['exist']

        if not(exist_table_eouv):
            sql = "create table eouv (package_id text primary key, nro_like text, nro_dislike text, FOREIGN KEY (package_id) REFERENCES public.package (id))"
            model.Session.execute(sql)
            model.Session.commit()

        #Consulta no banco se existe a tupla com os contador de like e dislike em package_extra
        query_posit = "SELECT EXISTS (SELECT 1 FROM eouv WHERE package_id = '"+str(package_id)+"') as positivo"

        exist_tupla_positiva = model.Session.execute(query_posit)

        for row in exist_tupla_positiva:
            exist_tuple = row['positivo']
        
        #Verifica se existe a tupla, se não houver, ele cria
        if not(exist_tuple):
            sql = "insert into eouv values ('"+str(package_id)+"', '0', '0')"
            model.Session.execute(sql)
            model.Session.commit()

        pass


    def vote(self, acao, package_id):
        '''
         Acao devera ser 1 para incrementar 1 no contador de likes
         Acao devera ser -1 para incrementar 1 no contador de dislike
        ''' 
        self.check_package_eouv(package_id)

        #Incrementa um nos likes em eouv
        if (acao == 1):
            query_nro_like = "SELECT nro_like FROM eouv WHERE package_id = '"+str(package_id)+"'"
            num_like_array = model.Session.execute(query_nro_like)

            for row in num_like_array:
                nro_likes = row['nro_like']
            
            nro_likes = int(nro_likes) + 1

            query_update_like = "UPDATE eouv SET nro_like = "+str(nro_likes)+" WHERE package_id = '"+str(package_id)+"'"
            model.Session.execute(query_update_like)
            model.Session.commit()
        
        #Incrementa um nos dislikes em eouv
        if (acao == -1):
            query_nro_dislike = "SELECT nro_dislike FROM eouv WHERE package_id = '"+str(package_id)+"'"
            num_dislike_array = model.Session.execute(query_nro_dislike)

            for row in num_dislike_array:
                nro_dislikes = row['nro_dislike']
            
            nro_dislikes = int(nro_dislikes) + 1

            query_update_like = "UPDATE eouv SET nro_dislike = "+str(nro_dislikes)+" WHERE package_id = '"+str(package_id)+"'"
            model.Session.execute(query_update_like)
            model.Session.commit()
        return

    def helper_get_contador_eouv (self, package_id):

        query_nro_dislike = "SELECT nro_like, nro_dislike FROM eouv WHERE package_id = '"+str(package_id)+"'"    
        num_dislike_array = model.Session.execute(query_nro_dislike)

        out = {}
        
        for row in num_dislike_array:
            out['nro_dislikes'] = row['nro_dislike']
            out['nro_likes'] = row['nro_like']
    
        return out

    def new_positive (self):
        package_id = request.POST['package_id'].encode('utf-8')
        self.vote(1, package_id)
        return '{"success": true}'


    def new_negative (self):
        ''' Avaliação negativa

            - Submete requisição para a ouvidoria do governo.
            - TODO Incrementa contador de avaliações negativas no dataset
        '''

        # Obtém parâmetros do POST
        package_id          = request.POST['package_id'].encode('utf-8')
        siorg               = request.POST['siorg'].encode('utf-8')
        text                = request.POST['text'].encode('utf-8')
        name                = request.POST['name'].encode('utf-8')
        email               = request.POST['email'].encode('utf-8')
        #receber_email       = request.POST['receber_email'].encode('utf-8')

        # Cabeçalho dados.gov.br
        cabecalho = "Trata-se de manifestação registrada por cidadão no Portal Brasileiro de Dados Abertos(dados.gov.br).\n\n"

        # Obtém informações do package
        from ckan.logic import get_action
        context = {'model': model, 'session': model.Session,
                'user': c.user or c.author}
        data_dict = {'id': package_id}
        package  = get_action('package_show')(context, data_dict)

        # Adiciona dados do package
        package_info  = 'Conjunto de Dados: '+str(package['title'].encode('utf-8'))+"\n"
        package_info += 'Link: http://dados.gov.br/dataset/'+str(package['id'].encode('utf-8'))+"\n"
        package_info += 'Link alternativo: http://dados.gov.br/dataset/'+str(package['name'].encode('utf-8'))+"\n\n"

        # Preenche o texto de envio
        text = cabecalho + package_info + text
        
        # DEBUG
        # import pprint
        # pprint.pprint(package['title'])
        # pprint.pprint(request.POST)
        # return ""

        # Contabiliza voto negativo
        self.vote(-1, package_id)

        # Set header for XML content
        response.headers['Content-Type'] = (b'text/xml; charset=utf-8')

        # Envia requisição anônima
        if(len(email) == 0):
            ouvidoria_response = self.send_request(siorg, 1, text)

        # Envia requisição não-anônima
        else:
            receber_email      = 1 # FIXADO A PEDIDO DO MP
            ouvidoria_response = self.send_request(siorg, 1, text, email, name, receber_email)

        # Retorna para protocolo ou erro para o JS
        return ouvidoria_response




    def send_request (
        self,
        idOrgaoDestinatario,
        idAssunto,
        textoManifestacao,
        email='',
        nomeManifestante='',
        enviarEmailCidadao='0',
        idTipoManifestacao='2'
    ):
        dadosPessoais = ''

        # Se a manifestação for anônima
        if (len(email)==0):
            idTipoIdentificacaoManifestante = '1'
        
        # Se não for anônima, terá dados pessoais
        else:
            idTipoIdentificacaoManifestante = '3'
            dadosPessoais += "<nomeManifestante>{p_nomeManifestante}</nomeManifestante>"
            dadosPessoais += "<email>{p_email}</email>"
            dadosPessoais += "<enviarEmailCidadao>{p_enviarEmailCidadao}</enviarEmailCidadao>\n"
            dadosPessoais = dadosPessoais.format(
                p_nomeManifestante = str(nomeManifestante),
                p_email = str(email),
                p_enviarEmailCidadao = str(enviarEmailCidadao)
            )
        
        # Acesso dos arquivos de configuração
        base_url = config['eouv.url']
        login    = config['eouv.user']
        senha    = config['eouv.pass']

        # URL de produção
        prod_url = 'http://sistema.ouvidorias.gov.br'

        # Destino (deve vir do arquivo de configurações!!!)
        url = base_url+"/Servicos/ServicoManterManifestacao.svc/v1"

        headers = {'content-type': 'text/xml', 'SOAPAction': 'http://sistema.ouvidorias.gov.br/servicos/ServicoManterManifestacao:v1/ServicoManterManifestacao/RegistrarManifestacaoTerceiro'}
        xml = """<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
            <Body>
                <RegistrarManifestacaoTerceiro xmlns="http://sistema.ouvidorias.gov.br/servicos/ServicoManterManifestacao:v1">
                    <login>{p_login}</login>
                    <senha>{p_senha}</senha>

                    <idTipoManifestacao>{p_idTipoManifestacao}</idTipoManifestacao>
                    <idOrgaoDestinatario>{p_idOrgaoDestinatario}</idOrgaoDestinatario>
                    <idAssunto>254</idAssunto>
                    <idCanalEntrada>1</idCanalEntrada>
                    <textoManifestacao>{p_textoManifestacao}</textoManifestacao>

                    {p_dadosPessoais}

                    <idTipoIdentificacaoManifestante>{p_idTipoIdentificacaoManifestante}</idTipoIdentificacaoManifestante>

                    
                </RegistrarManifestacaoTerceiro>
            </Body>
            </Envelope>"""
        
        # Adicionando variáveis
        xml = xml.format(
            p_login = str(login),
            p_senha = str(senha),
            p_idTipoManifestacao = str(idTipoManifestacao),
            p_idOrgaoDestinatario = str(idOrgaoDestinatario),
            p_textoManifestacao = str(textoManifestacao),
            p_dadosPessoais = str(dadosPessoais),
            p_idTipoIdentificacaoManifestante = str(idTipoIdentificacaoManifestante)
        )

        # DEBUG
        # return xml
        
        # Faz requisição à ouvidoria
        response = requests.post(url,data=xml, headers = headers)

        # Se o cadastro na ouvidoria ocorreu com sucesso
        if(response.status_code == 200):
            # TODO implementar persistência em banco
            pass
        
        # Retorna resposta com o número de protocolo
        return response.content  #protocolo
        
