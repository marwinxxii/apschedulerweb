from distutils.core import setup
try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

setup(name='apschedulerweb',
      version='0.1',
      author='Alexey Agapitov',
      author_email='marwinxxii@gmail.com',
      py_modules=['apschedulerweb'],
      requires=['bottle (>=0.9)', 'apscheduler', 'bottle_basicauth (>=0.1)'],
      cmd_class={'build_py': build_py}
      )
