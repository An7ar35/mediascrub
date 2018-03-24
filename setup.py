from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.read()

setup(
    name='mediascrub',
    version='0.0.2a',
    author='An7ar35',
    author_email='',
    description='Web page media scrubber',
    long_description=readme,
    url='https://github.com/an7ar35/mediascrub',
    license=license,
    install_requires=requirements,
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points=dict(
        console_scripts=[
            'mediascrub=mediascrub.__main__:main'
        ]
    ),
    classifiers=["Development Status :: 3 - Alpha",
                 "Topic :: Utilities",
                 "Environment :: Console",
                 "Operating System :: POSIX :: Linux",
                 "License :: OSI Approved :: GNU General Public License v2 (GPLv2)"
                 ],
)
