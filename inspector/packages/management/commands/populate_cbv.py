import inspect
import itertools

import django
from django.core.management.base import BaseCommand, CommandError
from django.views import generic

from packages.models import Package, PackageVersion, Module, Function, BasicCode, Klass, Method

"""
This file has been lifted to help imports from:
https://github.com/refreshoxford/django-cbv-inspector/
"""

class Command(BaseCommand):
    args = ''
    help = 'Wipes and populates the CBV inspection models.'
    target = generic
    def handle(self, *args, **options):
        # Delete ALL of the things.
        Package.objects.filter(name='django').delete()
        #Inheritance.objects.filter(parent__module__project_version__project__name__iexact='django').delete()

        # Setup Project
        package = Package.objects.create(name='django')
        self.package_version = PackageVersion.objects.create(
            package=package,
            name=django.get_version(),
        )

        #self.klasses = {}
        self.process_member(self.target)
        #self.create_inheritance()

    def ok_to_add_module(self, member, parent):
        if member.__package__ is None or not member.__name__.startswith(self.target.__name__):
            return False
        return True

    def ok_to_add_klass(self, member, parent):
        if member.__name__.startswith(self.target.__name__): # TODO: why?
            return False

        if inspect.getsourcefile(member) != inspect.getsourcefile(parent):
            return False

        return True

    def ok_to_add_method(self, member, parent):
        if inspect.getsourcefile(member) != inspect.getsourcefile(parent):
            return False

        # Use line inspection to work out whether the method is defined on this klass
        # PROBABLY NOT THE BEST WAY
        lines, start_line = inspect.getsourcelines(member)
        if start_line < klass_line_start or start_line > klass_line_end:
            return False

        return True

    def process_member(self, member, parent=None, parent_node=None):
        # MODULE
        if inspect.ismodule(member):
            # Only traverse under hierarchy
            if not self.ok_to_add_module(member, parent):
                return

            print 'module', member.__name__
            # Create Module object
            print [f.name for f in Module._meta.fields]
            this_node = Module.objects.create(
                package_version=self.package_version,
                name=member.__name__,
                owner=parent_node,
                #docstring=inspect.getdoc(member),
            )

        # CLASS
        elif inspect.isclass(member):
            if not self.ok_to_add_klass(member, parent):
                return

            print 'class', member.__name__
            this_node = Klass.objects.create(
                owner=parent_node,
                name=member.__name__,
                docstring=inspect.getdoc(member),
            )

        # METHOD
        elif inspect.ismethod(member):
            if not self.ok_to_add_method(member, parent):
                return

            print 'method', member.__name__
            # Strip unneeded whitespace from beginning of code lines
            lines, start_line = inspect.getsourcelines(member)
            whitespace = len(lines[0]) - len(lines[0].lstrip())
            for i, line in enumerate(lines):
                lines[i] = line[whitespace:]

            # TODO: Strip out docstring
            # Join code lines into one string
            code = ''.join(lines)

            # Get the method arguments
            i_args, i_varargs, i_keywords, i_defaults = inspect.getargspec(member)
            arguments = inspect.formatargspec(i_args, varargs=i_varargs, varkw=i_keywords, defaults=i_defaults)

            # Make the Method node
            this_node = Method.objects.create(
                owner=parent_node,
                name=member.__name__,
                docstring=inspect.getdoc(member),
                code=code,
                line_number=start_line,
                arguments=arguments[1:-1],
            )
        else:
            return

        print this_node
        # Go through members
        for member_name, member_type in inspect.getmembers(member):
            self.process_member(member_type, member, this_node)

    def create_inheritance(self):
        for klass, representation in self.klasses.iteritems():
            direct_ancestors = inspect.getclasstree([klass])[-1][0][1]
            for i, ancestor in enumerate(direct_ancestors):
                if ancestor in self.klasses:
                    Inheritance.objects.create(
                        parent=self.klasses[ancestor],
                        child=representation,
                        order=i
                    )
