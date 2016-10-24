from son_editor.util import constants
from son_editor.app.exceptions import NameConflict
import son_editor.impl.workspaceimpl
import son_editor.impl.projectsimpl
import son_editor.impl.servicesimpl
import son_editor.impl.functionsimpl
from son_editor.app.database import db_session
from son_editor.models.user import User
import json


def _get_header():
    return {'Content-Type': 'application/json'}


def create_vnf(user, wsid: int, pjid: int, name: str, vendor: str, version: str) -> str:
    """
    Creates a function with given name, vendor and version in the given project returns the id
    :param testcase: Testcase instance to call HTTP requests
    :param wsid: ID of the workspace
    :param pjid: ID of the project
    :param name: Name for the function to create
    :param vendor: Vendor name for the function to create
    :param version: Version name for the function to create
    :returns: ID of the created function
    """
    result = son_editor.impl.functionsimpl.create_function({'login': user.name}, wsid, pjid,
                                                           {"vendor": vendor,
                                                            "name": name,
                                                            "version": version})
    return result['id']


def create_ns(wsid: int, pjid: int, name: str, vendor: str, version: str) -> int:
    """
    Creates a function with given name, vendor and version in the given project returns the id
    :param testcase: Testcase instance to call HTTP requests
    :param wsid: ID of the workspace
    :param pjid: ID of the project
    :param name: Name for the function to create
    :param vendor: Vendor name for the function to create
    :param version: Version name for the function to create
    :returns: ID of the created function
    """

    result = son_editor.impl.servicesimpl.create_service(wsid, pjid,
                                                         {'name': name, 'vendor': vendor, 'version': version})
    return result['id']


def create_workspace(user, ws_name: str) -> int:
    """
    Creates a workspace
    :param testcase: Testcase instance to call HTTP requests
    :param name: Name of the workspace that gets created
    :return: ID of the created workspace
    """

    user_data = {'login': user.name}
    ws_data = {'name': ws_name}
    workspace_data = son_editor.impl.workspaceimpl.create_workspace(user_data, ws_data)
    return workspace_data['id']


def create_logged_in_user(app, user_name) -> User:
    """
    Creates a user with database record and session
    :param app: Test context / app
    :param user_name: User name
    :return: Model instance
    """
    # Add some session stuff ( need for finding the user's workspace )
    with app as c:
        with c.session_transaction() as session:
            session['userData'] = {'login': user_name}

    # Add some dummy objects
    user = User(name=user_name, email=user_name + "@bar.com")
    session = db_session()
    session.add(user)
    session.commit()
    return user


def delete_workspace(testcase, ws_id: int):
    """
    Deletes a workspace
    :param testcase: Testcase instance to call HTTP requests
    :param ws_id: The workspace id which gets deleted
    :return: True, if successful
    """
    response = testcase.app.delete("/" + constants.WORKSPACES + "/" + str(ws_id) + "/",
                                   headers=_get_header())
    return response.status_code == 200


def create_project(ws_id: int, project_name: str) -> str:
    """
    Creates a project
    :param testcase: Testcase instance to call HTTP requests
    :param ws_id: The workspace where the project gets created
    :param project_name: Name of the workspace that gets created
    :return: ID of the created project
    """
    return son_editor.impl.projectsimpl.create_project(ws_id, {'name': project_name})['id']