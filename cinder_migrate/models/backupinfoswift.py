# generated by datamodel-codegen:
#   filename:  record.json
#   timestamp: 2022-03-19T00:25:38+00:00

from __future__ import annotations

import functools

from .base import BaseModel


class BackupInfoSwift(BaseModel):
    status: str | None
    temp_snapshot_id: str | None
    display_name: str | None
    availability_zone: str | None
    deleted: bool
    volume_id: str | None
    restore_volume_id: str | None
    updated_at: str | None
    host: str | None
    snapshot_id: str | None
    user_id: str | None
    service_metadata: str | None
    id: str | None
    size: int
    object_count: int
    deleted_at: str | None
    container: str | None
    service: str | None
    driver_info: dict[str, str]
    created_at: str | None
    display_description: str | None
    data_timestamp: str | None
    temp_volume_id: str | None
    parent_id: str | None
    encryption_key_id: str | None
    num_dependent_backups: int
    fail_reason: str | None
    project_id: str | None
    metadata: dict[str, str]

    @functools.cached_property
    def metadata_key(self):
        return f"{self.service_metadata}_metadata"

    @functools.cached_property
    def sha256file_key(self):
        return f"{self.service_metadata}_sha256file"
