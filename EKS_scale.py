import boto3
import argparse

def get_nodegroup_info(eks_client, cluster_name, nodegroup_name):
    try:
        response = eks_client.describe_nodegroup(
            clusterName=cluster_name,
            nodegroupName=nodegroup_name
        )
        return response['nodegroup']
    except Exception as e:
        print(f"❌ Error fetching node group: {e}")
        return None

def validate_tags(tags, required_tags):
    return all(tags.get(k) == v for k, v in required_tags.items())

def update_nodegroup_capacity(eks_client, cluster_name, nodegroup_name, min_size, desired_size):
    try:
        eks_client.update_nodegroup_config(
            clusterName=cluster_name,
            nodegroupName=nodegroup_name,
            scalingConfig={
                'minSize': min_size,
                'desiredSize': desired_size
                # maxSize remains unchanged
            }
        )
        print(f"✅ Updated node group '{nodegroup_name}' (min={min_size}, desired={desired_size})")
    except Exception as e:
        print(f"❌ Error updating scaling config: {e}")

def main():
    parser = argparse.ArgumentParser(description="Update EKS Node Group scaling config if tags match.")
    parser.add_argument('--cluster', required=True, help="EKS Cluster Name")
    parser.add_argument('--nodegroup', required=True, help="Node Group Name")
    parser.add_argument('--key1', required=True, help="First tag key")
    parser.add_argument('--value1', required=True, help="First tag value")
    parser.add_argument('--key2', required=True, help="Second tag key")
    parser.add_argument('--value2', required=True, help="Second tag value")
    parser.add_argument('--min', type=int, required=True, help="Minimum capacity to set")
    parser.add_argument('--desired', type=int, required=True, help="Desired capacity to set")

    args = parser.parse_args()

    eks = boto3.client('eks')

    ng_info = get_nodegroup_info(eks, args.cluster, args.nodegroup)
    if not ng_info:
        return

    tags = ng_info.get('tags', {})
    required = {args.key1: args.value1, args.key2: args.value2}

    if not validate_tags(tags, required):
        print("❌ Required tags not found. Aborting scaling operation.")
        return

    update_nodegroup_capacity(eks, args.cluster, args.nodegroup, args.min, args.desired)

if __name__ == "__main__":
    main()
