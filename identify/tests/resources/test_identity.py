from __future__ import absolute_import, division, print_function, \
    unicode_literals

from identify.http_clients.sync_client import SyncHttpClient
from identify.resources.identity import Identity
from identify.microclients import IdentityMicroClient
from identify.main import get_client

class TestIdentity:
    '''
    Tests for the TrafficType class' methods
    '''
    def test_constructor(self, mocker):
        '''
        '''
        client = object()
        mock_init = mocker.Mock()
        mocker.patch(
            'identify.resources.base_resource.BaseResource.__init__',
            new=mock_init
        )
        identity = Identity(
            {
                'key': 'key',
                'trafficTypeId': 'ttid',
                'enironmentId': 'envid',
                'values': 'vals'
            },
            client
        )
        from identify.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(identity, None, client)

    def test_save(self, mocker):
        '''
        '''
        http_client_mock = mocker.Mock()
        i1 = Identity(
            {
                'key': 'key1',
                'trafficTypeId': '1',
                'environmentId': '1',
                'values': {'a1': 'v1'},
                'organizationId': 'o1'
            },
            http_client_mock
        )
        http_client_mock.make_request.return_value = i1.to_dict()

        res = i1.save()

        http_client_mock.make_request.assert_called_once_with(
           IdentityMicroClient._endpoint['create'],
            i1.to_dict(),
            trafficTypeId=i1.traffic_type_id,
            environmentId=i1.environment_id,
            key=i1.key
        )

        assert res.to_dict() == i1.to_dict()

        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = i1.to_dict()
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        i2 = Identity(i1.to_dict())
        res = i2.save(ic)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create'],
            i1.to_dict(),
            trafficTypeId=i2.traffic_type_id,
            environmentId=i2.environment_id,
            key=i2.key
        )
        assert res.to_dict() == i2.to_dict()

    def test_update(self, mocker):
        '''
        '''
        http_client_mock = mocker.Mock()
        i1 = Identity(
            {
                'key': 'key1',
                'trafficTypeId': '1',
                'environmentId': '1',
                'values': {'a1': 'v1'},
                'organizationId': 'o1'
            },
            http_client_mock
        )
        http_client_mock.make_request.return_value = i1.to_dict()

        res = i1.update()

        http_client_mock.make_request.assert_called_once_with(
           IdentityMicroClient._endpoint['update'],
            i1.to_dict(),
            trafficTypeId=i1.traffic_type_id,
            environmentId=i1.environment_id,
            key=i1.key
        )

        assert res.to_dict() == i1.to_dict()

        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = i1.to_dict()
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        i2 = Identity(i1.to_dict())
        res = i2.update(ic)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['update'],
            i1.to_dict(),
            trafficTypeId=i2.traffic_type_id,
            environmentId=i2.environment_id,
            key=i2.key
        )
        assert res.to_dict() == i2.to_dict()

    def test_delete_attributes(self, mocker):
        '''
        '''
        http_client_mock = mocker.Mock()
        i1 = Identity(
            {
                'key': 'key1',
                'trafficTypeId': '1',
                'environmentId': '1',
                'values': {'a1': 'v1'},
                'organizationId': 'o1'
            },
            http_client_mock
        )
        http_client_mock.make_request.return_value = None

        res = i1.delete_attributes()

        http_client_mock.make_request.assert_called_once_with(
           IdentityMicroClient._endpoint['delete_attributes'],
            trafficTypeId=i1.traffic_type_id,
            environmentId=i1.environment_id,
            key=i1.key
        )

        assert res is None

        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = None
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        i2 = Identity(i1.to_dict())
        res = i2.delete_attributes(ic)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['delete_attributes'],
            trafficTypeId=i2.traffic_type_id,
            environmentId=i2.environment_id,
            key=i2.key
        )
        assert res is None
