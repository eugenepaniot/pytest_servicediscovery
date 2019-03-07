Service & Secret Discovery PyTest Plugin: 3.x  


Configuration
=============

Configuration example:

discovery:
  providers:
    - name: consul-mke
      plugin: consul
      parameters:
        - ipAddress: 10.186.106.5
          port: 8500

    - name: static
      plugin: static
      parameters:
        - ip: localhost
          port: 8500

        - ip: localhost
          port: 8501

    - name: plaintext
      plugin: plaintext

    - name: gcs
      plugin: gcs

    - name: vault-local
      plugin: vault
      parameters:
        - ipAddress: 10.186.106.65
          port: 8243
          scheme: https

    - name: vault-consul
      plugin: vault-consul
      parameters:
        - scheme: https
          consulProvider: ca-dev-consul
          serviceName: vault-lb



  services:
    - name: consul
      provider: consul-mke
      parameters:
        - serviceName: consul

      secrets:
        - name: secret1
          provider: plaintext
          parameters:
            - value: secret1

        - name: secret2
          provider: gcs
          parameters:
            - bucket: secrets
              object: ca-dev-endpoints.yaml

        - name: secret3
          provider: vault-local
          parameters:
            - object: secret/foo

        - name: secret4
          provider: vault-consul
          parameters:
            - object: secret/foo


Discovery providers configuration
------------------------------------

Providers - the list of configured providers.

  

Field

Description

Example

Name

Provider name

providers:
      - name: consul
        ...

Plugin

The reference to the plugin name that implements service/secret discovery logic

providers:
      - name: consul
        plugin: consul
        ...

Parameters (Optional)

Plugin input parameters. Plugin initialization parameters

providers:
      - name: consul
        plugin: consul
        parameters:
          - ipAddress: 10.186.106.5
            port: 8500

  

Discovery services configuration
--------------------------------

Services - the list of configured services what we’re wanted to work with.

Field

Description

Example

Name

The name. This is how service object would be named/accessible in tests. This is a fixture name

services:
    - name: ...
    - name: ...
    - name: ...

  

  

  

Provider

The reference to service discovery provider name

services:
    - name: service1
      provider: consul
      ...

    - name: service2
      provider: static
      ...

Parameters

Service discovery provider plugin input parameters. Provider plugin call parameters.

services:
    - name: service1
      provider: consul
      parameters:
        - serviceName: consul

  

Discovery secret configuration
------------------------------

Secrets - the list of configured secrets.

Field

Description

Example

Name

The name. This is how secret object would be named in tests in a fixture object

      ...
      secrets:
        - name: secret1
          ...

        - name: secret2
          ...

        - name: secret3
          ...

Provider

The reference to secret discovery provider name

      ...
      secrets:
        - name: secret1
          provider: plaintext
          ...

        - name: secret2
          provider: plaintext
          ...

        - name: secret3
          provider: plaintext
          ...

Parameters

Secret discovery provider plugin input parameters. Plugin call parameters

      ...
      secrets:
        - name: secret1
          provider: plaintext
          parameters:
            - value: some-secret-value1

        - name: secret2
          provider: plaintext
          parameters:
            - value: some-secret-value2

        - name: secret3
          provider: plaintext
          parameters:
            - value: some-secret-value3


Providers
=========

Service Discovery Providers
---------------------------

### Consul service discovery provider

Consul service discovery provider used to discover service addresses from consul service catalog.

#### Example configuration

discovery:
  providers:
      - name: consul
        plugin: consul
        parameters:
          - ipAddress: 10.186.106.5
            port: 8500
            token: token

  services:
    - name: consul
      provider: consul
      parameters:
        - serviceName: consul
          tag: primary
          near: node-name

  

#### Initialisation parameters

Field

Description

Example

ipAddress

IP Address or Domain name of consul address

10.186.106.5

port

Port number of consul address

8500

token

Token to use for discovery request

token

  

#### Plugin call parameters

Field

Description

Example

serviceName

The service name to discover in consul provider

consul

tag

Specifies the tag to filter on

primary

near

Specifies a node name to sort the node list in ascending order based on the estimated round trip time from that node

node-name

  

### Static service discovery provider

Static service discovery provider used to discover service addresses from statically configured address and port.

#### Example configuration

discovery:
  providers:
      - name: static
        type: static
		parameters:
		  - ip: localhost
		    port: 8500

		  - ip: localhost
		    port: 8501

  services:
    - name: consul
      provider: static

  

#### Initialization parameters

Field

Description

Example

ip

IP Address or Domain name of service address

localhost

port

Service port number

8500

####   
Plugin call parameters

None

Secret Discovery Providers
--------------------------

### Plaintext secret discovery provider

Plaintext secret discovery provider used to discover secret from statically configured secrets

#### Example configuration

discovery:
  providers:
    - name: plaintext
      type: plaintext

  services:
    - name: ...
      secrets:
        - name: secret1
          provider: plaintext
          parameters:
            - value: secret1-value

  

#### Initialisation parameters

None

#### Plugin call parameters

Field

Description

Example

value

The service name to discover in consul provider

secret1-value

  

### JKS secret discovery provider

Allows an operator to specify a jks-keystore for the tests to load CA certificates from. Return value is a string that contains all of the found certificates concatenated.

#### Example configuration

discovery:
  providers:
    - name: jks	
      plugin: jks
      parameters:
        - passphrase: "passphrase"
          jksFile: "/etc/pki/java/cacerts"

  services:
    - name: kafka
      provider: consul
      parameters:
        - serviceName: myapp\_kafka
      
          secrets:
            - name: ssl\_cadata
              provider: jks
              parameters:
                - keyAlias: ""
                  keyPassword: ""
                  type: "ca"

  

#### Initialisation parameters

Field

Description

Example

passphrase (required)

Keystore password

forgetit

jksFile (required)

Keystore filename

/etc/pki/java/cacerts

#### Plugin call parameters

Field

Description

Example

keyAlias

Alias for the stored key or certificate

caroot

keyPassword

Password for the private key

forgetit

type

Specify what to extract - ca, cert or key

ca

### GCS secret discovery provider

Google Cloud Storage secret provider.

#### Example configuration

discovery:
  providers:
	- name: gcs
	  plugin: gcs

  services:
    - name: ...
      secrets:
		- name: secret
		  provider: gcs
		  parameters:
		    - bucket: secrets
		      object: ca-dev-endpoints.yaml

  

#### Initialisation parameters

Field

Description

Example

project (optional)

The project which the client acts on behalf of

kos-cicd

serviceAccountFile (optional)

The path to the service account json file

./service-account.json

#### Plugin call parameters

Field

Description

Example

bucket

The bucket name

secrets

object

The object path

ca-dev-endpoints.yaml

### Vault secret discovery provider

Vault secret provider.

#### Example configuration

discovery:
  providers:
	- name: vault
	  plugin: vault
	  parameters:
	    - ipAddress: 10.186.106.65
	      port: 8243
	      scheme: https
	      token: token

  services:
    - name: ...
      secrets:
		- name: secret
		  provider: vault
		  parameters:
		    - object: secret/foo

  

#### Initialisation parameters

Field

Description

Example

ipAddress

Vault ipAddress

10.186.106.65

port

Vault port

8200

scheme

HTTPS or HTTPS

https

namespace

Vault namespace

ns1

token

Vault token

token

#### Plugin call parameters

Field

Description

Example

object

The object path

secret/foo

  

#### Vault-consul secret discovery provider

Vault-consul secret provider extends vault provider with discovery address from consul

##### Example configuration

discovery:
  providers:
	- name: consul
	  plugin: consul
	  parameters:
    	- ipAddress: 10.186.106.100
	      port: 8500
   		  token: token

	- name: vault-consul
	  plugin: vault-consul
	  parameters:
   	 	- scheme: https
	      consulProvider: consul
	      serviceName: vault-lb
	      token: token

  services:
    - name: ...
      secrets:
		- name: secret
		  provider: vault-consul
		  parameters:
		    - object: secret/foo

  

##### Initialisation parameters, extends vault

Field

Description

Example

consulProvider

Reference to consul provider name. Where discover vault serviceName

consul

serviceName

The vault service name

vault-lb

##### Plugin call parameters

The same as vault.

Dynamically generated fixtures
------------------------------

We're make it easy to combine factory approach to the test setup with the dependency injection, heart of the pytest fixtures.

Every service name in the configuration will be registered as a fixture using ServiceFixtureFactory model.

  

class ServiceFixtureFactory(factory.Factory):
    class Meta(object):
        model = ServiceFixture


class ServiceModel(Model):
    name = StringType(required=True)
    address = ModelType(Address, required=True)
    addresses = ListType(ModelType(Address), required=True)
    secrets = DictType(StringType)
    health\_checks = ModelType(HealthChecks)


class ServiceFixture(ServiceModel):
   ...

Field

Description

name

The service name

address

The service address (ip, port)

addresses

The list of service addresses

secrets

The dict of secrets

health\_checks

The list of service health-checks results

  

Fixture using
-------------

Define service name in configuration and just start using fixture in a pytest standard ways - pass fixture (service name) to yours test suites.



### Example output

ServiceFixture(
secrets={u'token': u''}, 
addresses=\[
    Address(ip=10.186.106.103, port=8300),
    Address(ip=10.186.106.102, port=8300),
    Address(ip=10.186.106.104, port=8300)
\], 
health\_checks=HealthChecks(checks=\[
    HealthCheck(node=consul-0b4h, name=Serf Health Status, status=passing, output=Agent alive and reachable, id=serfHealth),
    HealthCheck(node=consul-4fxv, name=Serf Health Status, status=passing, output=Agent alive and reachable, id=serfHealth),
    HealthCheck(node=consul-wpsq, name=Serf Health Status, status=passing, output=Agent alive and reachable, id=serfHealth)
\]),
address=Address(ip=10.186.106.103, port=8300), 
name=consul)