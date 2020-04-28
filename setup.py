# Licensed to the White Turing under one or more
# contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.


# Note: To upload this project, you must:

'''
python setup.py sdist
pip install dist/cerium-1.2.6.tar.gz
python setup.py bdist_wheel
pip install twine
twine upload dist/*
'''

import os.path
from setuptools import setup

from cerium import __version__


# What packages are required for this module to be executed?
requires = [
    'lxml>=4.2.1',
]

# Import the README and use it as the long-description.
cwd = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Where the magic happens:
setup(
    name='cerium',
    packages=['cerium'],
    version=__version__,
    license='Apache 2.0',
    author='White Turing',
    author_email='fujiawei@stu.hznu.edu.cn',
    description='An Android automation framework.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ffujiawei/cerium',
    keywords=['android', 'adb', 'automation', 'testing'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries',
    ],
    package_data={
        'cerium': [
            'cerium/executable/adb.exe',
            'cerium/executable/AdbWinApi.dll',
            'cerium/executable/AdbWinUsbApi.dll',
        ]
    },
    include_package_data=True,
    python_requires='>=3.6.0',
    install_requires=requires,
    platforms=["Windows"],
)
