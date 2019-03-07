import os

import google

from google.cloud import storage
from google.oauth2 import service_account
from hamcrest import assert_that
from schematics.types import StringType

from pytest_servicediscovery.decorators import logthis
from pytest_servicediscovery.models.Null import NullProviderCfg
from pytest_servicediscovery.models.configuration.ProviderContainerMixin import ProviderParameters
from pytest_servicediscovery.providers.BaseSecretPluginProvider import BaseSecretPluginProvider


class GoogleStorageSecretProvideConfiguration(NullProviderCfg):
    project = StringType(metadata=dict(description="The project which the client acts on behalf of"))
    serviceAccountFile = StringType(metadata=dict(description="The path to the service account json file"))


class GoogleStorageSecretProviderParameter(ProviderParameters):
    bucket = StringType(required=True, metadata=dict(description="The bucket name"))
    object = StringType(required=True, metadata=dict(description="The object path"))


class GoogleStorageSecretProvider(BaseSecretPluginProvider):
    """**GoogleStorageSecretProvider**"""

    class Meta(object):
        name = "gcs"
        model = GoogleStorageSecretProvideConfiguration
        model_parameters = GoogleStorageSecretProviderParameter

    storage_client = None

    def new(self, cfg, *args, **kwargs):
        """Method to construct class

        :rtype: GoogleStorageSecretProvider
        :param cfg: Provider configuration
        :return: GoogleStorageSecretProvider
        """
        super(GoogleStorageSecretProvider, self).new(cfg, *args, **kwargs)

        c = self.cfg[0]

        project = c.project
        scopes = ['https://www.googleapis.com/auth/devstorage.read_only']

        if c.serviceAccountFile:
            credentials = service_account.Credentials.from_service_account_file(
                os.path.expanduser(c.serviceAccountFile),
                scopes=scopes
            )
            _project = service_account.Credentials.project_id

            if credentials.requires_scopes:
                credentials = credentials.with_scopes(scopes)
        else:
            credentials, _project = google.auth.default(scopes=scopes)

        if not project:
            project = _project

        self.log.debug("Going to use following project: %s" % project)
        self.storage_client = storage.Client(credentials=credentials, project=project)

        return self

    @property
    @logthis()
    def value(self):
        """value property

        :rtype:
        :return: Secret value
        """

        bucket = self.storage_client.bucket(self.parameters[0]['bucket'])
        blob = bucket.get_blob(self.parameters[0]['object'])

        assert_that(blob, "GCS blob response should not be empty")

        return unicode(blob.download_as_string())
