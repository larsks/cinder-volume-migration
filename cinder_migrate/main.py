# type: ignore
import click
import logging
import logging.config

from . import openstack

LOG = logging.getLogger(__name__)


def configure_logging(verbose):
    loglevel = ["WARNING", "INFO", "DEBUG"][min(verbose, 2)]

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s %(levelname)s %(name)s: %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "level": loglevel,
                    "formatter": "standard",
                    "class": "logging.StreamHandler",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["default"],
                    "level": "WARNING" if verbose <= 2 else "DEBUG",
                    "propagate": False,
                },
                __name__.split(".")[0]: {
                    "handlers": ["default"],
                    "level": loglevel,
                    "propagate": True,
                },
            },
        }
    )


@click.command()
@click.option("--verbose", "-v", count=True)
@click.option("--force", is_flag=True)
@click.option("--to", "-t", "cloud_dst", required=True)
@click.option("--from", "-f", "cloud_src", required=True)
@click.option("--backup-id", "-b", required=True)
def main(verbose, force, cloud_src, cloud_dst, backup_id):
    configure_logging(verbose)

    src = openstack.Openstack(cloud_src)
    dst = openstack.Openstack(cloud_dst)

    LOG.info("getting backup record for backup id %s", backup_id)
    record = src.export_backup_record(backup_id)

    LOG.info("checking for existing backup in %s", dst.cloud_name)
    if dst.metadata_exists(record) and not force:
        LOG.error("backup already exists on destination")
        raise click.Abort()

    LOG.info("prepare %s to receive backup %s", dst.cloud_name, backup_id)
    dst.prepare_receive_container(record)

    metadata = src.get_backup_metadata(record)
    for obj in metadata.objects:
        path = list(obj.keys())[0]
        LOG.info("copy %s from %s to %s", path, src.cloud_name, dst.cloud_name)
        dst.copy_object(record, src, path)

    LOG.info("copy backup metadata from %s to %s", src.cloud_name, dst.cloud_name)
    dst.copy_object(record, src, record.info.metadata_key)
    LOG.info("copy backup sha256file from %s to %s", src.cloud_name, dst.cloud_name)
    dst.copy_object(record, src, record.info.sha256file_key)

    LOG.info("attempt to import backup record to %s", dst.cloud_name)
    res = dst.import_backup_record(record)

    # XXX: this is just for debugging
    print(res)


if __name__ == "__main__":
    main()
