<<<<<<< HEAD
### 🏠 Helm From Scratch - Home Assignment
#### 🎯 Project Overview
This project demonstrates the creation of a comprehensive Helm chart from scratch. It deploys a containerized application (hashicorp/http-echo) alongside various Kubernetes resources to demonstrate orchestration, configuration management, and lifecycle handling using Helm.

## 📦 Kubernetes Resources & Purpose

| Resource | Purpose |
| :--- | :--- |
| **Deployment** | Manages the `http-echo` application pods, ensuring the desired number of replicas are running. |
| **Service** | Provides a stable internal IP and port to access the application pods. |
| **DaemonSet** | Runs an instance of the application on every node in the cluster for logging/monitoring simulation. |
| **CronJob** | Scheduled task that runs a `busybox` container every 5 minutes (configurable). |
| **Job** | A one-time execution task that runs once upon deployment and then terminates. |
| **ConfigMap** | Stores non-sensitive configuration like the echo text and port number. |
| **Secret** | Manages sensitive data (API Tokens) using Kubernetes Secrets. |
## 🛠️ Commands Used
### 1. Installation & Initialization
To install the chart for the first time or update an existing one:
> Bash
```
helm upgrade --install myapp ./charts/myapp
```

### 2. Version Upgrade
After updating the image.tag in values.yaml:
> Bash
```
# This creates a new revision in Helm history
helm upgrade --install myapp ./charts/myapp
```
### 3. Lifecycle Management
To view the history of releases and perform a rollback:
> Bash
```
** Check all revisions
helm history myapp

** Rollback to the very first version
helm rollback myapp 1
```

### 4. Bonus: External Chart
To add a dependency and install it:
> Bash
```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm upgrade --install external-nginx bitnami/nginx --set image.tag=1.23.0
```
## 🔍 Verification Steps
Run these commands to verify that the deployment was successful:

1. Check Resource Status

> Bash
```
** View all created resources
kubectl get all -l app.kubernetes.io/instance=myapp

** Specifically check the DaemonSet and CronJob
kubectl get ds,cronjob,job
```

### 2. Verify Configuration (ConfigMap & Secret)

> Bash
```
# Check if the ConfigMap holds the correct values
kubectl describe configmap myapp-config

# Decode the Secret to verify the API Token
kubectl get secret myapp-secret -o jsonpath='{.data.API_TOKEN}' | base64 --decode
```

### 3. Test Application Output
Use port-forwarding to access the echo server:

> Bash
```
kubectl port-forward svc/myapp-service 5678:5678
```

### 4. Inspect Logs
Check if the Job or CronJob executed correctly:

> Bash
```
kubectl logs -l job-name=myapp-one-time-job
```

📁 Repository Structure
* charts/myapp/: The complete Helm chart.
* outputs/: Logs of the commands executed during the assignment.
* answers.md: Detailed theoretical explanations of the Helm lifecycle and templates.
=======
### 🏠 Helm From Scratch - Home Assignment
#### 🎯 Project Overview
This project demonstrates the creation of a comprehensive Helm chart from scratch. It deploys a containerized application (hashicorp/http-echo) alongside various Kubernetes resources to demonstrate orchestration, configuration management, and lifecycle handling using Helm.

## 📦 Kubernetes Resources & Purpose

| Resource | Purpose |
| :--- | :--- |
| **Deployment** | Manages the `http-echo` application pods, ensuring the desired number of replicas are running. |
| **Service** | Provides a stable internal IP and port to access the application pods. |
| **DaemonSet** | Runs an instance of the application on every node in the cluster for logging/monitoring simulation. |
| **CronJob** | Scheduled task that runs a `busybox` container every 5 minutes (configurable). |
| **Job** | A one-time execution task that runs once upon deployment and then terminates. |
| **ConfigMap** | Stores non-sensitive configuration like the echo text and port number. |
| **Secret** | Manages sensitive data (API Tokens) using Kubernetes Secrets. |
## 🛠️ Commands Used
### 1. Installation & Initialization
To install the chart for the first time or update an existing one:
```
Bash
helm upgrade --install myapp ./charts/myapp
```

### 2. Version Upgrade
After updating the image.tag in values.yaml:
```
Bash
** This creates a new revision in Helm history
helm upgrade --install myapp ./charts/myapp
```
### 3. Lifecycle Management
To view the history of releases and perform a rollback:
```
Bash
** Check all revisions
helm history myapp

** Rollback to the very first version
helm rollback myapp 1
```

### 4. Bonus: External Chart
To add a dependency and install it:
```
Bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm upgrade --install external-nginx bitnami/nginx --set image.tag=1.23.0
```
## 🔍 Verification Steps
Run these commands to verify that the deployment was successful:
1. Check Resource Status
```
Bash
** View all created resources
kubectl get all -l app.kubernetes.io/instance=myapp

** Specifically check the DaemonSet and CronJob
kubectl get ds,cronjob,job
```
### 2. Verify Configuration (ConfigMap & Secret)
```
```
Bash
** Check if the ConfigMap holds the correct values
kubectl describe configmap myapp-config

** Decode the Secret to verify the API Token
kubectl get secret myapp-secret -o jsonpath='{.data.API_TOKEN}' | base64 
--decode
```
### 3. Test Application OutputUse port-forwarding to access the echo server:
```
Bash
kubectl port-forward svc/myapp-service 5678:5678
```
### 4. Inspect Logs
Check if the Job or CronJob executed correctly:
---
Bash
kubectl logs -l job-name=myapp-one-time-job
```
📁 Repository Structure
* charts/myapp/: The complete Helm chart.
* outputs/: Logs of the commands executed during the assignment.
* answers.md: Detailed theoretical explanations of the Helm lifecycle and templates.
>>>>>>> e77980a1cc60260ae22a93ca4fe29780549f1ac2
