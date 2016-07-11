from django.test.runner import DiscoverRunner # default

try:
	from django_nose import NoseTestSuiteRunner as Runner
	class BookOCRTestRunner(Runner):
		pass
except ImportError:
	print('django_nose not installed, trying ColourRunnerMixin')
	try:
		from colour_runner.django_runner import ColourRunnerMixin

		class BookOCRTestRunner(ColourRunnerMixin, DiscoverRunner):
			pass
	except:
		print('ColourRunnerMixin not installed, reverting to default')
		class BookOCRTestRunner(DiscoverRunner):
			pass

