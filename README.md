nwerk: The Nano Web Framework for WSGI
=======================================

nwerks calls itself a nano web framework because it is so much smaller than 
existing micro frameworks. nwerks is designed to specifically get out of your 
way during development. All that the server does is provide an abstraction layer
over WSGI and allows you to write simple middleware to be executed in a stack.

Future enhancements will include:

1. WSGI based configuration bootstrap

2. Simple URL router

3. ASGI compatibility


# License

Please see the [License File](LICENSE.md)

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Install dependencies with [pipenv](https://pipenv.readthedocs.io/en/latest/)
3. Install the library in development mode (`python setup.opy develop`)
3. Make your changes
4. Test your changes (`tox`)
5. Commit your changes (`git commit -am 'Add some feature'`)
6. Push to the branch (`git push origin my-new-feature`)
7. Create new Pull Request

### Running Tests With tox

Running tests with [tox](https://tox.readthedocs.io/en/latest/) requires a number of Python versions. The best way to 
manage these versions is with [pyenv](https://github.com/pyenv/pyenv). You will 
need to register all of the versions with 
[pyenv](https://github.com/pyenv/pyenv). There are a couple ways to do that. 
An example of doing it globally is::

    pyenv global 3.5.6 3.6.6 3.7.0 pypy3.5-6.0.0

Install tox via [pipenv](https://pipenv.readthedocs.io/en/latest/)::

    pipenv install

Run tests::

    tox
