from flask import Flask
from http import HTTPStatus

from app.models.anime_modal import Anime

def create():
    return {}, HTTPStatus.CREATED
def animes():
    return {}, HTTPStatus.OK
def select_by_id():
    return {}, HTTPStatus.OK
def update():
    return {}, HTTPStatus.OK
def delete():
    return {}, HTTPStatus.NO_CONTENT