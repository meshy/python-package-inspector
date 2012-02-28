from django.views.generic import DetailView, ListView

from packages.models import Package, PackageVersion


class PackageList(ListView):
    queryset = Package.objects.all()


class PackageDetailView(DetailView):
    model = Package
    slug_field = 'name'
    slug_url_kwarg = 'package'


class VersionDetailView(DetailView):
    model = PackageVersion
    slug_field = 'name'
    slug_url_kwarg = 'version'

    def get_queryset(self):
        qs = super(VersionDetailView, self).get_queryset()
        return qs.filter(package__name=self.kwargs['package'])

