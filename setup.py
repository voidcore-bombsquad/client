from distutils.core import Extension, setup
from Cython.Build import cythonize

import os


ext_module = Extension('exen', [])


for root, dirs, files in os.walk(ext_module.name):
    for file in files:
        if file.endswith('.py'):
            file = os.path.join(root, file)
            ext_module.sources.append(file)


setup(ext_modules=cythonize(ext_module, compiler_directives={'language_level': 3, 'binding': True}))
