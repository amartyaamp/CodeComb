from pip._internal.req import parse_requirements
from setuptools import setup

def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]

setup(name="CodeComb", version = '0.1.5',
	install_requires=load_requirements("requirements.txt"),
    python_requires='>=3.6.*',
	packages=['CodeComb_Core'],
	entry_points={
		'console_scripts': [ 
			'codecomb = CodeComb_Core.codecomb:run'
			]
		}
	)
