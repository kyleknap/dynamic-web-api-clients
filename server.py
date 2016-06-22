from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

from jsonrpc import JSONRPCResponseManager, dispatcher


@dispatcher.add_method
def multiply(*args):
    return reduce(lambda x, y: x*y, args)


@dispatcher.add_method
def add(*args):
    return reduce(lambda x, y: x+y, args)


@dispatcher.add_method
def subtract(*args):
    return reduce(lambda x, y: x-y, args)


@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, application)
