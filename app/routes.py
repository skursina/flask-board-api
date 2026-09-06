from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)



from app import db
from app.models import User, Advertisement


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return {"message": "Flask API работает"}

@main.route("/register", methods=["POST"])
def register():

    data = request.json

    email = data.get("email")
    password = data.get("password")


    if not email or not password:
        return jsonify({"error": "email and password required"}), 400

    user = User(email=email, password_hash=generate_password_hash(password))


    db.session.add(user)
    db.session.commit()


    return jsonify({
        "message": "user created",
        "id": user.id
    }), 201


@main.route("/login", methods=["POST"])
def login():

    data = request.json

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "invalid credentials"}), 401


    if not check_password_hash(user.password_hash, data.get("password")):
        return jsonify({"error": "invalid credentials"}), 401


    token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": token})


@main.route("/ads", methods=["POST"])
@jwt_required()
def create_ad():

    current_user_id = get_jwt_identity()

    data = request.json


    title = data.get("title")
    description = data.get("description")


    if not title or not description:
        return jsonify({"error": "Заголовок или описание в объявлении отсутствует."}), 400


    ad = Advertisement(title=title, description=description, owner_id=current_user_id)


    db.session.add(ad)
    db.session.commit()


    return jsonify({
        "message": "Объявление добавлено",
        "id": ad.id
    }), 201


@main.route("/ads/<int:ad_id>", methods=["GET"])
def get_ad(ad_id):

    ad = db.session.get(Advertisement, ad_id)

    if not ad:
        return jsonify({"error": "advertisement not found"}), 404


    return jsonify({
        "id": ad.id,
        "title": ad.title,
        "description": ad.description,
        "created_at": ad.created_at.isoformat(),
        "owner": ad.owner.email
    })


@main.route("/ads/<int:ad_id>", methods=["DELETE"])
@jwt_required()
def delete_ad(ad_id):

    current_user_id = int(get_jwt_identity())


    ad = db.session.get(Advertisement,ad_id)


    if not ad:
        return jsonify({"error": "advertisement not found"}), 404


    if ad.owner_id != current_user_id:
        return jsonify({"error": "you are not the owner"}), 403


    db.session.delete(ad)
    db.session.commit()


    return jsonify({"message": "advertisement deleted"})


@main.route("/ads/<int:ad_id>", methods=["PUT"])
@jwt_required()
def update_ad(ad_id):

    current_user_id = int(get_jwt_identity())

    ad = Advertisement.query.get(ad_id)

    if not ad:
        return jsonify({"error": "Объявление не найдено."}), 404


    if ad.owner_id != current_user_id:
        return jsonify({"error": "Вы не владелец этого объявления."}), 403


    data = request.json

    if "title" in data:
        ad.title = data["title"]

    if "description" in data:
        ad.description = data["description"]


    db.session.commit()


    return jsonify({"message": "Объявление обновлено!", "id": ad.id})