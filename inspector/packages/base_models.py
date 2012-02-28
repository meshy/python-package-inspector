from neo4django import Outgoing
from neo4django.db import models


class PythonNode(models.NodeModel):
    name = models.StringProperty()
    owner = models.Relationship('PythonNode',
        rel_type=Outgoing.OWNER,
        single=True,
        related_name='members')

    class Meta:
        abstract = True


class CodeNode(PythonNode):
    code = models.StringProperty()
    line_number = models.IntegerProperty()

    class Meta:
        abstract = True


class DocStringMixin(object):
    docstring = models.StringProperty()

    class Meta:
        abstract = True


class CallableMixin(DocStringMixin):
    arguments = models.StringProperty()

    class Meta:
        abstract = True
