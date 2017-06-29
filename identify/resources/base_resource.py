from __future__ import absolute_import, division, print_function, \
    unicode_literals
import abc
import six
from identify.util import validation
from identify.util.logger import LOGGER
from identify.util import camelcase
from identify.util.exceptions import UnknownIdentifyClientError


class BaseResource(six.with_metaclass(abc.ABCMeta)):
    '''
    Abstract class to handle resources uniformely.
    '''

    def __init__(self, id, client=None):
        '''
        Constructs (a child) resource instance (called via super or __init__,
        stores the id and client.

        :param id: string. Resource Id.
        :param client: HTTP client that will be used to make API calls.
        '''
        self._id = id
        self._client = client

    @property
    def id(self):
        return self._id

    @abc.abstractproperty
    def _schema(self):
        pass

    @classmethod
    def _validate(cls, response_item):
        '''
        This method validates that the schema from an object returned by the API
        matches the schema defined for the requested resource, defined in the
        child class.

        :param response_item: dict. Single item to verify.
        '''
        return all(
            validation.is_correct_type(value, cls._schema.get(key))
            for key, value in six.iteritems(response_item)
        )

    def to_dict(self):
        '''
        Returns a dictionary with the property names in camelCase, in compliance
        with the Identify backend
        '''
        try:
            temp = {
                attribute: getattr(
                    self, camelcase.to_underscore(attribute),
                    None
                ) for attribute in self._schema
            }
            return temp
        except Exception as e:
            LOGGER.debug(e)
            raise UnknownIdentifyClientError
