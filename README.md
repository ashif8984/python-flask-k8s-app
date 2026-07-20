# python-flask-k8s-app


## INstalling Helm

curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4
chmod 700 get_helm.sh
./get_helm.sh

helm create python-app
helm install python-app -n python . --create-namespace

helm upgrade --install argocd argo/argo-cd -n argocd --create-namespace -f values-argo.yaml

127.0.0.1 argocd.example.com


# Starting ArgoCD server
kubectl port-forward svc/argocd-server -n argocd 8080:443

localhost:8080

# Fetch password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

admin
<password>