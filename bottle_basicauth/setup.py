from distutils.core import setup
try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

setup(name='bottle-basicauth',
      version='0.1',
      author='Alexey Agapitov',
      author_email='marwinxxii@gmail.com',
      url='https://github.com/marwinxxii/apschedulerweb',
      description='HTTP Basic authorization for Bottle',
      py_modules=['bottle_basicauth'],
      requires=['bottle (>=0.9)'],
      cmd_class={'build_py': build_py}
      )
