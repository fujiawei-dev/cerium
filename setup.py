from setuptools import setup
'''
python setup.py sdist
twine upload dist/*
'''

setup(
    name = 'cerium',
    packages = ['cerium'],
    version = '1.0.0',
    author = 'White Turing',
    author_email = 'fujiawei@stu.hznu.edu.cn',
    description = 'This project is mainly targeted to users that need to communicate with Android devices in an automated fashion, such as in automated testing.',
    keywords = ['android', 'adb', 'automation'],
    url = 'https://github.com/fjwCode/cerium',
    classifiers = [
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing',
    ],
)