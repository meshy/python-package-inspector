from django.core.urlresolvers import reverse
import neo4django
from neo4django.db import models

from packages import base_models



class Package(models.NodeModel):
    name = models.StringProperty(unique=True, indexed=True)

    def get_absolute_url(self):
        return reverse('package-detail', kwargs={'package': self.name})

    def __unicode__(self):
        return self.name


class PackageVersion(models.NodeModel):
    name = models.StringProperty()
    package = models.Relationship(Package,
        rel_type=neo4django.Outgoing.VERSION_OF,
        single=True,
        related_name='versions')

    class Meta:
        unique_together = ('name', 'package')

    def __unicode__(self):
        return '{package} {ver}'.format(package=self.package, ver=self.name)


class Module(base_models.DocStringMixin, base_models.PythonNode):
    package_version = models.Relationship(PackageVersion,
        rel_type=neo4django.Outgoing.BELONGS_TO,
        single=True,
        related_name='modules')

    def __unicode__(self):
        return self.name


class Function(base_models.CallableMixin, base_models.CodeNode):
    def __unicode__(self):
        return 'def {0}({1})'.format(self.name, self.arguments)


class BasicCode(base_models.CodeNode):
    def __unicode__(self):
        return 'Codeblock: {0}'.format(self.name)


class Klass(base_models.CallableMixin, base_models.PythonNode):
    superclasses = models.Relationship(PackageVersion,
        rel_type=neo4django.Outgoing.SUPER_CLASS,
        related_name='subclasses')

    def __unicode__(self):
        return 'class {0}({1})'.format(self.name, self.arguments)


class Method(base_models.CallableMixin, base_models.CodeNode):
    def __unicode__(self):
        return 'def {0}({1})'.format(self.name, self.arguments)
