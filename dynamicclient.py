from modeledclient import ModeledClient


def create_client(model, cls_name='MyClient', cls_bases=None):
    """Creates a new client based on an API model

    :type model: dict
    :param model: A loaded JSON model representing the API

    :type cls_name: str
    :param cls_name: The name of the client class to generate

    :type cls_bases: tuple
    :param cls_bases: A tuple of classes that the client class and the
        instantiated client should inherit from.

    :returns: A client instance based on the provided API model
    """
    cls_name = cls_name
    # If no class bases were provided, then default to the ModeledClient class.
    if not cls_bases:
        cls_bases = (ModeledClient,)
    cls_props = {}

    # Iterate over all of the available operation models.
    for operation_name, operation_model in model['operations'].items():
        # Get the proxy method for that operation.
        method = _get_client_method(operation_name)
        # Set the name for the method.
        method.__name__ = str(operation_name)
        # Create docstrings for the method.
        method.__doc__ = _get_docstring(operation_model)
        # Add the method to the class.
        cls_props[operation_name] = method

    # Create the client class.
    cls = type(cls_name, cls_bases, cls_props)
    # Return an instance of the class back.
    return cls(model)


def _get_client_method(operation_name):
    # Define a function that uses the provided operation name to invoke the
    # make modeled_api_call.
    def _api_call(self, *args, **kwargs):
        return self.make_modeled_api_call(
            operation_name, *args, **kwargs)
    return _api_call


def _get_docstring(operation_model):
    # A helper function to get the docstring based on a model.

    # Add the top-level description of the method.
    doc_str = operation_model['documentation']
    doc_str += '\n\n'

    # Add the input description as parameters to the docstring.
    input_model = operation_model['input']
    # If the top-level input model is a list, then arguments should be
    # provided as positional arguments.
    if input_model['type'] == 'list':
        doc_str += _get_param_docstring(
            'args', input_model['members']['type'] + '(s)',
            input_model['documentation']
        )

    # If the top-level input model is a structure, then arguments should
    # be provided as keyword arguments.
    if input_model['type'] == 'structure':
        for param_name, param_value in input_model['members']:
            doc_str += _get_param_docstring(
                param_name, param_value['type'], param_value['documentation']
            )

    # Add the output description as a return value for the docstring.
    doc_str += '\n:rtype: %s\n' % operation_model['output']['type']
    doc_str += ':returns: %s\n' % operation_model['output']['documentation']
    return doc_str


def _get_param_docstring(param_name, param_type, param_documentation):
    param_str = ':type %s: %s' % (param_name, param_type)
    param_str += '\n:param %s: %s\n' % (param_name, param_documentation)
    return param_str
