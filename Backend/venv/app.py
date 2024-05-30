from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

# Load the pickled data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    data = {
        "book_name": list(popular_df['Book-Title'].values),
        "author": list(popular_df['Book-Author'].values),
        "image": list(popular_df['Image-URL-M'].values),
        "votes": list(popular_df['num_ratings'].values),
        "rating": list(popular_df['avg_rating'].values)
    }
    return jsonify(data)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    user_input = data.get('user_input')
    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

        recommendations = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            recommendations.append(item)

        return jsonify(recommendations)
    except IndexError:
        return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
