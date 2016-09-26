'''
Created on 22.07.2016

@author: Jonas
'''
import logging

from flask import request, session
from flask_restplus import Model, Resource, Namespace, fields

from son_editor.impl import servicesimpl, catalogue_servicesimpl
from son_editor.util.constants import get_parent, Category, WORKSPACES, PROJECTS, CATALOGUES, PLATFORMS, SERVICES
from son_editor.util.requestutil import prepare_response, get_json

logger = logging.getLogger(__name__)

proj_namespace = Namespace(WORKSPACES + '/<int:ws_id>/' + PROJECTS + "/<int:parent_id>/" + SERVICES,
                           description="Project Service Resources")

cata_namespace = Namespace(WORKSPACES + '/<int:ws_id>/' + CATALOGUES + "/<int:parent_id>/" + SERVICES,
                           description="Catalogue Service Resources")
plat_namespace = Namespace(WORKSPACES + '/<int:ws_id>/' + PLATFORMS + "/<int:parent_id>/" + SERVICES,
                           description="Platform Service Resources")

serv = Model("Service", {
    'name': fields.String(required=True, description='The Service Name'),
    'vendor': fields.String(required=True, description='The Service Vendor'),
    'version': fields.String(required=True, description='The Service Version')

})

serv_response = serv.inherit("ServiceResponse", serv, {
    "descriptor": fields.Nested(model=serv, description="The Complete Service Descriptor"),
    "id": fields.Integer(description='The Project ID'),
    "project_id": fields.Integer(description='The parent workspace id'),
})

proj_namespace.add_model(serv.name, serv)
proj_namespace.add_model(serv_response.name, serv_response)


@proj_namespace.route('/')
@cata_namespace.route('/')
@plat_namespace.route('/')
@proj_namespace.param('ws_id', 'The Workspace identifier')
@cata_namespace.param('ws_id', 'The Workspace identifier')
@plat_namespace.param('ws_id', 'The Workspace identifier')
@proj_namespace.param('parent_id', 'The Project identifier')
@cata_namespace.param('parent_id', 'The Catalogue identifier')
@plat_namespace.param('parent_id', 'The Platform identifier')
@proj_namespace.response(200, "OK")
class Services(Resource):
    @proj_namespace.response(200, "OK", [serv_response])
    def get(self, ws_id, parent_id):
        if get_parent(request) is Category.project:
            service = servicesimpl.get_services(ws_id, parent_id)
            return prepare_response(service)
        if get_parent(request) is Category.catalogue:
            service = catalogue_servicesimpl.get_all_in_catalogue(session['userData'], ws_id, parent_id, False)
            return prepare_response(service)
        return prepare_response("not yet implemented")

    @proj_namespace.expect(serv)
    @proj_namespace.response(201, "Created", serv_response)
    def post(self, ws_id, parent_id):
        if get_parent(request) is Category.project:
            service = servicesimpl.create_service(ws_id, parent_id)
            return prepare_response(service, 201)
        if get_parent(request) is Category.catalogue:
            vnf_data = get_json(request)
            service = catalogue_servicesimpl.create_in_catalogue(session['userData'], parent_id, vnf_data['id'], False)
            return prepare_response(service)
        return prepare_response("not yet implemented")


@proj_namespace.route('/<int:service_id>')
@cata_namespace.route('/<string:service_id>')
@plat_namespace.route('/<int:service_id>')
@proj_namespace.param('ws_id', 'The Workspace identifier')
@cata_namespace.param('ws_id', 'The Workspace identifier')
@plat_namespace.param('ws_id', 'The Workspace identifier')
@proj_namespace.param('service_id', 'The Service identifier')
@cata_namespace.param('service_id', 'The Service identifier')
@plat_namespace.param('service_id', 'The Service identifier')
@proj_namespace.param('parent_id', 'The Project identifier')
@cata_namespace.param('parent_id', 'The Catalogue identifier')
@plat_namespace.param('parent_id', 'The Platform identifier')
@proj_namespace.response(200, "OK")
class Service(Resource):
    @proj_namespace.expect(serv)
    @proj_namespace.response(200, "Updated", serv_response)
    def put(self, ws_id, parent_id, service_id):
        if get_parent(request) is Category.project:
            service = servicesimpl.update_service(ws_id, parent_id, service_id)
            return prepare_response(service)
        if get_parent(request) is Category.catalogue:
            function_data = get_json(request)
            service = catalogue_servicesimpl.update_service_catalogue(ws_id, parent_id, service_id, function_data,
                                                                      False)
            return prepare_response(service)
        return prepare_response("not yet implemented")

    @proj_namespace.response(200, "Deleted", serv_response)
    def delete(self, ws_id, parent_id, service_id):
        if get_parent(request) is Category.project:
            service = servicesimpl.delete_service(parent_id, service_id)
            return prepare_response(service)
        if get_parent(request) is Category.catalogue:
            service = catalogue_servicesimpl.delete_service_catalogue(ws_id, parent_id, service_id, False)
            return prepare_response(service)
        return prepare_response("not yet implemented")

    @proj_namespace.response(200, "OK", serv_response)
    def get(self, ws_id, parent_id, service_id):
        if get_parent(request) is Category.project:
            service = servicesimpl.get_service(ws_id, parent_id, service_id)
            return prepare_response(service)
        if get_parent(request) is Category.catalogue:
            service = catalogue_servicesimpl.get_in_catalogue(ws_id, parent_id, service_id, False)
            return prepare_response(service)
        return prepare_response("not yet implemented")
