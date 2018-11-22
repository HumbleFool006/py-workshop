import json
import sys
_, s3_bucket_name, k8s_cluster_name, nat1, nat2, nat3 = sys.argv

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

#kubeapiserver for istio
json_data["spec"]["kubeAPIServer"] = {"admissionControl":["NamespaceLifecycle", "LimitRanger", "ServiceAccount", "PersistentVolumeLabel", "DefaultStorageClass",
                                                         "DefaultTolerationSeconds", "MutatingAdmissionWebhook", "ValidatingAdmissionWebhook", "ResourceQuota",
                                                         "NodeRestriction", "Priority"]}
#hooks data for kops-k8s ca
hooks_data = {}
json_data["spec"]["hooks"] = [hooks_data]
hooks_data["name"] = "kops-hook-s3-config.service"
hooks_data["before"] = ["kubelet.service"]
hooks_data["manifest"] = "\n".join(["[Unit]", "Description=Copy config files from s3", "[Service]", "Type=oneshot", "ExecStart=aws s3 cp --recursive s3://{} /tmp".format(private_ca_path), "ExecStart=aws s3 cp --recursive s3://{} /tmp".format(issued_ca_path)])

with open('cluster_new.json', 'w') as outfile:
    json.dump(json_data, outfile)
