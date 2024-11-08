from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from typing import  List, Tuple, Any
from .models import db, Photo
from .schemas import PhotoCreateSchema
from sqlalchemy.exc import SQLAlchemyError


photo_bp = Blueprint('photo_bp', __name__)

@photo_bp.route("/",  methods=["GET"])
def index():
    photos: List[Tuple[any]] = Photo.query.all()  # Obtener todas las fotos

    photos_data = [
        {
            "id": photo.id,
            "title": photo.title,
            "description": photo.description,
            "image": photo.image
        }
        for photo in photos
    ]
    return jsonify(photos_data)



@photo_bp.route("/photos", methods=["POST"])
def add_photo():
    data = request.get_json()
    
    try:
        schema = PhotoCreateSchema(**data)  
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    new_photo = Photo(title=schema.title, description=schema.description, image=schema.image)
    
    db.session.add(new_photo)
    db.session.commit()
    
    return jsonify({"message": "Photo added", "photo": {"id": new_photo.id, "title": new_photo.title, "image": new_photo.image}}), 201



@photo_bp.route("/photos/<int:photo_id>", methods=["PUT"])
def update_photo(photo_id):
    data = request.get_json()

    photo = Photo.query.get(photo_id)
    if not photo:
        return jsonify("Foto no encontrada.", 404)
    
    try:
        schema = PhotoCreateSchema(**data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    photo.title = schema.title
    photo.description = schema.description
    photo.image = schema.image

    try:
        db.session.commit()
    except SQLAlchemyError:
        return jsonify("Ocurrió un error al actualizar la foto en la base de datos.", 500)
   
    return jsonify({"message": "Foto actualizada exitosamente", "photo": {"id": photo.id, "title": photo.title}}), 200



@photo_bp.route("/photos/<int:photo_id>", methods=["DELETE"])
def delete_photo(photo_id):
    
    photo = Photo.query.get(photo_id)
    if not photo:
        return jsonify("Foto no encontrada.", 404)

    try:
        db.session.delete(photo) 
        db.session.commit() 
    except SQLAlchemyError:
        return jsonify("Ocurrió un error al eliminar la foto de la base de datos.", 500)

    return jsonify({"message": "Foto eliminada exitosamente", "photo_id": photo_id}), 200