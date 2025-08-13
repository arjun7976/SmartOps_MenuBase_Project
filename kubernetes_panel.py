"""
Kubernetes Control Panel

This module provides a Streamlit-based UI for managing Kubernetes clusters.
"""
import streamlit as st

try:
    from kubernetes import client, config
    KUBERNETES_AVAILABLE = True
except ImportError:
    KUBERNETES_AVAILABLE = False

def load_kubernetes_config():
    """Load Kubernetes configuration with error handling."""
    try:
        config.load_kube_config()
        return True, "Successfully loaded kube config"
    except Exception as e:
        return False, f"Failed to load kube config: {str(e)}"

def show_kubernetes_panel():
    """Display the Kubernetes Control Panel."""
    if not KUBERNETES_AVAILABLE:
        st.error("""
        The Kubernetes client library is not installed. Please install it using:
        ```
        pip install kubernetes
        ```
        Also, make sure you have a valid kubeconfig file at ~/.kube/config
        """)
        return

    # Load Kubernetes config
    success, message = load_kubernetes_config()
    if not success:
        st.error(f"❌ {message}")
        st.info("""
        Please ensure you have a valid kubeconfig file at ~/.kube/config
        and that you have the necessary permissions to access the cluster.
        """)
        return

    # Initialize API clients
    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()

    # Sidebar navigation
    st.sidebar.title("☸️ SmartOps Kubernetes Panel")
    section = st.sidebar.radio("📂 Select Section", [
        "🏠 Cluster Info", 
        "📦 Pods", 
        "🧩 Deployments", 
        "📂 Namespaces", 
        "🌐 Services", 
        "🔐 Secrets"
    ])

    # =====================================
    # 🏠 CLUSTER INFO
    # =====================================
    if section == "🏠 Cluster Info":
        st.title("🏠 Cluster Info")
        try:
            nodes = v1.list_node().items
            st.subheader(f"🖥️ {len(nodes)} Nodes Found")
            for node in nodes:
                with st.expander(f"🖥️ {node.metadata.name}"):
                    st.write("🔧 Conditions:")
                    for condition in node.status.conditions:
                        st.write(f"- {condition.type}: {condition.status}")
                    st.write("📦 Capacity:")
                    for k, v in node.status.capacity.items():
                        st.write(f"- {k}: {v}")
        except Exception as e:
            st.error(f"Failed to fetch cluster info: {str(e)}")

    # =====================================
    # 📦 PODS
    # =====================================
    elif section == "📦 Pods":
        st.title("📦 Pods in Cluster")
        try:
            namespaces = [ns.metadata.name for ns in v1.list_namespace().items]
            selected_ns = st.selectbox("Select Namespace", namespaces)
            
            pods = v1.list_namespaced_pod(namespace=selected_ns)
            st.subheader(f"📍 {len(pods.items)} Pods in `{selected_ns}`")
            
            for pod in pods.items:
                with st.expander(f"📦 {pod.metadata.name}"):
                    st.write(f"- Status: {pod.status.phase}")
                    st.write(f"- Node: {pod.spec.node_name}")
                    if st.button(f"🗑️ Delete `{pod.metadata.name}`", 
                              key=f"del_pod_{pod.metadata.uid}"):
                        with st.spinner(f"Deleting {pod.metadata.name}..."):
                            try:
                                v1.delete_namespaced_pod(
                                    name=pod.metadata.name, 
                                    namespace=selected_ns
                                )
                                st.success(f"Deleted `{pod.metadata.name}`")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to delete pod: {str(e)}")
        except Exception as e:
            st.error(f"Failed to fetch pods: {str(e)}")

    # =====================================
    # 🧩 DEPLOYMENTS
    # =====================================
    elif section == "🧩 Deployments":
        st.title("🧩 Deployments in Cluster")
        try:
            namespaces = [ns.metadata.name for ns in v1.list_namespace().items]
            selected_ns = st.selectbox("Select Namespace", namespaces, key="deploy_ns")

            deployments = apps_v1.list_namespaced_deployment(namespace=selected_ns)
            st.subheader(f"🧩 {len(deployments.items)} Deployments in `{selected_ns}`")

            for deploy in deployments.items:
                with st.expander(f"📦 {deploy.metadata.name}"):
                    st.write(f"- Replicas: {deploy.spec.replicas}")
                    st.write(f"- Available: {deploy.status.available_replicas}")
                    new_replicas = st.slider(
                        "Scale Replicas", 
                        0, 10, 
                        deploy.spec.replicas or 0, 
                        key=f"scale_{deploy.metadata.uid}"
                    )
                    if st.button("⚙️ Scale", key=f"btn_scale_{deploy.metadata.uid}"):
                        with st.spinner(f"Scaling {deploy.metadata.name}..."):
                            try:
                                body = {"spec": {"replicas": new_replicas}}
                                apps_v1.patch_namespaced_deployment_scale(
                                    name=deploy.metadata.name,
                                    namespace=selected_ns,
                                    body=body
                                )
                                st.success(f"Scaled `{deploy.metadata.name}` to {new_replicas} replicas")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to scale deployment: {str(e)}")
        except Exception as e:
            st.error(f"Failed to fetch deployments: {str(e)}")

    # =====================================
    # 📂 NAMESPACES
    # =====================================
    elif section == "📂 Namespaces":
        st.title("📂 Namespaces")
        try:
            ns_list = v1.list_namespace().items
            st.subheader(f"📁 {len(ns_list)} Namespaces Found")
            
            # Display namespaces in columns for better organization
            cols = st.columns(3)
            for i, ns in enumerate(ns_list):
                with cols[i % 3]:
                    st.markdown(f"- `{ns.metadata.name}`")
            
            # Create new namespace
            st.markdown("### ➕ Create New Namespace")
            with st.form("create_namespace"):
                new_ns = st.text_input("Namespace Name")
                if st.form_submit_button("Create Namespace") and new_ns:
                    try:
                        body = client.V1Namespace(
                            metadata=client.V1ObjectMeta(name=new_ns)
                        )
                        v1.create_namespace(body=body)
                        st.success(f"Namespace `{new_ns}` created!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to create namespace: {str(e)}")
        except Exception as e:
            st.error(f"Failed to fetch namespaces: {str(e)}")

    # =====================================
    # 🌐 SERVICES
    # =====================================
    elif section == "🌐 Services":
        st.title("🌐 Services")
        try:
            namespaces = [ns.metadata.name for ns in v1.list_namespace().items]
            selected_ns = st.selectbox("Select Namespace", namespaces, key="svc_ns")
            
            services = v1.list_namespaced_service(namespace=selected_ns)
            st.subheader(f"🔌 {len(services.items)} Services in `{selected_ns}`")

            for svc in services.items:
                with st.expander(f"🌐 {svc.metadata.name}"):
                    st.write(f"- Type: {svc.spec.type}")
                    st.write(f"- Cluster IP: {svc.spec.cluster_ip}")
                    if svc.spec.ports:
                        st.write("🔌 Ports:")
                        for port in svc.spec.ports:
                            st.write(f"  - Port: {port.port} → Target: {port.target_port}")
        except Exception as e:
            st.error(f"Failed to fetch services: {str(e)}")

    # =====================================
    # 🔐 SECRETS
    # =====================================
    elif section == "🔐 Secrets":
        st.title("🔐 Secrets")
        try:
            namespaces = [ns.metadata.name for ns in v1.list_namespace().items]
            selected_ns = st.selectbox("Select Namespace", namespaces, key="secrets_ns")
            
            secrets = v1.list_namespaced_secret(namespace=selected_ns)
            st.subheader(f"🔐 {len(secrets.items)} Secrets in `{selected_ns}`")

            for secret in secrets.items:
                with st.expander(f"🔐 {secret.metadata.name}"):
                    st.write(f"- Type: {secret.type}")
                    st.write(f"- Data Keys: {list(secret.data.keys()) if secret.data else 'None'}")
        except Exception as e:
            st.error(f"Failed to fetch secrets: {str(e)}")

# For testing the panel directly
if __name__ == "__main__":
    show_kubernetes_panel()
