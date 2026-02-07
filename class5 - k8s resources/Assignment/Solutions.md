
# Home Assignment: Kubernetes Core Resources & RBAC (Hands-On)

## Part 0 – Prerequisites
### Requirements
    A running Kubernetes cluster (Minikube / Kind / Docker Desktop)

    kubectl installed and configured

## Verify:
    kubectl cluster-info
    kubectl get nodes

### kubectl cluster-info :

    C:\Users\repo\DevOps\class5 - k8s resources>kubectl cluster-info
    Kubernetes control plane is running at https://127.0.0.1:64813
    CoreDNS is running at https://127.0.0.1:64813/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

    To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.

### kubectl get nodes
    C:\Users\repo\DevOps\class5 - k8s resources>kubectl get nodes
    NAME       STATUS   ROLES           AGE    VERSION
    minikube   Ready    control-plane   7d1h   v1.34.0

## Part 1 – Namespace (Logical Separation)
### 1. Create a namespace named dev
> Answer : 
```
C:\Users\repo\DevOps\class5 - k8s resources>kubectl get namespace
NAME              STATUS   AGE
default           Active   7d3h
dev               Active   2m46s
kube-node-lease   Active   7d3h
kube-public       Active   7d3h
kube-system       Active   7d3h
namespace/dev created
```
1. What a namespace is
> Answer : 
>> Allows to isolate resources and prevent conflicts between different projects, using shared resources between environments, ability to limit each environment in the amount of resources
    

2. Why it is considered logical (not physical) separation
> Answer :
>> All Namespaces run on the same physical servers (Nodes)
,A Pod in one Namespace can "talk" to a Pod in another Namespace over the network

Apply this YAML:
``` apiVersion: v1
    kind: Namespace
    metadata:
    name: dev
```
> Answer :
C:\Users\repo\DevOps\class5 - k8s resources>kubectl apply -f namespace.yaml
namespace/dev created

### Verify:
    kubectl get namespaces
> Answer :
 ```   
 C:\Users\repo\DevOps\class5 - k8s resources>kubectl get namespace
    NAME              STATUS   AGE
    default           Active   7d3h
    dev               Active   6s
    kube-node-lease   Active   7d3h
    kube-public       Active   7d3h
    kube-system       Active   7d3h
```

## Part 2 – Pod (Ephemeral Workload)
1. Deploy a Pod running nginx
    > Answer : 
        >>
        C:\Users\repo\DevOps\class5 - k8s resources>kubectl apply -f nginx-deployment.yaml 
        pod/demo-pod created


2. Observe the Pod lifecycle
    > Answer : 
```
    C:\Users\Media>kubectl get pods -n dev -w
    NAME       READY   STATUS    RESTARTS   AGE
    demo-pod   1/1     Running   0          11m
    demo-pod   1/1     Terminating   0          11m
    demo-pod   1/1     Terminating   0          11m
    demo-pod   0/1     Completed     0          11m
    demo-pod   0/1     Completed     0          11m
    demo-pod   0/1     Completed     0          11m
    demo-pod   0/1     Pending       0          0s
    demo-pod   0/1     Pending       0          0s
    demo-pod   0/1     ContainerCreating   0          0s
    demo-pod   1/1     Running             0          3s
```


### ❓ Question:
### What happens if you delete this Pod? Who recreates it?
> Answer : 
    >>
    When deleting a directly configured pod, the API Server simply removes it from etcd
    and there is no one to create it again because there is no ReplicaSet


## Part 3 – Deployment (Desired State)

1. Deploy an application using a Deployment
    > Answer : 
    ```
    PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl get deployments -n dev
    NAME             READY   UP-TO-DATE   AVAILABLE   AGE
    app-deployment   3/3     3            3           33m
    PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl get pods -n dev
    NAME                              READY   STATUS    RESTARTS   AGE
    app-deployment-5d879fb8d9-dz6cd   1/1     Running   0          33m
    app-deployment-5d879fb8d9-nqmgk   1/1     Running   0          33m
    app-deployment-5d879fb8d9-tnms7   1/1     Running   0          33m
    ```

2. Scale it
    > Answer
    ```
    PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl apply -f .\nginx-deployment.yaml
    deployment.apps/app-deployment configured
    PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl get pods -n dev
    NAME                              READY   STATUS    RESTARTS   AGE
    app-deployment-5d879fb8d9-dz6cd   1/1     Running   0          37m
    app-deployment-5d879fb8d9-gfvww   1/1     Running   0          10s
    app-deployment-5d879fb8d9-nqmgk   1/1     Running   0          37m
    app-deployment-5d879fb8d9-pbstt   1/1     Running   0          10s
    app-deployment-5d879fb8d9-tnms7   1/1     Running   0          37m
    PS C:\Users\repo\DevOps\class5 - k8s resources> 
    ``

3. Delete a Pod and observe behavior

    > Answer :
    ```
    C:\Users\Media>kubectl get pods -n dev -w
    NAME                              READY   STATUS    RESTARTS   AGE
    app-deployment-5d879fb8d9-dz6cd   1/1     Running   0          41m
    app-deployment-5d879fb8d9-gfvww   1/1     Running   0          4m29s
    app-deployment-5d879fb8d9-nqmgk   1/1     Running   0          41m
    app-deployment-5d879fb8d9-pbstt   1/1     Running   0          4m29s
    app-deployment-5d879fb8d9-tnms7   1/1     Running   0          41m
    app-deployment-5d879fb8d9-dz6cd   1/1     Terminating   0          41m
    app-deployment-5d879fb8d9-dz6cd   1/1     Terminating   0          41m
    app-deployment-5d879fb8d9-tp5l4   0/1     Pending       0          0s
    app-deployment-5d879fb8d9-tp5l4   0/1     Pending       0          0s
    app-deployment-5d879fb8d9-tp5l4   0/1     ContainerCreating   0          0s
    app-deployment-5d879fb8d9-dz6cd   0/1     Completed           0          41m
    app-deployment-5d879fb8d9-dz6cd   0/1     Completed           0          41m
    app-deployment-5d879fb8d9-dz6cd   0/1     Completed           0          41m
    app-deployment-5d879fb8d9-tp5l4   1/1     Running             0          3s

    ```
    ### Verify: 
    * #### kubectl get deployments,rs,pods -n dev 
    ```
        PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl get deployments,rs,pods -n dev
        NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
        deployment.apps/app-deployment   5/5     5            5           44m

        NAME                                        DESIRED   CURRENT   READY   AGE
        replicaset.apps/app-deployment-5d879fb8d9   5         5         5       44m

        NAME                                  READY   STATUS    RESTARTS   AGE
        pod/app-deployment-5d879fb8d9-gfvww   1/1     Running   0          7m26s
        pod/app-deployment-5d879fb8d9-nqmgk   1/1     Running   0          44m
        pod/app-deployment-5d879fb8d9-pbstt   1/1     Running   0          7m26s
        pod/app-deployment-5d879fb8d9-tnms7   1/1     Running   0          44m
        pod/app-deployment-5d879fb8d9-tp5l4   1/1     Running   0          2m49s
    ```

## ❓ Questions:
* Which object ensures the number of Pods?
    > Answer :
    ```
    The ReplicaSet (created by the Deployment). It constantly compares the Desired State (what you requested in YAML) with the Actual State (what is happening on the ground). As soon as there is a gap – it acts to fix it.
    ```
* Why should Pods not be managed directly?
    > Answer :
    ```
    Pods are temporary. If a pod crashes or fails, it will not be recreated.
    There is no mechanism to bring the application back online in the event of a failure.
    You cannot easily increase or decrease the number of copies.
    You cannot update a software version without disabling the service.
    ```

## 🧩 Part 4 – Deployment → ReplicaSet → Pod Relationship
**Explanation**
* Deployment defines desired state
    > The k8s system ensures that the deployment is performed according to the Deployment settings and constantly checks the current state against the desired state. If there is a gap, the system will automatically rebuild it to return to the settings state
* ReplicaSet enforces replica count
    > The role of the ReplicaSet is to ensure that at any given moment, an exact number of instances (Pods) will run in the system, exactly according to the deployment settings.
* Pods run containers
    > The Pod is the worker
    This is the smallest unit.
    Its role: to run the container. It performs the work until it receives a command to stop or until it crashes

__Task__
1. Scale the Deployment:
    > kubectl scale deployment app-deployment --replicas=5 -n dev
    ```
    PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl scale deployment app-deployment --replicas=6 -n dev      
    deployment.apps/app-deployment scaled
    PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl get pods -n dev
    NAME                              READY   STATUS    RESTARTS   AGE
    app-deployment-5d879fb8d9-6l225   1/1     Running   0          5s
    app-deployment-5d879fb8d9-gfvww   1/1     Running   0          3h9m
    app-deployment-5d879fb8d9-nqmgk   1/1     Running   0          3h46m
    app-deployment-5d879fb8d9-pbstt   1/1     Running   0          3h9m
    app-deployment-5d879fb8d9-tnms7   1/1     Running   0          3h46m
    app-deployment-5d879fb8d9-tp5l4   1/1     Running   0          3h5m
    ```
2. Update the image:
    > kubectl set image deployment/app-deployment app=nginx:latest -n dev
    ```
    PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl set image deployment/app-deployment app=nginx:latest -n dev
    deployment.apps/app-deployment image updated
    PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl get pods -n dev
    NAME                              READY   STATUS              RESTARTS   AGE
    app-deployment-5d879fb8d9-nqmgk   1/1     Running             0          3h48m
    app-deployment-5d879fb8d9-pbstt   1/1     Running             0          3h11m
    app-deployment-5d879fb8d9-tnms7   1/1     Terminating         0          3h48m
    app-deployment-5d879fb8d9-tp5l4   1/1     Running             0          3h7m
    app-deployment-77cf88dc74-92s2h   1/1     Running             0          5s
    app-deployment-77cf88dc74-f8hqt   0/1     ContainerCreating   0          2s
    app-deployment-77cf88dc74-plr89   1/1     Running             0          5s
    app-deployment-77cf88dc74-rvvhj   0/1     ContainerCreating   0          0s
    app-deployment-77cf88dc74-tp2xc   0/1     ContainerCreating   0          5s
    PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl get pods -n dev
    NAME                              READY   STATUS    RESTARTS   AGE
    app-deployment-77cf88dc74-6z9nm   1/1     Running   0          7s
    app-deployment-77cf88dc74-92s2h   1/1     Running   0          13s
    app-deployment-77cf88dc74-f8hqt   1/1     Running   0          10s
    app-deployment-77cf88dc74-plr89   1/1     Running   0          13s
    app-deployment-77cf88dc74-rvvhj   1/1     Running   0          8s
    app-deployment-77cf88dc74-tp2xc   1/1     Running   0          13s
    ```

## ❓ Questions:
* How many ReplicaSets exist after the update?
    > has 2 ReplicaSets 

* Why does Kubernetes create a new ReplicaSet?
    > A new ReplicaSet is created when the template is changed

## 🧩 Part 5 – Service Types
Services provide stable networking for Pods.

> LoadBalancer
```
C:\Users\Media>minikube tunnel
* Tunnel successfully started

* NOTE: Please do not close this terminal as this process must stay alive for the tunnel to be accessible ...

! Access to ports below 1024 may fail on Windows with OpenSSH clients older than v8.1. For more information, see: https://minikube.sigs.k8s.io/docs/handbook/accessing/#access-to-ports-1024-on-windows-requires-root-permission
* Starting tunnel for service app-lb.\
```
> NodePort
```
PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl get endpoints -n dev
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
NAME           ENDPOINTS                                                  AGE
app-lb         10.244.0.20:80,10.244.0.21:80,10.244.0.22:80 + 3 more...   70s
app-nodeport   10.244.0.20:80,10.244.0.21:80,10.244.0.22:80 + 3 more...   70s
app-service    10.244.0.20:80,10.244.0.21:80,10.244.0.22:80 + 3 more...   70s
PS C:\Users\repo\DevOps\class5 - k8s resources> minikube service app-nodeport -n dev
┌───────────┬──────────────┬─────────────┬───────────────────────────┐
│ NAMESPACE │     NAME     │ TARGET PORT │            URL            │
├───────────┼──────────────┼─────────────┼───────────────────────────┤
│ dev       │ app-nodeport │ 80          │ http://192.168.49.2:30080 │
└───────────┴──────────────┴─────────────┴───────────────────────────┘
🏃  Starting tunnel for service app-nodeport./┌───────────┬──────────────┬─────────────┬────────────────────────┐
│ NAMESPACE │     NAME     │ TARGET PORT │          URL           │
├───────────┼──────────────┼─────────────┼────────────────────────┤
│ dev       │ app-nodeport │             │ http://127.0.0.1:60292 │
└───────────┴──────────────┴─────────────┴────────────────────────┘
🏃  Starting tunnel for service app-nodeport.
🎉  Opening service dev/app-nodeport in default browser...
❗  Because you are using a Docker driver on windows, the terminal needs to be open to run it.
✋  Stopping tunnel for service app-nodeport.
```
> External IP
```
PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl get svc -n dev
NAME           TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
app-lb         LoadBalancer   10.100.60.217    127.0.0.1     80:30917/TCP   4m39s
app-nodeport   NodePort       10.102.233.240   <none>        80:30080/TCP   4m39s
app-service    ClusterIP      10.110.130.3     <none>        80/TCP         4m39s
```

## ❓ Questions:
* Which Service is internal only?
> The ClusterIP.
This is the default Service type. It assigns an IP address that is only accessible from within the Cluste

* Which Service is best for production?
> the LoadBalancer  : it knows how to distribute traffic between all Nods and Pods in a smart and secure wey

## 🧩 Part 6 – Ingress (HTTP Routing)
Ingress routes external HTTP traffic to Services.
```
PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl get ing -n dev
NAME          CLASS   HOSTS        ADDRESS        PORTS   AGE
app-ingress   nginx   demo.local   192.168.49.2   80      4d1h
```
## ❓ Questions:
* Does Ingress work without an Ingress Controller?
> NO. the ingress is jost a configuration resource that tells kubernetes how to route traffic.
* Why not expose every Service directly?
> Each LoadBalancer service creates an external resource that costs money,
With Ingress, you use one IP for everyone,
Manage one SSL certificate and not each service separately,
Smart routing by domain name,

# 🧩 Part 7 – ConfigMap & Secret
 > PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl exec -n dev app-deployment-7c858774b9-7br7t -- printenv ENV     
```
 dev
```
> PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl exec -n dev app-deployment-7c858774b9-7br7t -- printenv PASSWORD
```
password
```

## ❓ Questions:
* Why separate config from images?
> 

* Why should Secrets be protected with RBAC?
   1. Preventing information leakage, 
    מניעת זליגת מידע: מפתח Front-end לא צריך גישה ל-Secret שמכיל את סיסמת ה-Root של בסיס הנתונים. בעזרת RBAC, נוודא שרק ה-Pod של ה-Backend יכול "לראות" את ה-Secret הזה.
    2.  reducing the attack surface, 
    צמצום מרחב התקיפה (Blast Radius): אם אפליקציה אחת נפרצת, והיא מוגדרת עם RBAC מצומצם, התוקף לא יוכל לגנוב Secrets של אפליקציות אחרות באותו Namespace.
    3. the principle of the minimum required>
    עקרון המינימום הנדרש (Least Privilege): זהו כלל ברזל באבטחת מידע. נותנים רק את המינימום ההכרחי כדי שהמערכת תעבוד.

## 🧩 Part 8 – RBAC & Namespace Isolation

>  kubectl auth can-i get pods --as=system:serviceaccount:dev:app-sa -n dev

* הפקודה הזו היא דרך מצוינת לוודא שהגדרות ה-RBAC (Role-Based Access Control) שלך עובדות כמו שצריך. אתה בעצם שואל את קוברנטיס: "האם ל-ServiceAccount שייצרתי יש באמת הרשאה לצפות בפודים?"

```
PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl auth can-i get pods --as=system:serviceaccount:dev:app-sa -n dev
yes
```

## ❓ Questions:
> Why is RBAC namespace-scoped?
```
הסיבה היא בידוד (Isolation). ב-Kubernetes, ה-Namespace הוא גדר לוגית.

1. ניהול צוותים: אם צוות א' עובד ב-Namespace בשם dev וצוות ב' ב-prod, אנחנו לא רוצים שהרשאה שניתנה בטעות ב-dev תאפשר למשתמש למחוק פודים ב-prod.

2. סדר וארגון: זה מאפשר למנהלי המערכת לתת הרשאות "פינצטה".

3. הערה: יש גם ClusterRole ו-ClusterRoleBinding שנועדו למקרים שבהם באמת צריך הרשאות על פני כל האשכול (כמו כלי ניטור או גיבוי), אבל כברירת מחדל, תמיד עדיף להישאר ברמת ה-Namespace.

```
> What security principle does RBAC enforce?
```
הוא אוכף את עיקרון המינימום הנדרש (Principle of Least Privilege - PoLP).

העיקרון אומר שכל ישות (משתמש, פוד או שירות) צריכה לקבל אך ורק את ההרשאות המינימליות שהיא חייבת כדי לבצע את עבודתה, ולא מילימטר מעבר לזה.

* לדוגמה: אם האפליקציה שלך רק צריכה לראות את הפודים כדי לבדוק סטטוס, ה-Role שלך מאפשר לה get ו-list. הוא לא נותן לה delete או patch. כך, אם מישהו יצליח לפרוץ לאפליקציה שלך, הנזק שהוא יוכל לעשות ל-Cluster יהיה מוגבל מאוד.
```

## 🧩 Part 9 – Production Thinking
### Production Deployment Example
```
resources:
  limits:
    cpu: "500m"
    memory: "256Mi"
replicas: 3
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 1  # כמה פודים מותר שיהיו "למטה" בזמן עדכון
    maxSurge: 1
```

הגעת לשלב שבו אנחנו מפסיקים "לשחק" עם קוברנטיס ומתחילים לחשוב כמו מהנדסי SRE/DevOps אמיתיים. ב-Production, היציבות היא קדושה, והקוד שכתבת (Resources, Replicas, RollingUpdate) הוא ה"ביטוח" של האפליקציה שלך.


## ❓ Questions:
> What changes between dev and prod?
```

בניגוד לקוד האפליקציה (שאמור להיות זהה), התשתית משתנה משמעותית כדי לעמוד בעומס ובשרידות:

כמות המשאבים (Resources): ב-Dev נותנים מינימום כדי לחסוך כסף. ב-Prod נותנים מספיק CPU ו-RAM כדי שהאפליקציה לא "תיחנק" בשיא העומס.

זמינות גבוהה (High Availability): ב-Dev מספיק פוד אחד (replicas: 1). ב-Prod נשתמש במינימום 3 פודים שמתפרסים על פני שרתים (Nodes) שונים, כדי שאם שרת אחד קורס, האתר לא ייפול.

סוג ה-Service: ב-Dev נשתמש ב-NodePort או Port-Forward. ב-Prod נשתמש ב-LoadBalancer עם DNS אמיתי ותעודת SSL.

אבטחה: ב-Prod ה-RBAC הרבה יותר הדוק, וה-Secrets מוצפנים בצורה חזקה יותר (למשל בעזרת Vault או KMS).
```


> Why are limits mandatory in production?
```
בלי Limits, פוד אחד עם באג (למשל Memory Leak) יכול להפוך ל"שכן רע" (Noisy Neighbor):

מניעת קריסת ה-Node: אם פוד מתחיל לצרוך את כל הזיכרון של השרת, ה-Linux Kernel של השרת יתחיל להרוג תהליכים באקראי כדי לשרוד. הוא עלול להרוג פודים חשובים אחרים או אפילו את רכיבי המערכת של קוברנטיס עצמו.

חיזוי עלויות: כשיש Limits, אתה יודע בדיוק כמה כל אפליקציה יכולה לצרוך, מה שמאפשר לך לתכנן נכון את גודל השרתים בענן.

יציבות ה-Scheduling: קוברנטיס משתמש ב-Requests כדי להחליט איפה לשים כל פוד. בלי הגדרות ברורות, הוא עלול "לדחוס" יותר מדי פודים על שרת אחד עד שהוא יקרוס מעומס.
```

## ⭐ Bonus
* Combine everything into one YAML file
* Deploy using:
> kubectl apply -f full-deploy.yaml 
```
PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl delete all --all -n dev
pod "app-deployment-7c858774b9-7br7t" deleted from dev namespace
pod "app-deployment-7c858774b9-7sqqb" deleted from dev namespace
pod "app-deployment-7c858774b9-8kg5w" deleted from dev namespace
pod "app-deployment-7c858774b9-dgdpb" deleted from dev namespace
pod "app-deployment-7c858774b9-xpwhr" deleted from dev namespace
service "app-lb" deleted from dev namespace
service "app-nodeport" deleted from dev namespace
service "app-service" deleted from dev namespace
deployment.apps "app-deployment" deleted from dev namespace
PS C:\Users\repo\DevOps\class5 - k8s resources> kubectl apply -f full-deploy.yaml
namespace/dev unchanged
configmap/app-config unchanged
secret/app-secret unchanged
role.rbac.authorization.k8s.io/pod-reader unchanged
rolebinding.rbac.authorization.k8s.io/pod-reader-binding unchanged
service/app-service created
service/app-nodeport created
service/app-lb created
deployment.apps/app-deployment created
PS C:\Users\repo\DevOps\class5 - k8s resources> 
```


C:\Users\repo\DevOps\class5 - k8s resources>