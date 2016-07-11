from django.test.runner import DiscoverRunner # default
from colour_runner.django_runner import ColourRunnerMixin

class BookOCRTestRunner(ColourRunnerMixin, DiscoverRunner):
    pass

