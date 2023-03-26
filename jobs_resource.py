from data.jobs import Jobs
from data import db_session
from flask_restful import abort, Resource
from flask import jsonify
from data.jobs_resource_parser import parser
from data.hazard_levels import HazardLevel


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    news = session.query(Jobs).get(job_id)
    if not news:
        abort(404, message=f"News {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'jobs': job.to_dict(
            only=('team_leader', "job", "work_size", "collaborators", "is_finished", "start_date", "end_date",
                  "hazard_level"))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, job_id):
        args = parser.parse_args()
        if not args or not all(key in args for key in
                               ['team_leader', "job", "work_size", "collaborators", "is_finished", "start_date",
                                "end_date", "hazard_level", ]):
            return jsonify({'error': 'Bad request'})
        db_sess = db_session.create_session()
        job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
        if job is None:
            job = Jobs()
            job.id = job_id
        job.job = args['job']
        job.team_leader = args['team_leader']
        job.is_finished = args['is_finished']
        job.start_date = args['start_date']
        job.end_date = args['end_date']
        job.collaborators = args['collaborators']
        job.work_size = args['work_size']
        haz_lvl = HazardLevel()
        haz_lvl.level = args['hazard_level']
        job.hazard_level.append(haz_lvl)
        db_sess.add(job)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        data = db_sess.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict() for item in data]})

    def post(self):
        args = parser.parse_args()
        if not args or not all(key in args for key in
                               ['team_leader', "job", "work_size", "collaborators", "is_finished", "start_date",
                                "end_date", "hazard_level"]):
            return jsonify({'error': 'Bad request'})
        db_sess = db_session.create_session()
        job = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished'],
            start_date=args['start_date'],
            end_date=args['end_date'],
        )
        haz_lvl = HazardLevel()
        haz_lvl.level = args["hazard_level"]
        job.hazard_level.append(haz_lvl)
        db_sess.add(job)
        db_sess.commit()
        return jsonify({'success': 'OK'})
