import neo4django
from neo4django.db import models


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


class PythonNode(models.NodeModel):
    name = models.StringProperty(indexed=True)

    class Meta:
        abstract = True


class ChildPythonNode(PythonNode):
    owner = models.Relationship(PythonNode,
        rel_type=neo4django.Outgoing.OWNER,
        single=True,
        related_name='members')

    class Meta:
        abstract = True


class DocstringMixin(object):
    docstring = models.StringProperty()

    class Meta:
        abstract = True


class Module(DocstringMixin, ChildPythonNode):
    package_version = models.Relationship(PackageVersion,
        rel_type=neo4django.Outgoing.VERSION,
        single=True,
        related_name='modules')

    def __unicode__(self):
        return self.name


class CodeNode(ChildPythonNode):
    code = models.StringProperty()
    line_number = models.IntegerProperty()

    class Meta:
        abstract = True


class CallableMixin(DocstringMixin):
    arguments = models.StringProperty()

    class Meta:
        abstract = True


class Function(CallableMixin, CodeNode):
    def __unicode__(self):
        return 'def {name}({args})'.format(name=self.name, args=self.arguments)


class BasicCode(CodeNode):
    def __unicode__(self):
        return 'Codeblock: {0}'.format(self.name)

class Klass(CallableMixin, ChildPythonNode):
    superclasses = models.Relationship(PackageVersion,
        rel_type=neo4django.Outgoing.SUPER_CLASS,
        related_name='subclasses')

    def __unicode__(self):
        return 'class {name}({args})'.format(name=self.name, args=self.arguments)


class Method(CallableMixin, CodeNode):
    def __unicode__(self):
        return 'def {name}({args})'.format(name=self.name, args=self.arguments)
