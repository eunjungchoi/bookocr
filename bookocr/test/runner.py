#from django.test.runner import DiscoverRunner # default
from django_nose import NoseTestSuiteRunner as Runner # default
from colour_runner.django_runner import ColourRunnerMixin

#class BookOCRTestRunner(ColourRunnerMixin, DiscoverRunner):
class BookOCRTestRunner(Runner):
    pass

