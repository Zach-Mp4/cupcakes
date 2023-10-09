"""Flask app for Cupcakes"""
from flask import Flask, jsonify, redirect, render_template, request
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'yurr'

connect_db(app)

@app.route('/')
def start():
    return render_template('index.html')

@app.route('/api/cupcakes', methods=['GET', 'POST'])
def get_cupcakes():
    if request.method == 'GET':
        all_cupcakes = Cupcake.query.all()
        serialized = [cake.serialize() for cake in all_cupcakes]
        return (jsonify(cupcakes=serialized), 200)
    elif request.method == 'POST':
        data = request.json
        flavor = data.get('flavor')
        size = data.get('size')
        rating = data.get('rating')
        image = data.get('image')

        new_cake = Cupcake(flavor = flavor, size = size, rating = rating, image = image)

        db.session.add(new_cake)
        db.session.commit()

        cp = Cupcake.query.get(new_cake.id)
        serialized = cp.serialize()

        return (jsonify(cupcake=serialized), 201)

        

@app.route('/api/cupcakes/<id>', methods = ['GET', 'PATCH', 'DELETE'])
def get_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    if request.method == 'GET':
        cupcake = Cupcake.query.get_or_404(id)
        serialized = cupcake.serialize()
        return (jsonify(cupcake = serialized), 200)
    elif request.method == 'PATCH':
        data = request.json
        flavor = data.get('flavor')
        size = data.get('size')
        rating = data.get('rating')
        image = data.get('image')

        cupcake.flavor = flavor
        cupcake.size = size
        cupcake.rating = rating
        cupcake.image = image

        db.session.add(cupcake)
        db.session.commit()

        new_cupcake = Cupcake.query.get(id)
        serialized = new_cupcake.serialize()
        
        return (jsonify(cupcake = serialized), 201)
    elif request.method == 'DELETE':
        Cupcake.query.filter_by(id = id).delete()
        db.session.commit()
        return (jsonify(message = 'DELETED'), 200)

    

