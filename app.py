from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import h11
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np
import pandas as pd
from flask.views import MethodView

from sklearn.feature_extraction.text import CountVectorizer

from flask_cors import CORS
app = Flask(__name__)
CORS(app)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('query')

dataset = pd.read_csv('datacomp2 2.3.csv')


count = CountVectorizer(stop_words=None)


def clean_data(x):

    if isinstance(x, str):
        return str.lower(x.replace(",", " "))
    else:
        return ''


features = ['Genres']

for feature in features:
    dataset[feature] = dataset[feature].apply(clean_data)


def soup(x):
    return x['Genres'] + ' ' + x['Artist']


dataset['soup'] = dataset.apply(soup, axis=1)
matrix = count.fit_transform(dataset['soup'])
cosine_sim2 = cosine_similarity(matrix, matrix)


def find_title_from_index(index):
    return dataset[dataset.index == index]["aTitle"].values[0]


def get_recommendations(title, cosine_sim=cosine_sim2):
    if title not in dataset['aTitle'].unique():
        print(title)
        return "Not in Database", -88
    else:
        i = dataset.loc[dataset['aTitle'] == title].index[0]
        lst = list(enumerate(cosine_sim[i]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        lst = lst[1:12]
        songindex = [i[0] for i in lst]  # songs index
        return dataset['aTitle'].iloc[songindex], songindex


class Recommendation(Resource):
    def get(self):
       

        pred, index = get_recommendations("Sucker")
        print(pred)
        
        # json with list of songs(indices)
        if index == -88:
            output = {
                "prediction": "Not in Db"
            }
            return output
        pred = pred.tolist()
        output = {
            "prediction": pred,
           
            }

        return output
class Recommendation2(Resource):
    def get(self,id):
        
        print(id)
        pred, index = get_recommendations(id)
        print(pred)
        
        # json with list of songs(indices)
        if index == -88:
            output = {
                "prediction": "Not in Db"
            }
            return output
        pred = pred.tolist()
        output = {
            "prediction": pred,
           
            }

        return output


api.add_resource(Recommendation, '/')
api.add_resource(Recommendation2, '/<string:id>')


if __name__ == '__main__':
    app.run(debug=True)
