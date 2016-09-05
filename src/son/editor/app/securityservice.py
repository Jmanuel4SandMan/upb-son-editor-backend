from flask import session

from son.editor.app.constants import PROJECTS
from son.editor.app.database import db_session
from son.editor.app.exceptions import NotFound
from son.editor.models.project import Project
from son.editor.models.workspace import Workspace
from son.editor.users.usermanagement import get_user


# This method checks if the current user is allowed to access a given workspace
def check_access(request):
    # Access parsed values of the url
    # Check if wsID was in the url
    if 'ws_id' in request.view_args:
        ws_id = request.view_args['ws_id']
        data_session = db_session()
        ws = data_session.query(Workspace).filter_by(id=ws_id).first()
        if 'userData' in session:
            # Get current user
            user = get_user(session['userData'])
            # If the requested workspace is in his workspaces, he is allowed to access it
            if ws in user.workspaces:
                if 'project_id' in request.view_args:
                    pj_id = request.view_args['project_id']
                    pj = data_session.query(Project).filter(Project.id == pj_id).first()
                    if pj in ws.projects:
                        return
                    else:
                        raise NotFound("Project not found")
                elif 'parent_id' in request.view_args and PROJECTS in request.url.split("/"):
                    pj_id = request.view_args['parent_id']
                    pj = data_session.query(Project).filter(Project.id == pj_id).first()
                    if pj in ws.projects:
                        return
                    else:
                        raise NotFound("Project not found")
                return
        raise NotFound("Workspace not found")
    return