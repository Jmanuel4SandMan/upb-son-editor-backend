import shlex

from flask import request
from flask_restplus import Resource, Namespace, fields

from son_editor.impl.gitimpl import clone, pull, commit_and_push, create_commit_and_push, delete, list, diff, init, \
    status
from son_editor.util.constants import WORKSPACES, GIT
from son_editor.util.requestutil import get_json, prepare_response

namespace = Namespace(WORKSPACES + '/<int:ws_id>/' + GIT, description='Git API')

pull_model = namespace.model('Pull information', {
    'project_id': fields.Integer(description='Project ID of the project to get pulled from')
})

init_model = namespace.model('Init information', {
    'project_id': fields.Integer(description='Project ID of the project to call git init from')
})

diff_model = namespace.model('Diff information', {
    'project_id': fields.Integer(description='Project ID of the project to get diff information')
})

clone_model = namespace.model('Clone information', {
    'url': fields.String(description='URL to clone from')
})

delete_model = namespace.model('Delete information', {
    'project_id': fields.Integer(description='Project ID of the project to get diff information'),
    'repo_name': fields.String(description='Remote repository that gets deleted'),
    'owner': fields.String(
        description='Owner/organization name of the repository\'s owner, otherwise user as owner is taken',
        required=False)
})

commit_model = namespace.model('Commit information', {
    'project_id': fields.Integer(description='Project ID for making commit'),
    'commit_message': fields.String(description='Commit message')
})

create_model = namespace.model('Create GitHub repository information', {
    'project_id': fields.Integer(description='Project ID for the project to push'),
    'repo_name': fields.String(description='Remote repository name for the project, that gets created')
})

response_model = namespace.model('Model response', {
    'success': fields.Boolean(description='True, if the operation was successful, otherwise false'),
    'message': fields.String(description='Reason'),
    'exitcode': fields.Integer(description='Exitcode of git')
})

exception_model = namespace.model('Exception response', {
    'message': fields.String()
})


@namespace.route('/clone')
class GitClone(Resource):
    @namespace.expect(clone_model)
    @namespace.response(200, "OK", response_model)
    @namespace.response(400, "When the cloned project seems to be no son project")
    @namespace.response(404, "When workspace not found", exception_model)
    @namespace.response(409, "When project already exists", exception_model)
    def post(self, ws_id):
        """ Clones projects into the workspace """
        json_data = get_json(request)
        result = clone(ws_id, shlex.quote(json_data['url']))
        return prepare_response(result, 200)


@namespace.route('/delete')
class GitDelete(Resource):
    @namespace.expect(delete_model)
    @namespace.response(200, "OK", response_model)
    def delete(self, ws_id):
        """ Deletes a remote repository"""
        json_data = get_json(request)
        result = delete(ws_id, int(json_data['project_id']), shlex.quote(json_data['repo_name']))
        return prepare_response(result, 200)


@namespace.route('/diff')
class GitDiff(Resource):
    @namespace.expect(diff_model)
    @namespace.response(200, "OK, with output information of 'git diff'")
    def post(self, ws_id):
        """ Retrieves the current diff of the project directory"""
        json_data = get_json(request)
        result = diff(ws_id, int(json_data['project_id']))
        return prepare_response(result, 200)


@namespace.route('/status')
class GitStatus(Resource):
    @namespace.expect(diff_model)
    @namespace.response(200, "OK, with output information of 'git status'")
    def post(self, ws_id):
        """ Retrieves the current status of the project directory"""
        json_data = get_json(request)
        result = status(ws_id, int(json_data['project_id']))
        return prepare_response(result, 200)


@namespace.route('/init')
class GitInit(Resource):
    @namespace.expect(init_model)
    @namespace.response(200, "OK", response_model)
    def post(self, ws_id):
        """ Initializes a repository in the given project"""
        json_data = get_json(request)
        result = init(ws_id, int(json_data['project_id']))
        return prepare_response(result, 200)


@namespace.route('/commit')
class GitCommit(Resource):
    @namespace.expect(commit_model)
    @namespace.response(200, "OK", response_model)
    @namespace.response(404, "When project or workspace not found", exception_model)
    def post(self, ws_id):
        """ Commits and pushes changes """
        json_data = get_json(request)
        result = commit_and_push(ws_id, int(json_data['project_id']), shlex.quote(json_data['commit_message']))
        return prepare_response(result, 200)


@namespace.route('/list')
class GitList(Resource):
    @namespace.response(200, "Visit https://developer.github.com/v3/repos/#response")
    def get(self, ws_id):
        """ Lists remote repository information """
        return prepare_response(list(ws_id))


@namespace.route('/create')
class GitCreate(Resource):
    @namespace.expect(create_model)
    @namespace.response(201, "When project got created and push went fine")
    @namespace.response(404, "When project or workspace not found", exception_model)
    def post(self, ws_id):
        """ Creates a remote repository and pushes a project for it"""
        json_data = get_json(request)
        result = create_commit_and_push(ws_id, int(json_data['project_id']),
                                        shlex.quote(json_data['repo_name']))
        return prepare_response(result)


@namespace.route('/pull')
class GitPull(Resource):
    @namespace.expect(pull_model)
    @namespace.response(200, "OK", response_model)
    @namespace.response(404, "When project or workspace not found", exception_model)
    def post(self, ws_id):
        """ Pulls updates from a project """
        json_data = get_json(request)
        result = pull(ws_id, json_data['project_id'])
        return prepare_response(result, 200)
