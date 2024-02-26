#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """
    retrieves all City objects from a specific state
    :return: json of all cities in a state or 404 on error
    """
    city_list = []
    state_obj = storage.get("State", state_id)

    if state_obj is None:
        abort(404)
    for obj in state_obj.cities:
        city_list.append(obj.to_json())

    return jsonify(city_list)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """
    create city route
    param: state_id - state id
    :return: newly created city obj
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id

    new_city = City(**city_json)
    new_city.save()
    resp = jsonify(new_city.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/cities/<city_id>",  methods=["GET"],
                 strict_slashes=False)
def city_by_id(city_id):
    """
    gets a specific City object by ID
    :param city_id: city object id
    :return: city obj with the specified id or error
    """

    fetched_obj = storage.get("City", str(city_id))

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_json())


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """
    updates specific City object by ID
    :param city_id: city object ID
    :return: city object and 200 on success, or 400 or 404 on failure
    """
    city_json = request.get_json(silent=True)
    if city_json is None:
        abort(400, 'Not a JSON')
    fetched_obj = storage.get("City", str(city_id))
    if fetched_obj is None:
        abort(404)
    for key, val in city_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(fetched_obj, key, val)
    fetched_obj.save()
    return jsonify(fetched_obj.to_json())


@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(city_id):
    """
    deletes City by id
    :param city_id: city object id
    :return: empty dict with 200 or 404 if not found
    """

    fetched_obj = storage.get("City", str(city_id))

    if fetched_obj is None:
        abort(404)

    storage.delete(fetched_obj)
    storage.save()

    return jsonify({})

# #!/usr/bin/python3
# '''Contains the cities view for the API.'''
# from flask import jsonify, request
# from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

# from api.v1.views import app_views
# from models import storage, storage_t
# from models.city import City
# from models.place import Place
# from models.review import Review
# from models.state import State


# @app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
# @app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
# def handle_cities(state_id=None, city_id=None):
#     '''The method handler for the cities endpoint.
#     '''
#     handlers = {
#         'GET': get_cities,
#         'DELETE': remove_city,
#         'POST': add_city,
#         'PUT': update_city,
#     }
#     if request.method in handlers:
#         return handlers[request.method](state_id, city_id)
#     else:
#         raise MethodNotAllowed(list(handlers.keys()))


# def get_cities(state_id=None, city_id=None):
#     '''Gets the city with the given id or all cities in
#     the state with the given id.
#     '''
#     if state_id:
#         state = storage.get(State, state_id)
#         if state:
#             cities = list(map(lambda x: x.to_dict(), state.cities))
#             return jsonify(cities)
#     elif city_id:
#         city = storage.get(City, city_id)
#         if city:
#             return jsonify(city.to_dict())
#     raise NotFound()


# def remove_city(state_id=None, city_id=None):
#     '''Removes a city with the given id.
#     '''
#     if city_id:
#         city = storage.get(City, city_id)
#         if city:
#             storage.delete(city)
#             if storage_t != "db":
#                 for place in storage.all(Place).values():
#                     if place.city_id == city_id:
#                         for review in storage.all(Review).values():
#                             if review.place_id == place.id:
#                                 storage.delete(review)
#                         storage.delete(place)
#             storage.save()
#             return jsonify({}), 200
#     raise NotFound()


# def add_city(state_id=None, city_id=None):
#     '''Adds a new city.
#     '''
#     state = storage.get(State, state_id)
#     if not state:
#         raise NotFound()
#     data = request.get_json()
#     if type(data) is not dict:
#         raise BadRequest(description='Not a JSON')
#     if 'name' not in data:
#         raise BadRequest(description='Missing name')
#     data['state_id'] = state_id
#     city = City(**data)
#     city.save()
#     return jsonify(city.to_dict()), 201


# def update_city(state_id=None, city_id=None):
#     '''Updates the city with the given id.
#     '''
#     xkeys = ('id', 'state_id', 'created_at', 'updated_at')
#     if city_id:
#         city = storage.get(City, city_id)
#         if city:
#             data = request.get_json()
#             if type(data) is not dict:
#                 raise BadRequest(description='Not a JSON')
#             for key, value in data.items():
#                 if key not in xkeys:
#                     setattr(city, key, value)
#             city.save()
#             return jsonify(city.to_dict()), 200
#     raise NotFound()
