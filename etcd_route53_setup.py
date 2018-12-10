import sys  
import subprocess  
import logging  
import boto3  
import requests
import traceback
import ConfigParser

METADATA_API = 'http://169.254.169.254/latest'  

def get_az():  
  return requests.get(
      "{}/meta-data/placement/availability-zone/".format(METADATA_API)
  ).text

def get_private_ip():  
  return requests.get(
      "{}/meta-data/local-ipv4/".format(
          METADATA_API
      )
  ).text

def change_hostname(namespace, az, domain):  
  newhostname = "{}-{}.{}".format(namespace, az, domain)

  subprocess.call(['hostname', newhostname])
  with open('/etc/hostname', 'w+') as f:
      f.write(newhostname)
      f.truncate()
      f.close()


def update_dns_record(zoneid, namespace, recordtype, domain, az, ttl, value):  
  client = boto3.client('route53')

  resp = client.change_resource_record_sets(
      HostedZoneId=zoneid,
      ChangeBatch={
          'Comment': 'Updating record',
          'Changes': [
              {
                  'Action': 'UPSERT',
                  'ResourceRecordSet': {
                      'Name': "{}-{}.{}".format(
                          namespace, az, domain
                      ),
                      'Type': recordtype,
                      'TTL': int(ttl),
                      'ResourceRecords': [
                          {
                              'Value': value
                          }
                      ]
                  }
              }
          ]
      }
  )
  return resp['ResponseMetadata']['HTTPStatusCode']

def create_systemd_file(domain_name, private_ip):
  config = ConfigParser.RawConfigParser()
  config.optionxform = str
  config.add_section('Unit')
  config.set('Unit', 'Description', 'etcd Daemon')
  config.set("Unit", "After", "network.target")
  config.add_section('Service')
  config.set("Service", "Type", "notify")
  config.set("Service", "Restart", "always")
  config.set("Service", "RestartSec", "25s")
  config.set("Service", "LimitNOFILE", "40000")
  config.set("Service", "TimeoutStartSec", "20s")
  config.add_section('Install')
  config.set("Install", "WantedBy", "multi-user.target")
  config.set("Service", "ExecStart", "/usr/local/bin/etcd -discovery-srv {} --initial-advertise-peer-urls http://{}:2380 --advertise-client-urls http://{}:2379 --listen-client-urls http://0.0.0.0:2379 --listen-peer-urls http://0.0.0.0:2380 --data-dir /var/cache/etcd/state --name %H --initial-cluster-token my-etcd-token --initial-cluster-state new".format(domain_name, private_ip, private_ip))
  with open('/etc/systemd/system/etcd3.service', 'w') as configfile:
    config.write(configfile)
  
def run_etcd():
  subprocess.call(["systemctl", "daemon-reload"])
  subprocess.call(["systemctl", "enable", "etcd3"])
  subprocess.call(["systemctl", "start", "etcd3"])

if __name__ == '__main__':
  _, zone_id, domain_name = sys.argv
  namespace = "etcdpwx"
  az = get_az()
  private_ip = get_private_ip()
  recordname = "{}-{}.{}".format( namespace, az, domain_name)
  try:
      change_hostname(namespace, az, domain_name)
      resp = update_dns_record(zone_id, namespace, "A", domain_name, az, "300", private_ip)
      create_systemd_file(domain_name, private_ip)
      run_etcd()
  except Exception as e:
    traceback.print_exc()
