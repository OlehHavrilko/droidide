import docker

class DockerService:
    def __init__(self):
        self.client = docker.from_env()

    def create_container(self, project_id: str):
        try:
            container = self.client.containers.run(
                "codercom/code-server",
                detach=True,
                ports={"8080/tcp": None},
                volumes={f"{project_id}_data:/home/coder/project"},
                environment=["PASSWORD=password"],
                labels={"project_id": project_id},
                mem_limit="512m",
                cpu_shares=512,
            )
            return container
        except docker.errors.APIError as e:
            raise Exception(f"Failed to create container: {e}")

    def get_container(self, project_id: str):
        try:
            containers = self.client.containers.list(
                filters={"label": f"project_id={project_id}"}
            )
            return containers[0] if containers else None
        except docker.errors.APIError as e:
            raise Exception(f"Failed to get container: {e}")

    def remove_container(self, project_id: str):
        container = self.get_container(project_id)
        if container:
            try:
                container.remove(force=True)
            except docker.errors.APIError as e:
                raise Exception(f"Failed to remove container: {e}")
