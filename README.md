# Python Flask Application on Kubernetes

A Python Flask application deployed to Kubernetes using **Helm** and managed via GitOps with **ArgoCD**.

---

## Prerequisites

* **Kubernetes Cluster** (Minikube, Kind, or managed cluster)
* **`kubectl`** configured to communicate with your cluster
* **`jq`** installed for JSON processing (`sudo apt install jq` or `brew install jq`)

---

## Getting Started

### 1. Install Helm
Download and execute the official Helm installation script:

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

### 2. Deploy the Application Chart

Create a local chart structure (if not already present) and deploy the application to the `python` namespace:

```bash
# Create chart directory
helm create python-app

# Install application
helm install python-app . -n python --create-namespace
```

---

## GitOps Setup with ArgoCD

### 1. Install ArgoCD
Deploy ArgoCD using custom value overrides:

```bash
helm upgrade --install argocd argo/argo-cd \
  -n argocd \
  --create-namespace \
  -f values-argo.yaml
```

### 2. Local DNS Configuration
Add the following entry to your `/etc/hosts` file:

```text
127.0.0.1 argocd.example.com
```

### 3. Access the ArgoCD Dashboard

1. **Port-Forward Server:**
   ```bash
   kubectl port-forward svc/argocd-server -n argocd 8080:443
   ```
2. Open your browser and navigate to `https://localhost:8080` (or `http://argocd.example.com:8080`).

3. **Retrieve Admin Credentials:**
   * **Username:** `admin`
   * **Password:** Run the command below to print the initial password:
     ```bash
     kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
     ```

---

## Monitoring & Troubleshooting

### ArgoCD Health Verification

* **View application resource tree:**
  ```bash
  argocd app resources my-app --output tree=detailed
  ```

* **Filter non-healthy resources:**
  ```bash
  argocd app get python-app -o json | jq '.status.resources[] | select(.health.status != "Healthy") | {kind: .kind, namespace: .namespace, name: .name, health: .health}'
  ```

### Kubernetes Diagnostics

* **View events for specific deployment:**
  ```bash
  kubectl events -n python-ns --for=deployment/python-app
  ```

* **View all namespace events ordered by time:**
  ```bash
  kubectl get events -n python-ns --sort-by='.lastTimestamp'
  ```

* **Inspect failing or stuck pods:**
  ```bash
  # Get pod list
  kubectl get pods -n python-ns -l app=python-app

  # Inspect pod details and events
  kubectl describe pod <pod-name> -n python-ns