from __future__ import annotations

import base64
import functools
import json

from pydantic import Field
from typing import Literal

from .backupinfoswift import BackupInfoSwift
from .base import BaseModel


class BackupRecord(BaseModel):
    backup_service: str
    backup_url: str


class SwiftBackupRecord(BackupRecord):
    backup_service: Literal["cinder.backup.drivers.swift.SwiftBackupDriver"]

    @functools.cached_property
    def info(self):
        return BackupInfoSwift(**json.loads(base64.b64decode(self.backup_url)))


class BackupRecordResponse(BaseModel):
    backup_record: SwiftBackupRecord = Field(alias="backup-record")

    class Config:
        allow_population_by_field_name = True
