import os

from django.test.runner import DiscoverRunner # default runner

try:
	# try using nose
	from django_nose import NoseTestSuiteRunner
	class BookOCRTestRunner(NoseTestSuiteRunner):
		pass
	# try rednose
	try:
		import rednose
		os.environ['NOSE_REDNOSE'] = '1'
	except ImportError: pass

except ImportError:
	# try using ColourRunnerMixin
	print('django_nose not installed, trying ColourRunnerMixin')
	try:
		from colour_runner.django_runner import ColourRunnerMixin
		class BookOCRTestRunner(ColourRunnerMixin, DiscoverRunner):
			pass
	except:
		# fallback to default runner
		print('ColourRunnerMixin not installed, reverting to default')
		class BookOCRTestRunner(DiscoverRunner):
			pass

