import yaml
import json
json_data = {}
final_data = {}
with open('/home/ec2-user/.kube/config', 'r') as fp:
  json_data = yaml.load(fp)
final_data["kind"] = "Config"
final_data["current-context"] = json_data["current-context"]
final_data["contexts"] = [json_data["contexts"][0]]
final_data["contexts"]["0"]["user"] = "helm.exec"
final_data_context = json_data["contexts"][0]
final_data["clusters"] = [json_data["clusters"][0]]
user_data = {}
final_data["users"] = [user_data]
user_data["name"] = "helm.exec"
user_data["user"] = {}
user_data["user"]["exec"] = {}
user_data["user"]["exec"]["apiVersion"] = "client.authentication.k8s.io/v1alpha1"
user_data["user"]["exec"]["command"] = "heptio-authenticator-aws"
user_data["user"]["exec"]["args"] = [ "token", "-i", "helm", "-r", "arn:aws:iam::642731736239:role/K8s-cicd-KopsRole" ]
user_data["user"]["exec"]["apiVersion"] = "client.authentication.k8s.io/v1alpha1"

with open('kubectl_config', 'w') as fp:
  fp.write(yaml.dump(final_data, default_flow_style=False))
