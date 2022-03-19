# type: ignore
import functools
import json
import logging
import openstack

from . import models


LOG = logging.getLogger(__name__)


class Openstack:
    def __init__(self, cloud_name):
        self.cloud_name = cloud_name
        self.conn = openstack.connect(cloud=cloud_name)
        LOG.debug(
            "connected to %s as user %s project %s",
            self.cloud_name,
            self.conn.current_user_id,
            self.conn.current_project_id,
        )

    @functools.cached_property
    def cinder_endpoint(self):
        endpoint = self.conn.endpoint_for("volumev3")
        LOG.debug("found endpoint %s for cinder @ %s", endpoint, self.cloud_name)
        return endpoint

    def export_backup_record(self, backupid):
        url = f"{self.cinder_endpoint}/backups/{backupid}/export_record"
        res = self.conn.session.get(url)
        res.raise_for_status()
        return models.BackupRecordResponse(**res.json()).backup_record

    def import_backup_record(self, record):
        body = models.BackupRecordResponse(backup_record=record)
        url = f"{self.cinder_endpoint}/backups/import_record"
        res = self.conn.session.post(
            url, json=body.dict(by_alias=True, exclude={"info"})
        )
        res.raise_for_status()
        return res.json()

    def metadata_exists(self, record):
        container = record.info.container
        res = self.conn.get_object(container, record.info.metadata_key)
        if res is None:
            return False
        return True

    def get_backup_metadata(self, record):
        container = record.info.container
        res = self.conn.get_object(container, record.info.metadata_key)
        return models.BackupMetadata(**json.loads(res[1]))

    def prepare_receive_container(self, record):
        container = self.conn.get_container(record.info.container)
        if container is None:
            LOG.debug(
                "create target container %s on %s", record["container"], self.cloud_name
            )
            self.conn.create_container(record["container"])

    def copy_object(self, record, src, key):
        res = src.conn.get_object_raw(record.info.container, key)
        res.raise_for_status()
        self.conn.create_object(
            record.info.container,
            key,
            data=res.content,
            md5=res.headers["etag"],
        )
