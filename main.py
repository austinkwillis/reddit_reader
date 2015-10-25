from flask import Flask, jsonify
import praw
app = Flask(__name__)

@app.route('/')
def get_r_all():

    r = praw.Reddit(user_agent='aw_test_reddit_app_1_0')
    submissions = r.get_subreddit('all').get_hot(limit=10)
    
    return jsonify(results = [str(x) for x in submissions])

if __name__ == '__main__':
    app.run(debug=True)