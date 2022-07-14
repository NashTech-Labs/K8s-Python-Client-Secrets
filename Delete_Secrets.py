from kubernetes import client
from kubernetes.client import ApiClient
import json
import yaml
from kubernetes.client.rest import ApiException


def __get_kubernetes_corev1client(bearer_token,api_server_endpoint):
    try:
        configuration = client.Configuration()
        configuration.host = api_server_endpoint
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": "Bearer " + bearer_token}
        client.Configuration.set_default(configuration)
        client_api = client.CoreV1Api()
        return client_api
    except Exception as e:
        print("Error getting kubernetes client \n{}".format(e))
        return None

def __format_data_for_secret(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        if len(json_data["items"]) != 0:
            for secret in json_data["items"]:
                temp_dict={
                    "secret": secret["metadata"]["name"],
                    "namespace": secret["metadata"]["namespace"]
                }
                temp_list.append(temp_dict)
        return temp_list

def __format_data_for_create_secret(client_output):
        temp_dict={}
        temp_list=[]
        json_data=ApiClient().sanitize_for_serialization(client_output)
        
        if type(json_data) is str:
            print("FORMAT_DATA :{}".format(type(json_data)))
            json_data = json.loads(json_data)
        temp_list.append(json_data)
        return temp_list
    

def create_secret(cluster_details,yaml_body=None,namespace="default"):
    try:
        client_api= __get_kubernetes_corev1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        yaml_data=open("secret.yaml", "rb").read().decode('utf-8')
        yaml_body=yaml.safe_load(yaml_data)
        resp = client_api.create_namespaced_secret(
            body=yaml_body, namespace="{}".format(namespace))

        data=__format_data_for_create_secret(resp)
        print (data)    
    except ApiException as e:
        print("ERROR IN create_secret:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_secret(e.body)


def delete_secret(cluster_details,k8s_object_name=None,namespace="default"):
    # Configs can be set in Configuration class directly or using helper
    # utility. If no argument provided, the config will be loaded from
    # default location.
    try:
        client_api= __get_kubernetes_corev1client(
                bearer_token=cluster_details["bearer_token"],
                api_server_endpoint=cluster_details["api_server_endpoint"],
            )
        resp = client_api.delete_namespaced_secret(
                name=k8s_object_name,
                namespace="{}".format(namespace),
                body=client.V1DeleteOptions(
                    propagation_policy="Foreground", grace_period_seconds=5)
            )

        data=__format_data_for_create_secret(resp)
        return data
    except ApiException as e:
        print("ERROR IN create_deployment:\n{}".format(e.body))
        print("TYPE :{}".format(type(e)))
        return __format_data_for_create_secret(e.body)

if __name__ == '__main__':
    cluster_details={
        "bearer_token":"Your_cluster_bearer_token",
        "api_server_endpoint":"Your_cluster_IP"
    }

    #create_secret(cluster_details,"default")
    #delete_secret(cluster_details,k8s_object_name="Deekshaa")