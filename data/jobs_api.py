import flask
from flask import jsonify, request
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.hazard_levels import HazardLevel

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_news():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('job', 'user.name'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(job_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=('job', 'user.name'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'hazard_level', 'collaborators',
                  'start_date', 'end_date', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if "id" in request.json:
        if db_sess.query(Jobs).filter(request.json["id"] == Jobs.id).first():
            return jsonify({'error': "Id already exists"})
    job = Jobs()
    r = request.json
    job.job = r["job"]
    job.team_leader = r["team_leader"]
    job.collaborators = r["collaborators"]
    job.is_finished = r["is_finished"]
    job.start_date = r["start_date"]
    job.end_date = r["end_date"]
    job.work_size = r["work_size"]
    hazard = HazardLevel()
    hazard.level = r["hazard_level"]
    job.hazard_level.append(hazard)
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:id>', methods=['DELETE'])
def delete_job(id):
    db_sess = db_session.create_session()
    el = db_sess.query(Jobs).get(id)
    if not el:
        return jsonify({'error': 'Bad request'})
    db_sess.delete(el)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:id>', methods=['PUT'])
def edit_job(id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'hazard_level', 'collaborators',
                  'start_date', 'end_date', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(id)
    if not job:
        return jsonify({'error': "Id doesn't exist"})
    if not db_sess.query(User).filter(User.email == request.json['team_leader']).first():
        return jsonify({'error': 'Bad request'})
    r = request.json
    job.job = r["job"]
    job.team_leader = r["team_leader"]
    job.collaborators = r["collaborators"]
    job.is_finished = r["is_finished"]
    job.start_date = r["start_date"]
    job.end_date = r["end_date"]
    job.work_size = r["work_size"]
    hazard = HazardLevel()
    hazard.level = r["hazard_level"]
    job.hazard_level.append(hazard)
    db_sess.commit()
    return jsonify({'success': 'OK'})
