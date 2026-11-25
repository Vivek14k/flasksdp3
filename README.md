# TechWorld — Vivek Kumar

A polished, responsive Flask portfolio inspired by the original TechWorld landing page. It includes a real Flask application, container image, Kubernetes deployment, and a GitHub Actions pipeline for building and optionally deploying each change to a Kubernetes cluster.

## What’s included

- Personal landing page for Vivek Kumar, with services, about, and contact sections.
- Optional direct email link configured through `CONTACT_EMAIL`.
- `/healthz` and `/readyz` endpoints for container and Kubernetes probes.
- Small, non-root Docker image running Gunicorn.
- Kubernetes Deployment and ClusterIP Service in the `vivek-techworld` namespace.
- GitHub Actions tests, GHCR image publishing, and opt-in Kubernetes rollout.

## Run locally

Requires Python 3.12 or newer.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:CONTACT_EMAIL = "your-email@example.com"
python app.py
```

Open [http://localhost:8000](http://localhost:8000). Run the tests with:

```powershell
python -m unittest discover -s tests -v
```

## Build and run with Docker

```powershell
docker build -t vivek-techworld .
docker run --rm -p 8000:8000 -e CONTACT_EMAIL="your-email@example.com" vivek-techworld
```

Open [http://localhost:8000](http://localhost:8000).

## Deploy to Kubernetes

The manifests create two replicas with resource limits, non-root/read-only container settings, and HTTP startup, liveness, and readiness probes.

```powershell
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl -n vivek-techworld port-forward service/vivek-techworld 8080:80
```

Visit [http://localhost:8080](http://localhost:8080). The default manifest uses `ghcr.io/vivek14k/flasksdp3:latest`; publish that image first or change the image to your registry. If the GHCR package is private, configure an image pull secret in the cluster and reference it in the Deployment's `spec.template.spec.imagePullSecrets`.

## GitHub Actions deployment

`.github/workflows/deploy.yml` runs tests on pull requests and pushes. On pushes to `main` and manual workflow runs, it builds and publishes the commit-tagged image and `latest` to GitHub Container Registry. Kubernetes deployment is opt-in:

1. In the repository’s **Settings → Secrets and variables → Actions**, add the `KUBECONFIG` secret containing the target cluster’s kubeconfig.
2. Add the repository variable `ENABLE_KUBERNETES_DEPLOYMENT` with the value `true`.
3. Ensure the cluster can pull the GHCR image. Make the package public, or add an image pull secret in the `vivek-techworld` namespace and reference it in the Deployment.
4. Push to `main` or run the workflow manually. The workflow applies the manifests, updates the Deployment to the exact commit image, and waits for the rollout.

The kubeconfig should be scoped to the target cluster and have permission to manage the `vivek-techworld` namespace and its Deployment and Service. Do not commit kubeconfig files or registry credentials.

## Contact address

The site does not invent an email address or claim to send messages. Set `CONTACT_EMAIL` for local or container runs; for Kubernetes, add the variable to the Deployment or provide it through a Kubernetes Secret and reference it as a container environment variable.
