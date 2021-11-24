from setuptools import setup

with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name='liteflow.providers.sqlite',
    version='0.1.1',
    description='Sqlite persistence provider for LiteFlow',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Serik Uatkhanov',
    author_email='serik.uatkhanov@gmail.com',
    license='MIT',
    namespace_packages=['liteflow'],
    packages=['liteflow.providers.sqlite'],
    zip_safe=False,
    install_requires=[
        'liteflow.core>=0.3',
        'python-interface>=1.4.0'
    ],
    url="https://github.com/USerik/liteflow",
    python_requires='>=3.6',
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    )
)