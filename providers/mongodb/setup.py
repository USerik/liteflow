from setuptools import setup

setup(
    name='liteflow.providers.mongo',
    version='0.2',
    description='MongoDB persistence provider for LiteFlow',
    author='Daniel Gerlag',
    author_email='daniel@gerlag.ca',
    license='MIT',
    namespace_packages=['liteflow'],
    packages=['liteflow.providers.mongo'],
    zip_safe=False,
    install_requires=[
        'liteflow.core>=0.2',
        'pymongo>=3.6.1',
        'python-interface>=1.4.0'
    ],
    url="https://github.com/danielgerlag/liteflow",
    python_requires='>=3.6'
)