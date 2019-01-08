from flask import Flask, jsonify
from pandas import DataFrame
from fuzzywuzzy import process, fuzz

app = Flask(__name__)

persons = [dict(name='Mauricio Macri', doc='112233', country='Argentina', counter=0),
           dict(name='Jair Bolsonaro', doc='445566', country='Brasil', counter=0),
           dict(name='Evo Morales', doc='556677', country='Bolivia', counter=0),
           dict(name='Pepe Mujica', doc='667788', country='Uruguay', counter=0)]


def match_tester2(test_user, list_db, name_param, doc_param, site_param, name_function):
    res_df = DataFrame()
    df1_ = DataFrame(process.extractWithoutOrder(str(test_user.iloc[0].name), list_db.name))
    res_df['name_score'] = df1_[1]
    df2_ = DataFrame(process.extractWithoutOrder(str(test_user.iloc[0].user_doc_number), list_db.doc, scorer = fuzz.ratio))
    res_df['doc_score'] = df2_[1]
    df3_ = DataFrame(process.extractWithoutOrder(str(test_user.iloc[0].country), list_db.country))
    res_df['country_score'] = df3_[1]
    res_df['counter'] = list_db.counter
    res_df['final_score'] = (res_df.name_score * name_param * name_function(res_df.counter)) + (res_df.doc_score * doc_param) + (res_df.country_score * site_param)
    return res_df


def name_func(xxx):
    return 100*(1/(100+1.007**xxx))


@app.route('/')
def test():
    return jsonify({'message':'It works!'})


@app.route('/search/<string:doc>', methods=['GET'])
def getOne(doc):
    result = [person for person in persons if person['doc'] == doc]
    return jsonify({'person':result[0]})


@app.route('/aprox/<string:name>/<string:doc>/<string:country>', methods=['GET'])
def get_aprox(name, doc, country):
    tester1 = DataFrame([{'name': name, 'user_doc_number': doc, 'country': country}])
    persons_df = DataFrame(persons)
    resultados = match_tester2(test_user = tester1,
                               list_db = persons_df,
                               name_param = 0.4,
                               doc_param = 0.5,
                               site_param = 0.1,
                               name_function = name_func)
    indexx = resultados.sort_values('final_score', ascending=False).head(1).index
    return jsonify(persons_df.iloc[indexx].to_dict())


if __name__ == '__main__':
    app.run(debug=True)
