#!/usr/bin/python3

""" objects that handle all default RestFul API actions for States """


from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_state.yml', methods=['GET'])
def get_states():
    """
    Retrieves the list of all State objects
    """
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_id_state.yml', methods=['get'])
def get_state(state_id):
    """ Retrieves a specific State """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/delete_state.yml', methods=['DELETE'])
def delete_state(state_id):
    """
    Deletes a State Object
    """

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post_state.yml', methods=['POST'])
def post_state():
    """
    Creates a State
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


<<<<<<< HEAD
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/state/put_state.yml', methods=['PUT'])
def put_state(state_id):
    """
    Updates a State
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
=======
def update_state(state_id=None):
    '''Updates the state with the given id.
    '''
    xkeys = ('id', 'created_at', 'updated_at')
    all_states = storage.all(State).values()
    res = list(filter(lambda x: x.id == state_id, all_states))
    if res:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        old_state = res[0]
        for key, value in data.items():
            if key not in xkeys:
                setattr(old_state, key, value)
        old_state.save()
        return jsonify(old_state.to_dict()), 200
    raise NotFound()

# #!/usr/bin/python3
# """Create a view for state"""

# from flask import jsonify, request, abort, make_response
# from api.v1.views import app_views
# from models import storage
# from models.state import State


# @app_views.route('/states', methods=['GET'], strict_slashes=False)
# def get_states():
#     """Retrieves the list of all State objects"""
#     state_obj = storage.all(State)
#     return jsonify([obj.to_dict() for obj in state_obj.values()])


# @app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
# def get_states_id(state_id):
#     """Retrieves a State object by ID"""
#     state = storage.get("State", state_id)
#     if state is None:
#         abort(404)
#     return jsonify(state.to_dict())


# @app_views.route('/states/<state_id>', methods=['DELETE'],
#                  strict_slashes=False)
# def delete_state(state_id):
#     """Deletes a State object by ID"""
#     state = storage.get("State", state_id)
#     if state is None:
#         abort(404)
#     storage.delete(state)
#     storage.save()
#     return make_response(jsonify({}), 200)


# @app_views.route('/states', methods=['POST'], strict_slashes=False)
# def create_state():
#     """Creates a new state"""
#     new_state = request.get_json()
#     if not new_state:
#         abort(400, 'Not a JSON')
#     if 'name' not in new_state:
#         abort(400, 'Missing name')
#     state = State(**new_state)
#     storage.new(state)
#     storage.save()
#     return make_response(jsonify(state.to_dict()), 201)


# @app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
# def update_state(state_id):
#     """Updates a State object by ID"""
#     state = storage.get("State", state_id)
#     if state is None:
#         abort(404)
#     data = request.get_json()
#     if not data:
#         abort(400, 'Not a JSON')

#     # Update the State object's attributes based on the JSON data
#     for key, value in data.items():
#         if key not in ['id', 'created_at', 'updated_at']:
#             setattr(state, key, value)
#     state.save()
#     return make_response(jsonify(state.to_dict()), 200)
>>>>>>> 8c4ec8a6679eb59c02437da4d8fd053a720cb12e
