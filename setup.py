#!/usr/bin/env python
install_requires=['numpy','scipy','h5py','xarray']
tests_require=['pytest','nose','coveralls']
# %%
from setuptools import setup,find_packages

setup(name='piradar',
      packages=find_packages(),
      author='Michael Hirsch, Ph.D.',
      version='0.5.1',
      description='HF radar for ionosphere using Red Pitaya for RF and Raspberry Pi coprocessor',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: MIT License',
      'Topic :: Scientific/Engineering :: Atmospheric Science',
      'Programming Language :: Python :: 3.6',
      ],
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'plot':['matplotlib','seaborn',],
                       'io':['radioutils'],
                       'tests':tests_require},
      python_requires='>=3.6',
	  )

