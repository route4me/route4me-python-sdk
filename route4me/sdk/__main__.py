from route4me.sdk import __title__
from route4me.sdk import __version__
from route4me.sdk import __build__
from route4me.sdk import __commit__

# python -m route4me-sdk (with Python >= 2.7)
if __name__ == '__main__':
	infostr = "{}\n\tVERSION : {}\n\tBUILD   : {}\n\tCOMMIT  : {}\n".format(
		__title__,
		__version__,
		__build__,
		__commit__
	)
	print(infostr)
