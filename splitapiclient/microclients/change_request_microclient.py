from splitapiclient.resources import ChangeRequest
from splitapiclient.util.exceptions import HTTPResponseError, \
    UnknownApiClientError
from splitapiclient.util.logger import LOGGER
from splitapiclient.util.helpers import as_dict

class ChangeRequestMicroClient:
    '''
    '''
    _endpoint = {
        'list_initial': {
            'method': 'GET',
            'url_template': 'changeRequests?limit=100&environmentId={environmentId}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },     
        'list_initial_all_environments': {
            'method': 'GET',
            'url_template': 'changeRequests?limit=100',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'list_next': {
            'method': 'GET',
            'url_template': 'changeRequests?limit=100&after={after}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'list_next_all_environments': {
            'method': 'GET',
            'url_template': 'changeRequests?limit=100&environmentId={environmentId}&after={after}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'update_status': {
            'method': 'PUT',
            'url_template': 'changeRequests/{changeRequestId}',
            'headers': [{
                'name': 'Authorization',
                'template': 'Bearer {value}',
                'required': True,
            }],
            'query_string': [],
            'response': True,
        },
        'submit_change_request': {
            'method': 'POST',
            'url_template': 'changeRequests/ws/{workspaceId}/environments/{environmentId}',
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

    def list(self, environment_id):
        '''
        Returns a list of change request objects.

        :returns: list of Change request objects
        :rtype: list(ChangeRequest)
        '''
        final_list = []
        afterMarker = 0
        while True:
            if afterMarker==0 and environment_id!=None:
                response = self._http_client.make_request(
                    self._endpoint['list_initial'],
                    environmentId = environment_id
                )
            elif afterMarker==0 and environment_id==None:
                response = self._http_client.make_request(
                    self._endpoint['list_initial_all_environments'],
                ) 
            elif environment_id==None:
                response = self._http_client.make_request(
                    self._endpoint['list_next_all_environments'],
                    after = afterMarker
                )
            else:
                response = self._http_client.make_request(
                    self._endpoint['list_next'],
                    after = afterMarker
                )
            for item in response['data']:
                final_list.append(as_dict(item))
            if response['nextMarker'] is None:
                break
            else:
                afterMarker = response['nextMarker']
                continue
        return [ChangeRequest(item,  self._http_client) for item in final_list]

    def find(self, split_name=None, segment_name=None, environment_id=None):
        '''
        Find Change requests for optional environment, split name or segment name objects.

        :returns: list of change request objects
        :rtype: list(ChangeRequest)
        '''
        final_list = []
        for item in self.list(environment_id):
            if item._split != None:
                if item._split['name'] == split_name:
                    final_list.append(item)
            if item._segment != None:
                if item._segment['name'] == segment_name:
                    final_list.append(item)
        return final_list

    def update_status(self, change_request_id, new_status, comment):
        '''
        Update a change request status

        :returns: Updated Change request objects
        :rtype: ChangeRequest
        '''
        data = {
            'status': new_status,
            'comment': comment
        }
        response = self._http_client.make_request(
            self._endpoint['update_status'],
            changeRequestId = change_request_id,
            body = data
        )
        return ChangeRequest(response, self._http_client)

    def submit_change_request(self, environment_id, workspace_id, data):
        '''
        Submit a split definition change request

        :returns: Change request objects
        :rtype: ChangeRequest
        '''
        response = self._http_client.make_request(
            self._endpoint['submit_change_request'],
            environmentId = environment_id,
            workspaceId = workspace_id,
            body = data
        )
        return ChangeRequest(response, self._http_client)

