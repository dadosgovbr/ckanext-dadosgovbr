import os
from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer
import ckan.plugins.toolkit

class DadosGovBrTheme(SingletonPlugin):
    '''The theme for the dados.gov.br site.

    Uses CKAN's IConfigurer plugin interface to override some of CKAN's
    default files and templates with files and templates from this extension
    package.

    '''
    implements(IConfigurer, inherit=True)

    def update_config(self, config):
        '''This IConfigurer implementation causes CKAN to look in the
        ```public``` and ```templates``` directories present in this package
        for any customisations.

        It also shows how to set the site title here (rather than in the main
        site .ini file).

        '''
        # Setup some variable that will be useful below.
        here = os.path.dirname(__file__)
        rootdir = os.path.dirname(os.path.dirname(here))
        our_public_dir = os.path.join(rootdir, 'ckanext', 'dadosgovbr',
                'public')
        template_dir = os.path.join(rootdir, 'ckanext', 'dadosgovbr',
                'templates')
        
        # use new style plugin toolkit
        ckan.plugins.toolkit.add_public_directory(config, 'public')
        ckan.plugins.toolkit.add_resource('public/css', 'application.css')

        # Configure our public and templates overrides.
        config['extra_public_paths'] = ','.join([our_public_dir,
                config.get('extra_public_paths', '')])
        config['extra_template_paths'] = ','.join([template_dir,
                config.get('extra_template_paths', '')])

