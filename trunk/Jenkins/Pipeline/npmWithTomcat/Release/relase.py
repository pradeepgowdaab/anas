from xml.etree import ElementTree as et
import requests
import sys
from requests.auth import HTTPBasicAuth
import os.path
from os import path

if __name__ == "__main__":
    ns = "http://maven.apache.org/POM/4.0.0"
    group = artifact = version = ""
    filename = sys.argv[1]
    module = sys.argv[2]
   # release = sys.argv[3]
    tree = et.ElementTree()
    tree.parse("/opt/jenkins/workspace/" + filename + "/pom.xml")

    p = tree.getroot().find("{%s}parent" % ns)

    if p is not None:
      if p.find("{%s}groupId" % ns) is not None:
        group = p.find("{%s}groupId" % ns).text

      if p.find("{%s}version" % ns) is not None:
        version = p.find("{%s}version" % ns).text

    if tree.getroot().find("{%s}groupId" % ns) is not None:
      group = tree.getroot().find("{%s}groupId" % ns).text

    if tree.getroot().find("{%s}artifactId" % ns) is not None:
      artifact = tree.getroot().find("{%s}artifactId" % ns).text
    
    if tree.getroot().find("{%s}packaging" % ns) is not None:
      package = tree.getroot().find("{%s}packaging" % ns).text

    if tree.getroot().find("{%s}version" % ns) is not None:
      version = tree.getroot().find("{%s}version" % ns).text

    print(group, artifact, version, package)
    build_name = artifact+"."+package
    build_path1 = "/opt/jenkins/workspace/" + filename + "/target/" + artifact+"-"+version+"."+package
    build_path2 = "/opt/jenkins/workspace/" + filename + "/target/" + artifact+"."+package
    group_name = group.replace(".", "/")
    if path.isfile(build_path1):
        print build_path1
        url = "http://192.168.1.143:8081/repository/trinityAnalytics_Product/QA/release"+"/"+module+"/"+artifact+"/"+version+"/"+artifact+"."+package
        response = requests.put(url, auth=HTTPBasicAuth('admin', 'TrInItY123'), data=open(build_path1,'r').read())
        url2 = "http://192.168.1.143:8081/repository/trinityAnalytics_Product/QA/latest"+"/"+module+"/"+artifact+"."+package
        response2 = requests.put(url2, auth=HTTPBasicAuth('admin', 'TrInItY123'), data=open(build_path1,'r').read())
    elif path.isfile(build_path2):
        print build_path2
        url = "http://192.168.1.143:8081/repository/trinityAnalytics_Product/QA/release"+"/"+module+"/"+artifact+"/"+version+"/"+artifact+"."+package
        response = requests.put(url, auth=HTTPBasicAuth('admin', 'TrInItY123'), data=open(build_path2,'r').read())
        url2 = "http://192.168.1.143:8081/repository/trinityAnalytics_Product/QA/latest"+"/"+module+"/"+artifact+"."+package
        response2 = requests.put(url2, auth=HTTPBasicAuth('admin', 'TrInItY123'), data=open(build_path2,'r').read())
