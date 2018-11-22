import json
import sys
_, s3_bucket_name, k8s_cluster_name = sys.argv

private_ca_path = "/".join([s3_bucket_name,k8s_cluster_name,"pki/private/ca"])
issued_ca_path = "/".join([s3_bucket_name,k8s_cluster_name,"pki/issued/ca"])

with open("cluster.json", 'r') as fp:
    data = fp.read()
json_data = json.loads(data)

json_data["spec"]["kubeAPIServer"] = {"admissionControl":["NamespaceLifecycle", "LimitRanger", "ServiceAccount", "PersistentVolumeLabel", "DefaultStorageClass",
                                                         "DefaultTolerationSeconds", "MutatingAdmissionWebhook", "ValidatingAdmissionWebhook", "ResourceQuota",
                                                         "NodeRestriction", "Priority"]}
hooks_data = {}
json_data["spec"]["hooks"] = [hooks_data]
hooks_data["name"] = "kops-hook-s3-config.service"
hooks_data["before"] = ["kubelet.service"]
hooks_data["manifest"] = "\n".join(["[Unit]", "Description=Copy config files from s3", "[Service]", "Type=oneshot", "ExecStart=aws s3 cp --recursive s3://{} /tmp".format(private_ca_path), "ExecStart=aws s3 cp --recursive s3://{} /tmp".format(issued_ca_path)])
with open('cluster_new.json', 'w') as outfile:
    json.dump(json_data, outfile)
