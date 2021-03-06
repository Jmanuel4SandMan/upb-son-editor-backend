from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from son_editor.app.database import Base


class Workspace(Base):
    __tablename__ = 'workspace'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    path = Column(String(255), unique=True)
    projects = relationship("Project", back_populates="workspace", cascade="all, delete-orphan")
    catalogues = relationship("Catalogue", back_populates="workspace", cascade="all, delete-orphan")
    platforms = relationship("Platform", back_populates="workspace", cascade="all, delete-orphan")
    priv_functions = relationship("PrivateFunction", back_populates="workspace", cascade="all, delete-orphan")
    priv_services = relationship("PrivateService", back_populates="workspace", cascade="all, delete-orphan")
    owner_id = Column(Integer, ForeignKey('user.id'))
    owner = relationship("User", back_populates="workspaces")
    vnf_schema_index = Column(Integer)
    ns_schema_index = Column(Integer)

    UniqueConstraint('owner_id', 'name', name='uix_1')

    def __init__(self, name=None, path=None, owner=None, vnf_schema_index=0, ns_schema_index=0):
        self.name = name
        self.path = path
        self.owner = owner
        self.vnf_schema_index = vnf_schema_index
        self.ns_schema_index = ns_schema_index

    def __repr__(self):
        return '<Workspace %r:%r>' % (self.name, self.path)

    def as_dict(self):
        return {"id": self.id, "name": self.name, "path": self.path,
                "catalogues": list(map(lambda x: x.as_dict(), self.catalogues)),
                "platforms": list(map(lambda x: x.as_dict(), self.platforms)),
                "vnf_schema_index": self.vnf_schema_index, "ns_schema_index": self.ns_schema_index}
