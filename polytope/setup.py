# coding:utf8
from setuptools import setup, find_packages

readme = open('README.md').read()

setup(
    name="polytope",
    version="0.0.1-SNAPSHOT",
    description="python spout and bolt in polytope",
    author="shaolianbo",
    author_email="lianboshao@sohu-inc.com",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'polytope.spout_source.utils.ipip': ['*.datx'],
    },
    install_requires=[
        'kazoo',
        'samsa'
    ],
    entry_points={
        'console_scripts': [
            'polytope-spout = polytope.monitor_data_spout:run',
            'polytope-addup = polytope.addup_bolt:run',
            'polytope-store = polytope.store_bolt:run',
        ]
    },
    long_description=readme
)
