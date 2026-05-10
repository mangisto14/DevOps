
🧨 שלב 1 — מחיקת כל מה שקיים (ניקוי מלא)
🔥 מחיקת Helm אם קיים
helm uninstall monitoring-dev -n monitoring-dev

אם הוא לא קיים — לא נורא, ממשיכים.

🧹 מחיקת namespace (הכי נקי)

זה מוחק הכל כולל ConfigMaps, Pods, Services:

kubectl delete namespace monitoring-dev

⏳ לחכות עד שזה יסתיים לגמרי.

בדיקה:

kubectl get ns
🆕 שלב 2 — יצירת namespace מחדש
kubectl create namespace monitoring-dev
📦 שלב 3 — הוספת Helm repo
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
⚙️ שלב 4 — יצירת values.yaml נקי (חשוב מאוד)

צור קובץ values.yaml:

grafana:
  adminUser: admin
  adminPassword: admin123

  service:
    type: ClusterIP

  datasources:
    datasources.yaml:
      apiVersion: 1
      datasources:
        - name: Prometheus
          type: prometheus
          url: http://monitoring-dev-kube-promet-prometheus:9090
          access: proxy
          isDefault: true

        - name: Alertmanager
          type: alertmanager
          url: http://monitoring-dev-kube-promet-alertmanager:9093
          access: proxy
          isDefault: false

prometheus:
  prometheusSpec:
    retention: 2d

👉 שים לב:

רק Prometheus הוא default
אין כפילות → זה מה ששבר אותך קודם
🚀 שלב 5 — התקנה מחדש נקייה
helm install monitoring-dev prometheus-community/kube-prometheus-stack \
  -n monitoring-dev \
  -f values.yaml
📊 שלב 6 — בדיקות
kubectl get pods -n monitoring-dev
kubectl get svc -n monitoring-dev

ואז:

kubectl get pods -n monitoring-dev | findstr grafana
🌐 כניסה ל-Grafana
kubectl port-forward svc/monitoring-dev-grafana 3000:80 -n monitoring-dev

ואז:

http://localhost:3000
🔐 התחברות
user: admin
pass: admin123