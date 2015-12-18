from flask import Flask, jsonify, render_template, request
import praw
import ConfigParser
app = Flask(__name__)

#reddit user-agent handle
Config = ConfigParser.ConfigParser()
user_name = Config.get('Credentials', 'user')
passwd = Config.get('Credentials', 'pass')

page_limit = 10
sorts = ['hot', 'new', 'top', 'controversial']
sort_time_frames = ['hour', 'day', 'week', 'month', 'year', 'all']

r = praw.Reddit(user_agent='aw_test_reddit_app_1_0')
r.login(user_name, passwd) #todo: switch to oauth

@app.route('/')
@app.route('/index')
def get_submissions():

    submissions = r.get_subreddit('all').get_hot(limit=page_limit)
    attrs = dir(submissions)
    # now dump this in some way or another
    print attrs
    return render_template('index.html',
	                           user_name=user_name,
	                           submissions=submissions)
    #return jsonify(results = [str(x) for x in submissions])


@app.route('/next', defaults={'before':'', 'after':''})
@app.route('/next/page/<before>/<after>')
def get_next_page(before, after):

    submissions = r.get_subreddit('all').get_hot(limit=page_limit)
    if not users:
        abort(404)
    return render_template('index.html',
                               user_name=user_name,
                               before=submissions.before,
                               after=submissions.after,
                               submissions=submissions)


#@app.route('/_save/<submission_id>')
@app.route('/_save')
def save():
    submission = r.get_submission(submission_id=request.args.get('submission_id'))
    submission.save()
    return ('', 204)


@app.route('/_unsave')
def unsave():
    submission = r.get_submission(submission_id=request.args.get('submission_id'))
    submission.unsave()
    return ('', 204)

@app.route('/saved', defaults={'sort':'top', 'sort_time_frame':'all'}, methods=['GET', 'POST'])
@app.route('/saved/<sort>/<sort_time_frame>', methods=['GET', 'POST'])
def get_saved(sort, sort_time_frame):
    if request.method == 'POST':
        sort = request.form['sort']
        sort_time_frame = request.form['sort_time_frame']

    submissions = r.user.get_saved(sort=sort,time=sort_time_frame)

    return render_template('saved_submissions.html',
                               user_name=user_name,
                               sorts=sorts,
                               sort_time_frames=sort_time_frames,
                               submissions=submissions)
    # user_name=user_name, 
    # sorts=sorts,
    # sort_time_frames=sort_time_frames,
    # submissions=submissions
    return #jsonify(results = [str(x) for x in submissions])


@app.route('/comments/<submission_id>')
def get_comments(submission_id):

    submission = r.get_submission(submission_id=submission_id)
    return render_template('comments.html',
                       title=submission.title,
                       submission=submission)

if __name__ == '__main__':
  app.run(debug=True)
  Config.read("config.ini")