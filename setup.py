import setuptools

setuptools.setup(
    name="pytest_servicediscovery",
    version="3.1.0",
    description='Service Discovery pytest plugin',
    long_description='Service Discovery pytest plugin',
    author='Eugene Paniot',
    author_email='e.paniot@gmail.com',

    python_requires='~=2.7',

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
                      'factory-boy==2.11.1',
                      'pytest-factoryboy==2.0.2',
                      'schematics==2.1.0',
                      'six',
                      'PyYAML',
                      'python-consul==1.1.0',
                      'pyjks==18.0.0',
                      'pyOpenSSL==19.0.0',
                      'hvac==0.7.2',
                      'google-cloud-storage==1.13.2',
                      'googleapis-common-protos==1.5.6',
                      'google-api-core==1.7.0',
                      'google-auth==1.6.2',
                      'google-cloud-core==0.29.1',
                      'google-cloud-storage==1.13.2',
                      'google-resumable-media==0.3.2',
                      'more-itertools==5.0.0',
                      'validators==0.12.6'],

    zip_safe=False,
    platforms='any',

    entry_points={
        'pytest11': [
            'servicediscovery = pytest_servicediscovery.plugin',
        ],
    },

    keywords=['pytest', 'servicediscovery', 'discovery', 'plugin'],
    classifiers=["Framework :: Pytest"],
)
