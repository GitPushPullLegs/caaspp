from setuptools import setup
from _version import version

setup(
    name='caaspp',
    version=version,
    description="An unofficial API for CAASPP websites.",
    url="https://github.com/GitPushPullLegs/caaspp",
    author="Joe Aguilar",
    author_email="Jose.Aguilar.6694@gmail.com",
    license="GNU General Public License",
    packages=["caaspp"],
    install_requires=["requests", "lxml"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)