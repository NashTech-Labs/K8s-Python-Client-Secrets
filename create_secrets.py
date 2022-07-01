from kubernetes import client, config

def create_secret(data , string_data , client_api):
    secret = client.V1Secret(
        api_version="v1",
        kind="Secret",
        metadata=client.V1ObjectMeta(name="my-secret"),
        data=data , 
        string_data=string_data
    )

    api = client_api.create_namespaced_secret(namespace="default", body=secret)
    return api

api_server_endpoint = "Your_API"
bearer_token = "Your_Bearer_Token"


configuration = client.Configuration()
configuration.host = api_server_endpoint
configuration.verify_ssl = False
configuration.api_key = {"authorization": "Bearer " + bearer_token}
client.Configuration.set_default(configuration)
client_api = client.CoreV1Api()

cm={
    "name": "deekasha"
}
create_secret({} , cm , client_api)