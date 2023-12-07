import flask
from errors import HttpError
from flask import jsonify, request, views
from models import Session, Ads
from schema import CreateAds, UpdateAds
from sqlalchemy.exc import IntegrityError
from tools import validate

app = flask.Flask("app")



@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response: flask.Response):
    request.session.close()
    return response


@app.errorhandler(HttpError)
def error_handler(error):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response


def get_advertisement(advertisement_id: int):
    advertisement = request.session.get(Ads, advertisement_id)
    if advertisement is None:
        raise HttpError(404, "advertisement not found")
    return advertisement


def add_advertisement(advertisement: Ads):
    try:
        request.session.add(advertisement)
        request.session.commit()
    except IntegrityError as err:
        raise HttpError(409, "user already exists")


class AdsView(views.MethodView):
    @property
    def session(self) -> Session:
        return request.session

    def get(self, advertisement_id: int):
        advertisement = get_advertisement(advertisement_id)
        return jsonify(advertisement.dict)

    def post(self):
        advertisement_data = validate(CreateAds, request.json)
        advertisement = Ads(**advertisement_data)
        add_advertisement(advertisement)
        return jsonify({"id": advertisement.id})

    def patch(self, advertisement_id: int):
        advertisement = get_advertisement(advertisement_id)
        advertisement_data = validate(UpdateAds, request.json)
        for key, value in advertisement_data.items():
            setattr(advertisement, key, value)
            add_advertisement(advertisement)
        return jsonify({"id": advertisement.id})


    def delete(self, advertisement_id: int):
        advertisement = get_advertisement(advertisement_id)
        self.session.delete(advertisement)
        self.session.commit()
        return jsonify({"status": "ok"})


ads_view = AdsView.as_view("ads_view")

app.add_url_rule(
    "/ads/<int:advertisement_id>", view_func=ads_view, methods=["GET", "PATCH", "DELETE"]
)
app.add_url_rule("/ads", view_func=ads_view, methods=["POST"])

if __name__ == "__main__":
    app.run()
