import sys  
import subprocess  
import logging  
import boto3  
import requests
import traceback
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

if __name__ == '__main__':
  _, zone_id, domain_name = sys.argv
  namespace = "etcdpwx"
  az = get_az()
  private_ip = get_private_ip()
  recordname = "{}-{}.{}".format( namespace, az, domain_name)
  try:
      change_hostname(namespace, az, domain_name)
      resp = update_dns_record(zone_id, namespace, "A", domain_name, az, "300", private_ip)
  except Exception as e:
    traceback.print_exc()
