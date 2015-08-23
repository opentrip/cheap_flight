from setuptools import setup, find_packages

with open("requirements.txt") as fhandler:
    install_requires = [
        line.strip()
        for line in fhandler.readlines()
    ]


setup(
    name='CheapFlight',
    version='0.0.1.dev',
    url='http://github.com/mckelvin/cheap_flight/',
    license='BSD',
    author='mckelvin',
    author_email='mckelvin@noreply.github.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
)
