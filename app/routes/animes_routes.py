from flask import Blueprint
from app.controllers import create, animes, select_by_id, update,delete

bp_animes = Blueprint("animes", __name__)

bp_animes.post("/animes")(create)
bp_animes.get("/animes")(animes)
bp_animes.get("/animes/<int:anime_id>")(select_by_id)
bp_animes.patch("/animes/<int:anime_id>")(update)
bp_animes.delete("/animes/<int:anime_id>")(delete)