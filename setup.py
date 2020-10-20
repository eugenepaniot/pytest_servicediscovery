import setuptools

setuptools.setup(
    name="pytest_servicediscovery",
    version="4.0.0",
    description='Service Discovery pytest plugin',
    long_description='Service Discovery pytest plugin',
    author='Eugene Paniot',
    author_email='e.paniot@gmail.com',

    python_requires='<4',

    packages=["pytest_servicediscovery",
              "pytest_servicediscovery/decorators/",
              "pytest_servicediscovery/exceptions",
              "pytest_servicediscovery/factories",
              "pytest_servicediscovery/models",
              "pytest_servicediscovery/models/configuration/",
              "pytest_servicediscovery/models/types/",
              "pytest_servicediscovery/providers",
              "pytest_servicediscovery/tests",
              ],

    include_package_data=True,

    install_requires=['pytest',
                      'PyHamcrest',
                      'allure-pytest',
                      'factory-boy',
                      'pytest-factoryboy',
                      'schematics',
                      'six',
                      'PyYAML',
                      'python-consul',
                      'pyjks',
                      'pyOpenSSL',
                      'hvac',
                      'google-cloud-storage',
                      'googleapis-common-protos',
                      'google-api-core',
                      'google-auth',
                      'google-cloud-core',
                      'google-cloud-storage',
                      'google-resumable-media',
                      'more-itertools',
                      'validators'],

    zip_safe=False,
    platforms='any',

    entry_points={
        'pytest11': [
            'servicediscovery = pytest_servicediscovery.plugin',
        ],
    },

    keywords=['pytest', 'servicediscovery', 'plugin'],
    classifiers=["Framework :: Pytest"],
)
