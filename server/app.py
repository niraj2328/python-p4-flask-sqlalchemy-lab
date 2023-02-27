#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'


@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get_or_404(id)

    response_body = f"""
        <ul>Id: {animal.id}</ul>
        <ul>Name: {animal.name}</ul>
        <ul>Species: {animal.species}</ul>
        <ul>Zookeeper: {animal.zookeeper}</ul>
        <ul>Enclosure: {animal.enclosure}</ul>
    """

    return make_response(response_body, 200)


@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get_or_404(id)

    response_body = f"""
        <ul>Id: {zookeeper.id}</ul>
        <ul>Name: {zookeeper.name}</ul>
        <ul>Birthday: {zookeeper.birthday}</ul>
    """

    animals = zookeeper.animals

    if not animals:
        response_body += f"<ul>No animals under care.</ul>"
    else:
        response_body += "<ul>Animals under care:</ul>"
        for animal in animals:
            response_body += f"<li>{animal.name}</li>"

    return make_response(response_body, 200)


@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get_or_404(id)

    response_body = f"""
        <ul>Id: {enclosure.id}</ul>
        <ul>Environment: {enclosure.environment}</ul>
        <ul>Open to Visitors: {enclosure.open_to_visitors}</ul>
    """

    animals = enclosure.animals

    if not animals:
        response_body += f"<ul>No animals in enclosure.</ul>"
    else:
        response_body += "<ul>Animals in enclosure:</ul>"
        for animal in animals:
            response_body += f"<li>{animal.name}</li>"

    return make_response(response_body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
