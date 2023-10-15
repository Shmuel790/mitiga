"""A Kubernetes Python Pulumi program"""

import os
import pulumi
from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Service, ConfigMap
from pulumi_kubernetes.core.v1 import PersistentVolumeClaim

app_name = "nginx"

# Read in your index.html file
with open("./index.html", "r", encoding="utf-8") as f:
    file_content = f.read()
    
#Create ConfigMap
configmap = ConfigMap(
    "nginx-index",
    data={"index.html": file_content}
)


# Create a PVC for persistent volume
pvc = PersistentVolumeClaim(
    app_name,
    spec={
        "accessModes": ["ReadWriteOnce"],
        "resources": {"requests": {"storage": "1Gi"}}
    })

# nginx Deployment
dep = Deployment(
    app_name,
    spec={
        "selector": {"matchLabels": {"app": app_name}},
        "replicas": 4,
        "template": {
            "metadata": {"labels": {"app": app_name}},
            "spec": {
                "containers": [{
                    "name": app_name,
                    "image": "nginx:latest",
                    "resources": {
                        "requests": {"cpu": "250m", "memory": "64Mi"},
                        "limits": {"cpu": "500m", "memory": "128Mi"}},
                    "volumeMounts": [
                        {
                        "mountPath": "/usr/share/nginx/html",
                        "name": "wwwdata"
                        },
                        {
                        "mountPath": "/usr/share/nginx/html/index.html",
                        "name": "indexhtml",
                        "subPath": "index.html"
                        }]
                }],
                "volumes": [{
                    "name": "wwwdata",
                    "persistentVolumeClaim": {"claimName": pvc.metadata["name"]}
                },
                {
                    "name": "indexhtml",
                    "configMap": {
                        "name": configmap.metadata["name"]
                    }
                }]
            }
        }
    }
)

# nginx Service
svc = Service(app_name, 
    spec={
        "type": "ClusterIP",
        "selector": {"app": app_name},
        "ports": [
            {
                "name": "http", 
                "port": 80,
                "targetPort": 80
            },
            {   
                "name": "https",
                "port": 443,
                "targetPort": 443
            }
        ]
    }
)

# Export the KubeConfig output
pulumi.export("kubeconfig", dep)