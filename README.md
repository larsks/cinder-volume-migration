# cinder-migrate

## Requirements

- Both your source and destination environment must have the Cinder backup service enabled.
- Non-admin users must be able to run the `backup record export`/`backup record import` commands.

## Example

Assuming you have created a backup by running the `openstack volume backup create` command:

```
$ openstack --os-cloud src-cloud volume backup list
+--------------------------------------+--------------------+-------------+-----------+------+
| ID                                   | Name               | Description | Status    | Size |
+--------------------------------------+--------------------+-------------+-----------+------+
| b37f840d-6fd3-4de3-a6ed-985a6f6a40a8 | vol0-20220317-2321 | None        | available |    2 |
+--------------------------------------+--------------------+-------------+-----------+------+
```

You can migrate that backup to a selected target environment like this:

```
cinder-migrate -v \
  --from src-cloud \
  --to dest-cloud \
  -b b37f840d-6fd3-4de3-a6ed-985a6f6a40a8
```

Where `src-cloud` and `dest-cloud` are the names of OpenStack environments from your `clouds.yaml` file.
