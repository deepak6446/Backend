# Kubernetes Node.js Sample Application

## Project Overview

This project provides a complete, well-documented guide for deploying a containerized Node.js application on a local Kubernetes cluster using Minikube. It is designed to be an educational tool, showcasing a wide range of essential Kubernetes concepts, including:

- **Deployments**: Managing application lifecycle.
- **Services**: Exposing applications within the cluster.
- **Probes**: Liveness and Readiness checks for application health.
- **ConfigMaps & Secrets**: Managing configuration and sensitive data.
- **Volumes**: Providing ephemeral storage to pods.
- **Horizontal Pod Autoscaler (HPA)**: Automatically scaling based on CPU load.
- **Istio**: Using Gateway and VirtualService for advanced ingress traffic management.

The setup is tailored for an **Ubuntu 22.04** environment.

## Prerequisites

Before you begin, ensure you have the following tools installed on your Ubuntu 22.04 system:

- **Docker**: The container runtime.
- **Kubectl**: The Kubernetes command-line tool.
- **Minikube**: A tool for running a single-node Kubernetes cluster locally.

## Step 1: Local Kubernetes Cluster Setup

These commands will set up `kubectl`, `minikube`, and a local cluster ready for our application.

1.  **Install `kubectl`**:

    ```bash
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    kubectl version --client
    ```

2.  **Install `minikube`**:

    ```bash
    curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube /usr/local/bin/
    ```

3.  **Start the Minikube Cluster**:
    We will start Minikube with specific resources to ensure it can handle the HPA and Istio.

    ```bash
    minikube start --driver=docker --cpus=4 --memory=4096
    ```

    ```bash
    minikube status
    minikube delete --all --purge
    ```

4.  **Enable Required Addons**:
    The `metrics-server` is crucial for the HPA to collect CPU/memory metrics. `istio` installs the service mesh components.

    ```bash
    minikube addons enable metrics-server
    minikube addons enable istio
    # This command installs the NGINX Ingress Controller into your cluster
    minikube addons enable ingress
    # Watch the pods in the ingress-nginx namespace. Do not proceed until they are all Running and READY
    kubectl get pods -n ingress-nginx -w
    ```

5.  **Configure Shell to Use Minikube's Docker Daemon**:
    This is a critical step for local development. It points your local Docker client to the Docker engine inside the Minikube cluster. This allows you to build a Docker image that is immediately available to the cluster without pushing it to a remote registry.
    ```bash
    eval $(minikube -p minikube docker-env)
    ```
    **Note**: This command is only valid for your current terminal session. If you open a new terminal, you must run it again.

## Step 2: Build and Deploy the Application

Now we will build the application's Docker image and deploy all our Kubernetes resources.

1.  **Build the Docker Image**:
    From the root directory of this project (where the `Dockerfile` is located), run:

    ```bash
    # Replace 'your-dockerhub-username' with your actual username or any other identifier.
    docker build -t deepak6446/nodejs-app:latest .
    ```

2.  **Create the Kubernetes Secret**:
    Our application expects a secret named `app-secrets`. We create it manually using `kubectl`.

    ```bash
    kubectl create secret generic app-secrets --from-literal=API_KEY='SUPER_SECRET_12345'
    ```

3.  **Apply the Kubernetes Manifest**:
    This single command will create the ConfigMap, Deployment, Service, HPA, and Istio resources defined in the manifest file.
    ```bash
    kubectl apply -f k8s-manifest.yaml
    ```
    You should see a confirmation message for each resource created.

## Step 3: Accessing and Testing the Application

We will use the Istio Ingress Gateway to access our application from outside the cluster.

1.  **Get the Cluster IP Address**:
    Minikube runs on a specific IP on your host machine. We'll get this IP and store it in an environment variable.

    ```bash
    export INGRESS_HOST=$(minikube ip)
    echo "Application can be accessed at http://${INGRESS_HOST}"
    ```

2.  **Test the Endpoints**:
    Use `curl` to test the different endpoints of our application.

    - **Root Endpoint**:

      ```bash
      curl http://${INGRESS_HOST}/
      # Expected Output: Welcome to the Node.js sample app on Kubernetes!
      ```

    - **ConfigMap Endpoint**:

      ```bash
      curl http://${INGRESS_HOST}/config
      # Expected Output: Message from ConfigMap: Hello from the ConfigMap!
      ```

    - **Secret Endpoint**:

      ```bash
      curl http://${INGRESS_HOST}/secret
      # Expected Output: My secret API Key is: SUPER_SECRET_12345
      ```

    - **Volume Endpoint**:
      Run this command multiple times to see the timestamp update.

      ```bash
      curl http://${INGRESS_HOST}/data
      # Expected Output: Read from volume: "Data written at: 2023-10-27T..."
      ```

    - **Heavy CPU Endpoint** (for HPA testing):
      This request will take a few seconds to complete as it's performing a heavy calculation.
      ```bash
      curl http://${INGRESS_HOST}/heavy
      # Expected Output: Heavy computation finished. Result (not meaningful): ...
      ```

## Step 4: Testing Kubernetes Features

### Probes (Readiness)

Shortly after you apply the manifest, the Readiness probe will fail for the first ~20 seconds because of our simulated startup delay.

1.  Check the pod status. You will see `0/1` under the `READY` column initially.
    ```bash
    kubectl get pods
    ```
2.  Get the name of one of your pods (e.g., `nodejs-app-deployment-xxxxxxxx-yyyyy`).
3.  Describe the pod to see its events. Scroll to the bottom to the `Events` section.
    ```bash
    kubectl describe pod <your-pod-name-here>
    ```
    You will see events like `Warning Unhealthy Readiness probe failed: HTTP probe failed with statuscode: 500`. After about 20 seconds, the pod will become ready, and these warnings will stop.

### Autoscaling (HPA)

We will generate load on the `/heavy` endpoint to trigger the HorizontalPodAutoscaler.

1.  **Terminal 1: Watch the HPA status**.
    This will show you the current CPU utilization and replica count.

    ```bash
    kubectl get hpa -w
    ```

    Initially, the `TARGETS` column might show `<unknown>/50%` until metrics are collected. After a minute, it should stabilize around `0%/50%` or a low number.

2.  **Terminal 2: Watch the Pods**.
    This will show you new pods being created when the HPA scales up.

    ```bash
    kubectl get pods -w
    ```

3.  **Terminal 3: Generate Load**.
    This simple `while` loop will continuously send requests to the CPU-intensive endpoint.

    ```bash
    while true; do curl -s -o /dev/null http://${INGRESS_HOST}/heavy; done
    ```

4.  **Observe**:
    - In Terminal 1, you will see the `TARGETS` percentage climb above 50%.
    - The HPA will then increase the `REPLICAS` count.
    - In Terminal 2, you will see new pods being created and moving to the `Running` state.
    - Stop the `while` loop in Terminal 3 (with `Ctrl+C`). After a few minutes, the CPU load will drop, and the HPA will scale the number of replicas back down to the `minReplicas` (2).

## Debugging Tips

If something goes wrong, these commands are your best friends:

- **View all resources**: `kubectl get all`
- **Inspect a pod's state and events**: `kubectl describe pod <pod-name>`
- **Stream logs from a pod**: `kubectl logs -f <pod-name>`
- **Get a shell inside a running container**: `kubectl exec -it <pod-name> -- /bin/sh`

## Cleanup

To tear down the entire setup and free up resources, run the following commands.

1.  **Delete Kubernetes resources from the manifest**:

    ```bash
    kubectl delete -f k8s-manifest.yaml
    ```

2.  **Delete the manually created secret**:

    ```bash
    kubectl delete secret app-secrets
    ```

3.  **Stop and delete the Minikube cluster**:
    ```bash
    minikube stop && minikube delete
    ```
