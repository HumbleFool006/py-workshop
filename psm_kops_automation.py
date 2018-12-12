import json
import sys
_, s3_bucket_name, k8s_cluster_name, nat1, nat2, nat3, sshKeyName, role = sys.argv

private_ca_path = "/".join([s3_bucket_name,k8s_cluster_name,"pki/private/ca"])
issued_ca_path = "/".join([s3_bucket_name,k8s_cluster_name,"pki/issued/ca"])

nat_map = {}
nat_map[nat1.split(",")[0]] = nat1.split(",")[1]
nat_map[nat2.split(",")[0]] = nat2.split(",")[1]
nat_map[nat3.split(",")[0]] = nat3.split(",")[1]


with open("cluster.json", 'r') as fp:
    data = fp.read()
json_data = json.loads(data)

#egress mapping
[data.update({"egress": nat_map[data["id"]]}) for data in json_data["spec"]["subnets"] if data["id"] in nat_map]

#kubeapiserver for istio and aws iam authenticator
json_data["spec"]["kubeAPIServer"] = {"admissionControl":["NamespaceLifecycle", "LimitRanger", "ServiceAccount", "PersistentVolumeLabel", "DefaultStorageClass",
                                                         "DefaultTolerationSeconds", "MutatingAdmissionWebhook", "ValidatingAdmissionWebhook", "ResourceQuota",
                                                         "NodeRestriction", "Priority"], "authenticationTokenWebhookConfigFile": "/srv/kubernetes/heptio-authenticator-aws/kubeconfig.yaml"}
#sshKeyName
json_data["spec"]["sshKeyName"] = sshKeyName
#hooks data for kops-k8s ca
k8s_ca = {}
iam_authenticator = {}
sudo_access_removal = {}
json_data["spec"]["additionalPolicies"] = {}
json_data["spec"]["additionalPolicies"]["node"] = '[{"Effect": "Allow",  "Action": ["ec2:AttachVolume", "ec2:DetachVolume", "ec2:CreateTags",  "ec2:CreateVolume", "ec2:DeleteTags", "ec2:DeleteVolume", "ec2:DescribeTags", "ec2:DescribeVolumeAttribute", "ec2:DescribeVolumesModifications", "ec2:DescribeVolumeStatus", "ec2:DescribeVolumes", "ec2:DescribeInstances"], "Resource": [ "*" ]}]'
json_data["spec"]["hooks"] = [k8s_ca, iam_authenticator, sudo_access_removal]
k8s_ca["name"] = "k8s-ca-config.service"
k8s_ca["before"] = ["kubelet.service"]
k8s_ca["manifest"] = "\n".join(["[Unit]", "Description=Copy config files from s3 for k8s-ca", "[Service]", "Type=oneshot", "ExecStart=/usr/local/bin/aws s3 cp --recursive s3://{} /tmp".format(private_ca_path), "ExecStart=/usr/local/bin/aws s3 cp --recursive s3://{} /tmp".format(issued_ca_path)])
iam_authenticator["name"] = "iam-auth-config.service"
iam_authenticator["before"] = ["kubelet.service"]
iam_authenticator["manifest"] = "\n".join(["[Unit]", "Description=Copy config files from s3 for iam auth", "[Service]", "Type=oneshot", "ExecStart=/bin/mkdir -p /srv/kubernetes/heptio-authenticator-aws","ExecStart=/usr/local/bin/aws s3 cp --recursive s3://{}/{}/addons/authenticator /srv/kubernetes/heptio-authenticator-aws/".format(s3_bucket_name, k8s_cluster_name)])
sudo_access_removal["name"] = "sudo-access-removal.service"
sudo_access_removal["before"] = ["kubelet.service"]
sudo_access_removal["manifest"] = "\n".join(["[Unit]", "Description=Remove sudo access", "[Service]", "Type=oneshot", "ExecStart=/bin/rm -f /etc/sudoers.d/*"])

with open('cluster_new.json', 'w') as outfile:
    json.dump(json_data, outfile)
