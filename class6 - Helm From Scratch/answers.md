# Part 1 – Create Helm Chart

## explain each  templates

### * Deployment
- The Deployment is the manager of your Pods. It is responsible for the Desired State of the application.
- It makes sure that there are always X replicas (copies) running. If a Pod crashes, the Deployment will create a new one in its place.

### * Service
- The Service is the internal Load Balancer.
- Since Pods are temporary and their IP address changes, the Service provides a permanent IP and DNS address (e.g. myapp-service). It routes the traffic that comes to it to the correct Pods according to Labels.

### * DaemonSet
- Similar to Deployment, but with different legality: it runs one copy of the Pod on each Node (server) in the Cluster.

- Typically used for infrastructure tasks such as log collection (Fluentd), monitoring (Prometheus Node Exporter) or network management.

### * CronJob
Like the "Scheduler".

- It runs tasks based on time (for example: every day at 12 midnight, or every 5 minutes). It does not run a regular Pod, but creates a Job according to the schedule you set.

### * Job - a one-time task.

- Unlike Deployment, which wants the Pod to run forever, the Job runs a Pod until it finishes its operation and then stops.

- Suitable for running database migrations, cleaning temporary files or spot data processing.

### * ConfigMap
- Separates the configuration from the code. Instead of hardcoding text or ports within the Image, we store them here. Allows you to update the text in the ConfigMap and perform a new Deployment without building a new Docker Image.

### * Secret
- Similar to ConfigMap, but intended for sensitive information.
Used to store passwords, tokens (API Tokens) and encryption keys. In Kubernetes, the information is encoded in Base64 and access to it can be restricted to a stricter level of permissions.



# Part 2 – Deploy the Chart
```
PS C:\Users\repo\DevOps\devops-course\class6 - Helm From Scratch> kubectl get all
NAME                                     READY   STATUS             RESTARTS      AGE
pod/my-release-my-app-6db96b8ccc-2x8p7   1/1     Running            1 (23h ago)   5d23h
pod/myapp-deploy-745ff694b8-g79n9        0/1     ImagePullBackOff   0             3m13s
pod/myapp-logger-t6dx6                   1/1     Running            0             3m13s
pod/myapp-setup-job-vg2wl                0/1     Completed          0             3m13s

NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
service/kubernetes          ClusterIP   10.96.0.1       <none>        443/TCP   14d
service/my-release-my-app   ClusterIP   10.99.3.40      <none>        80/TCP    5d23h
service/myapp-service       ClusterIP   10.111.85.157   <none>        80/TCP    3m14s

NAME                          DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
daemonset.apps/myapp-logger   1         1         1       1            1           <none>          3m14s

NAME                                READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/my-release-my-app   1/1     1            1           5d23h
deployment.apps/myapp-deploy        0/1     1            0           3m14s

NAME                                           DESIRED   CURRENT   READY   AGE
replicaset.apps/my-release-my-app-6db96b8ccc   1         1         1       5d23h
replicaset.apps/myapp-deploy-745ff694b8        1         1         0       3m14s

NAME                        STATUS     COMPLETIONS   DURATION   AGE
job.batch/myapp-setup-job   Complete   1/1           9s         3m14s
PS C:\Users\repo\DevOps\devops-course\class6 - Helm From Scratch> kubectl get configmap
NAME               DATA   AGE
kube-root-ca.crt   1      14d
myapp-cm           1      3m14s
PS C:\Users\repo\DevOps\devops-course\class6 - Helm From Scratch> kubectl get secret

NAME                               TYPE                 DATA   AGE
myapp-secret                       Opaque               1      3m14s
sh.helm.release.v1.my-release.v1   helm.sh/release.v1   1      5d23h
sh.helm.release.v1.myapp.v1        helm.sh/release.v1   1      3m14s
```

# Part 3 – Image Version Upgrade
>  helm upgrade --install myapp ./charts/myapp >> .\outputs\helm-upgrade.txt
```
Release "myapp" has been upgraded. Happy Helming!
NAME: myapp
LAST DEPLOYED: Sun Feb  8 21:08:14 2026
NAMESPACE: default
STATUS: deployed
REVISION: 2
DESCRIPTION: Upgrade complete
TEST SUITE: None
```


# Part 4 – Helm History & Rollback
1. Check release history:
- helm history myapp
    > PS C:\Users\repo\DevOps\devops-course\class6 - Helm From Scratch>    helm history myapp
    REVISION        UPDATED                         STATUS          CHART           APP VERSION     DESCRIPTION     
    1               Sun Feb  8 21:02:07 2026        superseded      myapp-0.1.0     0.3.1           Install complete
    2               Sun Feb  8 21:08:14 2026        superseded      myapp-0.1.0     0.3.1           Upgrade complete
    3               Sun Feb  8 21:08:42 2026        superseded      myapp-0.1.0     0.3.1           Upgrade complete
    4               Sun Feb  8 21:16:57 2026        superseded      myapp-0.1.0     0.3.1           Upgrade complete
    5               Sun Feb  8 21:17:48 2026        superseded      myapp-0.1.0     0.3.1           Upgrade complete
    6               Sun Feb  8 21:21:36 2026        superseded      myapp-0.1.0     0.3.1           Upgrade complete
    7               Sun Feb  8 21:25:25 2026        superseded      myapp-0.1.0     0.3.2           Upgrade complete
    8               Sun Feb  8 21:40:18 2026        superseded      myapp-0.1.0     0.3.0           Upgrade complete
    9               Sun Feb  8 21:41:37 2026        superseded      myapp-0.1.0     0.3.1           Rollback to 1
    10              Sun Feb  8 21:43:25 2026        deployed        myapp-0.1.0     0.3.1           Rollback to 1

2. Rollback to previous revision:
- helm rollback myapp 1
    > Rollback was a success! Happy Helming!
    hashicorp/http-echo:0.3.0 hashicorp/http-echo:0.3.1


Save outputs:
- outputs/helm-history.txt
    > REVISION	UPDATED                 	STATUS    	CHART      	APP VERSION	DESCRIPTION     
    1       	Sun Feb  8 21:02:07 2026	superseded	myapp-0.1.0	0.3.1      	Install complete
    2       	Sun Feb  8 21:08:14 2026	superseded	myapp-0.1.0	0.3.1      	Upgrade complete
    3       	Sun Feb  8 21:08:42 2026	superseded	myapp-0.1.0	0.3.1      	Upgrade complete
    4       	Sun Feb  8 21:16:57 2026	superseded	myapp-0.1.0	0.3.1      	Upgrade complete
    5       	Sun Feb  8 21:17:48 2026	superseded	myapp-0.1.0	0.3.1      	Upgrade complete
    6       	Sun Feb  8 21:21:36 2026	superseded	myapp-0.1.0	0.3.1      	Upgrade complete
    7       	Sun Feb  8 21:25:25 2026	superseded	myapp-0.1.0	0.3.2      	Upgrade complete
    8       	Sun Feb  8 21:40:18 2026	superseded	myapp-0.1.0	0.3.0      	Upgrade complete
    9       	Sun Feb  8 21:41:37 2026	deployed  	myapp-0.1.0	0.3.1      	Rollback to 1   

- outputs/helm-rollback.txt
> hashicorp/http-echo:0.3.0 hashicorp/http-echo:0.3.1

# Part 5 – ConfigMap and Secret Usage
- Explain usage 
```   
- ConfigMap: Used for soft settings like URLs, ports, or text that is displayed to the user. This allows you to change the behavior of the application without rebuilding the Docker Image.

- Secret: Encoded (Base64) and not encrypted, it allows for RBAC and reduces password exposure.

- Decoupling: Using Helm makes the system dynamic. The Deployment doesn't "know" what text will be displayed, it just knows that it needs to pull it from the ConfigMap.
```

# Part 6 – Bonus – External Helm Chart
#### 1. Add an external Helm repository and update
> helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```
PS C:\Users\repo\DevOps\devops-course\class6 - Helm From Scratch> helm repo add bitnami https://charts.bitnami.com/bitnami
"bitnami" has been added to your repositories
PS C:\Users\repo\DevOps\devops-course\class6 - Helm From Scratch>     helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "bitnami" chart repository
Update Complete. ⎈Happy Helming!⎈
```

```
helm upgrade --install external-nginx bitnami/nginx `
--set image.tag=1.23.0 `
--namespace nginx-test --create-namespace
```
#### 2. Use an external Helm chart (e.g., bitnami/nginx) as a dependency
```
PS C:\Users\repo\DevOps\devops-course\class6 - Helm From Scratch> helm dependency update ./charts/myapp
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "bitnami" chart repository
Update Complete. ⎈Happy Helming!⎈
Saving 1 charts
Downloading nginx from repo https://charts.bitnami.com/bitnami
Deleting outdated charts
```

#### 4. Override values to match your local deployment (e.g., image tag, service type, port):

```
PS C:\Users\repo\DevOps\devops-course\class6 - Helm From Scratch> helm upgrade --install myapp -n dev --create-namespace ./charts/myapp >> .\outputs\helm-upgrade.txt --set nginx.image.tag=1.23.0 --set nginx.service.type=ClusterIP  --set nginx.service.ports.http=8080  
```
#### kubectl get pods -n dev
```
PS C:\Users\repo\DevOps\devops-course\class6 - Helm From Scratch> kubectl get pods -n dev
NAME                              READY   STATUS                  RESTARTS   AGE
app-deployment-7c858774b9-84j96   1/1     Running                 0          28h
app-deployment-7c858774b9-97nfr   1/1     Running                 0          28h
app-deployment-7c858774b9-t427z   1/1     Running                 0          28h
app-deployment-7c858774b9-wgwl4   1/1     Running                 0          28h
app-deployment-7c858774b9-z4ndh   1/1     Running                 0          28h
myapp-deploy-579bf9c664-6k4sz     1/1     Running                 0          17m
myapp-deploy-579bf9c664-6ns8d     1/1     Running                 0          17m
myapp-logger-652x5                1/1     Running                 0          17m
myapp-nginx-59f94cbf64-hmdkh      0/1     Init:ImagePullBackOff   0          79s
myapp-setup-job-2hwll             0/1     Completed               0          25m
```
