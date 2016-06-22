import six

from simpleclient import Client


class ModeledClient(Client):
    def __init__(self, model):
        """A client with input validation and output parsing

        :type model: dict
        :param model: A loaded JSON model representing an API
        """
        self._model = model
        self._validator = RequestParamsValidator()
        self._parser = ResponseParamsParser()
        super(ModeledClient, self).__init__(model['endpoint_url'])

    def make_modeled_api_call(self, method, *args, **kwargs):
        # Validate the parameters provided for the particular method using the
        # provided model.
        validated_params = self._validate_method_params(
            method, *args, **kwargs)
        # Make the API call and get the response.
        api_response = self.make_api_call(method, validated_params)
        # Parse the response for the particular method using the provided
        # model.
        return self._parse_api_response(method, api_response)

    def _validate_method_params(self, method, *args, **kwargs):
        # Get the input model for the operation.
        operation_input_model = self._get_operation_model(method)['input']
        # Use the input model and the validator to validate the provided
        # parameters.
        return self._validator.validate(operation_input_model, *args, **kwargs)

    def _parse_api_response(self, method, api_response):
        # Get the output model for the operation.
        operation_output_model = self._get_operation_model(method)['output']
        # Use the output model and the parser to correctly parse the response.
        return self._parser.parse(
            operation_output_model, api_response)

    def _get_operation_model(self, method):
        operation_models = self._model['operations']
        if method not in operation_models:
            raise RuntimeError(
                'Unknown operation %s' % method)
        return operation_models[method]


class RequestParamsValidator(object):
    def validate(self, operation_input_model, *args, **kwargs):
        """Validate based on an operation model

        :type operation_input_model: dict
        :param operation_input_model: The loaded JSON model for the input
            of an operation.
        """
        if args and kwargs:
            raise RuntimeError(
                'Only positional args or keyword args can be provided, '
                'Not both.')
        client_params = kwargs
        if args:
            client_params = list(args)
        self._validate(operation_input_model, client_params)
        return client_params

    def _validate(self, model, params):
        input_type = model['type']
        # Using the type proxy out to the appropriate validate method for that
        # type.
        getattr(self, '_validate_' + input_type)(model, params)

    def _validate_structure(self, model, params):
        member_models = model['members']
        self._validate_type(params, dict)
        for param_name, param_value in params.items():
            if param_name not in member_models:
                raise RuntimeError(
                    'Got unexpected parameter %s.' % param_name)
            self._validate(member_models[param_name], param_value)

    def _validate_list(self, model, params):
        member_model = model['members']
        self._validate_type(params, list)
        for param in params:
            self._validate(member_model, param)

    def _validate_string(self, model, params):
        self._validate_type(params, six.string_types)

    def _validate_integer(self, model, params):
        self._validate_type(params, int)

    def _validate_boolean(self, model, params):
        self._validate_type(params, bool)

    def _validate_type(self, param, param_type):
        if not isinstance(param, param_type):
            raise RuntimeError(
                'Param %s is of type %s, expecting parameter of type %s '
                'instead.' % (
                    param, param_type, type(param)))


class ResponseParamsParser(object):
    def parse(self, operation_output_model, api_response):
        """Parse a response based on an operation model

        :type operation_output_model: dict
        :param operation_output_model: The loaded JSON model for the output
            of an operation.
        """
        # Raise an exception if API response had an error in it.
        if 'error' in api_response:
            raise Exception(api_response['error']['message'])
        # Parse the response using the provided operation model.
        return self._parse(operation_output_model, api_response['result'])

    def _parse(self, model, params):
        output_type = model['type']
        # Parse base on the modeled type.
        return getattr(self, '_parse_' + output_type, self._parse_default)(
            model, params)

    def _parse_structure(self, model, params):
        parsed_dict = {}
        member_models = model['members']
        for param_name, param_value in params.items():
            if param_name in member_models:
                parsed_dict[param_name] = self._parse(
                    member_models[param_name], param_value)
        return parsed_dict

    def _parse_list(self, model, params):
        parsed_list = []
        member_model = model['members']
        for param in params:
            parsed_list.append(self._parse(member_model, param))
        return parsed_list

    def _parse_default(self, model, params):
        return params
