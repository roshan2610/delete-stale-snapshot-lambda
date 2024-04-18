#Importing boto3 module which will talk to AWS APIs
import boto3

#creating lambda_handler function which works as an entry point 
def lambda_handler(event, context):
    
    #Created ec2 client object
    ec2 = boto3.client('ec2')
    
    #Retrieve the information about snapshots associated with ec2
    response = ec2.describe_snapshots(OwnerIds=['self'])
    
    #Retrieve the information about running instances
    instances_response = ec2.describe_instances(Filters = [{'Name':'instance-state-name', 'Values': ['running']}])
    #Created a set() to store instance ids
    active_instance_ids = set()

    #Traverse through the instance_response and add instance ids to the set
    for reservation in instances_response['Reservations']:
        for instance in reservation['Instances']:
            active_instance_ids.add(instance['InstanceId'])

    #Taken the snapshot id and volume id from snapshot information
    for snapshot in response['Snapshots']:
        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')

        #Checks whether volume is there for the snapshot or not, if volume not present then delete the snapshot
        if not volume_id:
            ec2.delete_snapshot(SnapshotId = snapshot_id)
            print(f"Deleted EBS {snapshot_id} as it was not attached to any volume.")
        
        else:
            try:
                #Describing volume information
                volume_response = ec2.describe_volumes(VolumeIds = [volume_id])
                #If there are no attachments found for the volume, then delete the snapshot as volume is not associated with any running instance
                if not volume_response['Volumes'][0]['Attachments']:
                    ec2.delete_snapshot(SnapshotId = snapshot_id)
                    print(f"Deleted EBS {snapshot_id} as associated volume has not attached to any running instance.")
            
            except ec2.exceptions.ClientError as e:
                #Checks if volume does not found then will delete the snapshot
                if e.response['Error']['Code'] == 'InvalidVolume.NotFound':
                    ec2.delete_snapshot(SnapshotId = snapshot_id)
                    print(f"Deleted EBS {snapshot_id} as associated volume does not found.")
        
