import neo4django
from neo4django.db import models

from packages.base_models import PythonNode, CodeNode, DocStringMixin, CallableMixin


class Package(models.NodeModel):
    name = models.StringProperty(indexed=True)


class PackageVersion(models.NodeModel):
    name = models.StringProperty()
    package = models.Relationship(Package,
        rel_type=neo4django.Outgoing.PACKAGE,
        single=True,
        related_name='versions')

    def __unicode__(self):
        return '{package} {ver}'.format(package=self.package, ver=self.name)


class Module(DocStringMixin, PythonNode):
    package_version = models.Relationship(PackageVersion,
        rel_type=neo4django.Outgoing.VERSION,
        single=True,
        related_name='modules')

    def __unicode__(self):
        return self.name

class Function(CallableMixin, CodeNode):
    def __unicode__(self):
        return 'def {name}({args})'.format(name=self.name, args=self.arguments)


class BasicCode(CodeNode):
    def __unicode__(self):
        return 'Codeblock: {0}'.format(self.name)


class Klass(CallableMixin, PythonNode):
    superclasses = models.Relationship(PackageVersion,
        rel_type=neo4django.Outgoing.SUPER_CLASS,
        related_name='subclasses')

    def __unicode__(self):
        return 'class {name}({args})'.format(name=self.name, args=self.arguments)


class Method(CallableMixin, CodeNode):
    def __unicode__(self):
        return 'def {name}({args})'.format(name=self.name, args=self.arguments)
