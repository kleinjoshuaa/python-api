from splitapiclient.resources import Environment
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER

class EnvironmentMicroClient:
    '''
    '''
    _endpoint = {
        'all_items': {
            'method': 'GET',
            'url_template': 'environments/ws/{workspaceId}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
    }

    def __init__(self, http_client):
        '''
        Constructor
        '''
        self._http_client = http_client

    def list(self, workspace_id):
        '''
        Returns a list of Environment objects.

        :returns: list of Environment objects
        :rtype: list(Environment)
        '''
        response = self._http_client.make_request(
            self._endpoint['all_items'],
            workspaceId =workspace_id
        )
        return [Environment(item, self._http_client) for item in response]
