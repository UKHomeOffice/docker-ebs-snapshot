import boto3
import collections
import datetime
import re
from botocore.exceptions import ClientError

# Set default retention days
retention_days = 10

ec = boto3.client('ec2')

# Find volumes with tag = backup
volumes_to_backup = ec.describe_volumes(Filters=[
                        {'Name': 'tag-key', 'Values': ['backup', 'Backup']},
                    ])

to_tag = collections.defaultdict(list)

# If Rentention is set, use it
for volume in (volumes_to_backup["Volumes"]):
    try:
        for t in volume['Tags']:
            if t['Key'] == 'Retention':
                retention_days = int(t['Value'])
    except ClientError as e:
        print "using default retention"

    vol_id = volume['VolumeId']

    snap = ec.create_snapshot(
        VolumeId=vol_id,
    )

    # Add tags from the original volume
    ec.create_tags(
        Resources=[snap['SnapshotId']],
        Tags=volume['Tags'],
    )

    to_tag[retention_days].append(snap['SnapshotId'])

    print "Retaining snapshot %s of volume %s for %d days" % (
        snap['SnapshotId'],
        vol_id,
        retention_days,
    )

    for retention_days in to_tag.keys():
        delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
        delete_fmt = delete_date.strftime('%Y-%m-%d')

        print "Will delete %d snapshots on %s" % (len(to_tag[retention_days]), delete_fmt)
        ec.create_tags(
            Resources=to_tag[retention_days],
            Tags=[{'Key': 'DeleteOn', 'Value': delete_fmt}],
        )

    # Delete snapshots with a delete on = today
    delete_on = datetime.date.today().strftime('%Y-%m-%d')
    filters = [
        {'Name': 'tag-key', 'Values': ['DeleteOn']},
        {'Name': 'tag-value', 'Values': [delete_on]},
    ]
    snapshot_response = ec.describe_snapshots(Filters=filters)

    for snap in snapshot_response['Snapshots']:
        print "Deleting snapshot %s" % snap['SnapshotId']
        ec.delete_snapshot(SnapshotId=snap['SnapshotId'])
