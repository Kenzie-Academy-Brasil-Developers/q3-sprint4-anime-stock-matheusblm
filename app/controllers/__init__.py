from flask import  jsonify, request
from http import HTTPStatus
from psycopg2.errors import UniqueViolation
from psycopg2.errors import UndefinedTable
from app.models.anime_modal import Anime

def create():
    try:
        data = request.get_json()
        Anime.verify_keys(data)   
        animes = Anime(**data)
        inserted_anime = animes.create_anime()
    except UniqueViolation:
        return (
            jsonify({"error": 'anime is already exists'}), HTTPStatus.UNPROCESSABLE_ENTITY
        )
    except KeyError:
        keys = ["anime", "released_date", "seasons"]
        request_data_keys = list(data.keys())
        compared_keys = [not_key for not_key in request_data_keys if not_key not in keys]
        return jsonify(
            {
                "available_keys": [
                "anime",
                "released_date",
                "seasons"
                ]
            }, {
                "wrongs_keys_sended":
                compared_keys
            }
            ),HTTPStatus.UNPROCESSABLE_ENTITY 
    anime_keys = ['id', 'anime', 'released_date', 'seasons']
    inserted_anime = dict(zip(anime_keys, inserted_anime))
    return jsonify(inserted_anime), HTTPStatus.CREATED

def animes():
    try:
        Anime.get_animes()
    except UndefinedTable:
        Anime.create_table()
        return jsonify({"data": []}), HTTPStatus.OK    
    except TypeError:
        return jsonify({"data": []}), HTTPStatus.OK    
    anime_keys = ['id', 'anime', 'released_date', 'seasons']
    animes_list = [dict(zip(anime_keys, anime)) for anime in Anime.get_animes()]
    return jsonify({'data': animes_list}), HTTPStatus.OK

def select_by_id(anime_id):
    anime_keys = ['id', 'anime', 'released_date', 'seasons']
    animes_list = [dict(zip(anime_keys, anime)) for anime in Anime.get_anime_by_id(anime_id)]
    if animes_list == []:
        return jsonify({"error": "Not Found"}), HTTPStatus.NOT_FOUND
    return jsonify({'data': animes_list}), HTTPStatus.OK

def update(anime_id):
    payload = request.get_json()
    try:
        Anime.verify_keys(payload) 
        updated_anime = Anime.update_anime(anime_id, payload)
        if not updated_anime:
            return jsonify({"error": "Not Found"}), HTTPStatus.NOT_FOUND

        serialize_anime = Anime.serialize_anime(updated_anime)
    except KeyError:
        keys = ["anime", "released_date", "seasons"]
        request_data_keys = list(payload.keys())
        compared_keys = [wrong_key for wrong_key in request_data_keys if wrong_key not in keys]
        return jsonify(
            {
                "available_keys": [
                "anime",
                "released_date",
                "seasons"
                ]
            }, {
                "wrongs_keys_sended":
                compared_keys
            }
            ),HTTPStatus.UNPROCESSABLE_ENTITY
    return jsonify(serialize_anime), HTTPStatus.OK

def delete(anime_id):
    anime = Anime.get_anime_by_id(anime_id)
    if anime == []:
        return jsonify({"error": "Not Found"}), HTTPStatus.NOT_FOUND
    Anime.delete_anime(anime_id)
    return '', HTTPStatus.NO_CONTENT 