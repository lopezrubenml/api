from flask import Flask, jsonify
from pandas import DataFrame, Series

app = Flask(__name__)

persons = [dict(name='Mauricio Macri', doc='112233', country='Argentina'),
           dict(name='Jair Bolsonaro', doc='445566', country='Brasil'),
           dict(name='Evo Morales', doc='556677', country='Bolivia'),
           dict(name='Pepe Mujica', doc='667788', country='Uruguay')]


@app.route('/')
def test():
    return jsonify({'message':'It works!'})


@app.route('/search/<string:doc>', methods=['GET'])
def getOne(doc):
    result = [person for person in persons if person['doc'] == doc]
    return jsonify({'person':result[0]})


if __name__ == '__main__':
    app.run(debug=True)
