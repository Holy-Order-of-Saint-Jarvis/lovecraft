# :octopus: lovecraft
[![Travis](https://img.shields.io/travis/Holy-Order-of-Saint-Jarvis/lovecraft.svg?style=for-the-badge)](https://travis-ci.org/Holy-Order-of-Saint-Jarvis/lovecraft)
[![Codecov](https://img.shields.io/codecov/c/github/Holy-Order-of-Saint-Jarvis/lovecraft.svg?style=for-the-badge)](https://codecov.io/gh/Holy-Order-of-Saint-Jarvis/lovecraft)

Tecthulu API and (simplified) Ingress game model.

## Development
As a Python package, ``lovecraft`` uses [setuptools] to manage its dependencies.
This means that most everything will just work for a modern version of Python.
Since the code targets Python 3.6, this should always be the case.

First, get the source:

~~~
git clone https://github.com/Holy-Order-of-Saint-Jarvis/lovecraft.git
~~~

Then, setup a new [Pipenv]:

~~~
cd lovecraft
pipenv install
~~~

Install ``lovecraft`` and its dependencies:

~~~
python setup.py develop
~~~

Run [tox] to run test suites and code checks:

~~~
tox
~~~

### Further information

Further information, including architecture diagrams, is available in the [project overview](docs/overview.md).

<!-- links -->
[pipenv]: https://pipenv.readthedocs.io/
[setuptools]: https://setuptools.readthedocs.io/
[tox]: https://tox.readthedocs.io/
