from modeledclient import ModeledClient


class CachedClient(ModeledClient):
    def __init__(self, model):
        """A client that caches previous requests and responses for reuse

        :type model: dict
        :param model: The a loaded JSON model representing the API
        """
        super(CachedClient, self).__init__(model)
        # Create an empty dictionary to initialize the cache.
        self._operation_cache = {}

    @property
    def history(self):
        return self._operation_cache

    def make_modeled_api_call(self, method, *args, **kwargs):
        # Create a key for the cache that consists of the methods and
        # the various args provided.
        cache_key = '%s(args=%s,kwargs=%s)' % (method, args, kwargs)
        # If the key is in the cache then use that stored result.
        if cache_key in self._operation_cache:
            print('Retrieving result from history')
            return self._operation_cache[cache_key]
        # If the key is not in the cache then make an API call and store
        # it for future use.
        else:
            print('Retrieving result from server')
            result = super(CachedClient, self).make_modeled_api_call(
                method, *args, **kwargs)
            self._operation_cache[cache_key] = result
            return result
