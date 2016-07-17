Intro
=====
This repository has sample code on how you can dynamically generate web API
clients as shown in my 2016 EuroPython talk: `Dynamic Class Generation in
Python <https://ep2016.europython.eu/conference/talks/dynamic-class-generation-in-python>`__.


Installation
============

To install the necessary dependencies, run::

    pip install -r requirements.txt


Quickstart
==========

In order for the clients to make API calls to the server, the server needs
to be up and running. So in a seperate process run::

    $ python server.py


Now you can start dynamically generating clients and interact with the server.
The current available API models for use under the ``apis`` directory are:

* ``api.json``: Only has ``multiply`` suport
* ``updated-api.json``: Has ``add``, ``subtract``, ``multiply`` support.


To start using theses models to create a client, run the following::

    >>> from client import get_model, create_client
    >>> model = get_model('apis/updated-api.json')
    >>> c = create_client(model)


Now, you should be able to use this client to interact with the server::

    >>> c.add(1, 2, 3, 4)
    10
    >>> c.subtract(10, 5, 3)
    2
    >>> c.multiply(1, 2, 3)
    6
