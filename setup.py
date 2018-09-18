from distutils.core import setup

from setuptools import find_packages

with open('README.md') as f:
    README = f.read()

setup(name='nwerk',
      version='0.1.0',
      description='The nano web framework for WSGI',
      long_description=README,
      long_description_content_type='text/markdown; charset=UTF-8',
      author='Adam Englander',
      author_email='adamenglander@yahoo.com',
      classifiers=[
          "Programming Language :: Python",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent,"
          "Environment :: Web Environment",
          "Development Status :: 1 - Planning",
          "Intended Audience :: Developers",
          "Natural Language :: English",
          "Internet :: WWW/HTTP :: Dynamic Content ",
          "Internet :: WWW/HTTP :: WSGI :: Application",
          "Software Development :: Libraries :: Application Frameworks",
          "Software Development :: Libraries :: Python Modules"
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
      ],
      # url='https://www.python.org/sigs/distutils-sig/',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=['webob~=1.8'],
      test_suite='tests',
      tests_require=[]
      )
