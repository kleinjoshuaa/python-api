from __future__ import absolute_import, division, print_function, \
    unicode_literals

from identify.resources.traffic_type import TrafficType
from identify.microclients import AttributeMicroClient
from identify.microclients import IdentityMicroClient
from identify.http_clients.sync_client import SyncHttpClient
from identify.main import get_client


class TestTrafficType:
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
        tt = TrafficType(
            {
                'id': '123',
                'name': 'name',
                'displayAttributeId': 'a1'
            },
            client
        )
        from identify.resources.base_resource import BaseResource
        BaseResource.__init__.assert_called_once_with(tt, '123', client)

    def test_fetch_attributes(self, mocker):
        '''
        '''
        data = [{
            'id': 'a1',
            'trafficTypeId': '1',
            'displayName': 'dn1',
            'isSearchable': False,
            'dataType': 'string',
            'description': 'd1',
        }, {
            'id': 'a2',
            'trafficTypeId': '1',
            'displayName': 'dn2',
            'isSearchable': False,
            'dataType': 'string',
            'description': 'd2',
        }]
        http_client_mock = mocker.Mock()
        http_client_mock.make_request.return_value = data
        tt1 = TrafficType(
            {
                'id': '1',
                'displayAttributeId': 'asd',
                'name': 'n1',
            },
            http_client_mock
        )

        attrs = tt1.fetch_attributes()

        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['all_items'],
            trafficTypeId=data[0]['trafficTypeId']
        )
        assert [a.to_dict() for a in attrs] == data

        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = data
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        tt2 = TrafficType({
            'id': '1',
            'displayAttributeId': 'asd',
            'name': 'n2'
        })
        attrs = tt2.fetch_attributes(ic)
        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['all_items'],
            trafficTypeId=data[0]['trafficTypeId']
        )
        assert [a.to_dict() for a in attrs] == data

    def test_add_attribute(self, mocker):
        '''
        '''
        data = {
            'id': 'a1',
            'trafficTypeId': '1',
            'displayName': 'dn1',
            'isSearchable': False,
            'dataType': 'string',
            'description': 'd1',
        }
        http_client_mock = mocker.Mock()
        http_client_mock.make_request.return_value = data
        tt1 = TrafficType(
            {
                'id': '1',
                'displayAttributeId': 'asd',
                'name': 'n1',
            },
            http_client_mock
        )

        attr = tt1.add_attribute(data)

        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['create'],
            data,
            trafficTypeId=data['trafficTypeId'],
        )
        assert attr.to_dict() == data

        tt2 = TrafficType({
            'id': '1',
            'displayAttributeId': 'asd',
            'name': 'n2'
        })
        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = data
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        attr = tt2.add_attribute(data, ic)
        http_client_mock.make_request.assert_called_once_with(
            AttributeMicroClient._endpoint['create'],
            data,
            trafficTypeId=data['trafficTypeId'],
        )
        assert attr.to_dict() == data

    def test_add_identity(self, mocker):
        '''
        '''
        data = {
            'key': 'key1',
            'trafficTypeId': '1',
            'environmentId': '1',
            'values': {'a1': 'v1'},
            'organizationId': 'o1',
        }
        http_client_mock = mocker.Mock()
        http_client_mock.make_request.return_value = data
        tt1 = TrafficType(
            {
                'id': '1',
                'name': 'tt1',
                'displayAttributeId': '111',
            },
            http_client_mock
        )

        attr = tt1.add_identity(data)

        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create'],
            data,
            trafficTypeId=data['trafficTypeId'],
            environmentId=data['environmentId'],
            key=data['key']
        )
        assert attr.to_dict() == data

        tt2 = TrafficType(
            {
                'id': '1',
                'name': 'tt1',
                'displayAttributeId': '111',
            }
        )

        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = data
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        attr = tt2.add_identity(data, ic)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create'],
            data,
            trafficTypeId=data['trafficTypeId'],
            environmentId=data['environmentId'],
            key=data['key']
        )
        assert attr.to_dict() == data

    def test_add_identities(self, mocker):
        '''
        '''
        data = [{
            'key': 'key1',
            'trafficTypeId': '1',
            'environmentId': '1',
            'values': {'a1': 'v1'},
            'organizationId': 'o1',
        }, {
            'key': 'key2',
            'trafficTypeId': '1',
            'environmentId': '1',
            'values': {'a2': 'v2'},
            'organizationId': 'o1',
        }]

        http_client_mock = mocker.Mock()
        http_client_mock.make_request.return_value = {
            'objects': data,
            'failed': [],
            'metadata': {}
        }
        tt1 = TrafficType(
            {
                'id': '1',
                'name': 'tt1',
                'displayAttributeId': '111'
            },
            http_client_mock
        )

        s1, f1 = tt1.add_identities(data)

        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create_many'],
            data,
            trafficTypeId=data[0]['trafficTypeId'],
            environmentId=data[0]['environmentId'],
        )
        assert [s.to_dict() for s in s1] == data

        tt2 = TrafficType({
            'id': '1',
            'name': 'tt1',
            'displayAttributeId': '111'
        })

        mocker.patch('identify.http_clients.sync_client.SyncHttpClient.make_request')
        SyncHttpClient.make_request.return_value = {
            'objects': data,
            'failed': [],
            'metadata': {}
        }
        ic = get_client({'base_url': 'http://test', 'apikey': '123'})
        s2, f2 = tt2.add_identities(data, ic)
        http_client_mock.make_request.assert_called_once_with(
            IdentityMicroClient._endpoint['create_many'],
            data,
            trafficTypeId=data[0]['trafficTypeId'],
            environmentId=data[0]['environmentId'],
        )
        assert [s.to_dict() for s in s2] == data

#    def test_add_identity(self, mocker):
#        '''
#        '''
#        data = {
#            'key': 'key1',
#            'trafficTypeId': '1',
#            'environmentId': '1',
#            'values': {'a1': 'v1'},
#            'organizationId': 'o1',
#        }
#        http_client_mock = mocker.Mock()
#        http_client_mock.make_request.return_value = data
#        tt1 = TrafficType(
#            {
#                'id': '1',
#                'displayAttributeId': 'asd',
#                'name': 'n1',
#            },
#            http_client_mock
#        )
#
#        attr = tt1.add_identity(data)
#
#        http_client_mock.make_request.assert_called_once_with(
#            IdentityMicroClient._endpoint['create'],
#            data,
#            trafficTypeId=data['trafficTypeId'],
#            environmentId=data['environmentId'],
#            key=data['key']
#        )
#        assert attr.to_dict() == data
#
#        http_client_mock.reset_mock()
#        tt2 = TrafficType(
#            {
#                'id': '1',
#                'displayAttributeId': 'asd',
#                'name': 'n1',
#            },
#        )
#
#        attr = tt2.add_identity(data, IdentityMicroClient(http_client_mock))
#        http_client_mock.make_request.assert_called_once_with(
#            IdentityMicroClient._endpoint['create'],
#            data,
#            trafficTypeId=data['trafficTypeId'],
#            environmentId=data['environmentId'],
#            key=data['key']
#        )
#        assert attr.to_dict() == data
#
#    def test_add_identities(self, mocker):
#        '''
#        '''
#        data = [{
#            'key': 'key1',
#            'trafficTypeId': '1',
#            'environmentId': '1',
#            'values': {'a1': 'v1'},
#            'organizationId': 'o1',
#        }, {
#            'key': 'key2',
#            'trafficTypeId': '1',
#            'environmentId': '1',
#            'values': {'a2': 'v2'},
#            'organizationId': 'o1',
#        }]
#
#        http_client_mock = mocker.Mock()
#        http_client_mock.make_request.return_value = {
#            'objects': data,
#            'failed': [],
#            'metadata': {}
#        }
#        tt1 = TrafficType(
#            {
#                'id': '1',
#                'displayAttributeId': 'asd',
#                'name': 'n1',
#            },
#            http_client_mock
#        )
#
#        s1, f1 = tt1.add_identities(data)
#
#        http_client_mock.make_request.assert_called_once_with(
#            IdentityMicroClient._endpoint['create_many'],
#            data,
#            trafficTypeId=data[0]['trafficTypeId'],
#            environmentId=data[0]['environmentId'],
#        )
#        assert [s.to_dict() for s in s1] == data
#
#        http_client_mock.reset_mock()
#        tt2 = TrafficType(
#            {
#                'id': '1',
#                'displayAttributeId': 'asd',
#                'name': 'n1',
#            },
#        )
#
#        s2, f2 = tt2.add_identities(data, IdentityMicroClient(http_client_mock))
#        http_client_mock.make_request.assert_called_once_with(
#            IdentityMicroClient._endpoint['create_many'],
#            data,
#            trafficTypeId=data[0]['trafficTypeId'],
#            environmentId=data[0]['environmentId'],
#        )
#        assert [s.to_dict() for s in s2] == data
