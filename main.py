import json
import yaml
import os


def read_yml(filepath):
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)

    return data


namespace = "redhat"
collection = "controller_configuration"
container = {
    namespace: {
        collection: {}
    }
}


def build_container():
    roles_path = f"../{collection}/roles"

    for role in os.listdir(roles_path):
        role_path = f"{roles_path}/{role}"
        main_path = f"{role_path}/tasks/main.yml"
        if os.path.isdir(role_path) and os.path.isfile(main_path):
            container[namespace][collection][role] = read_yml(main_path)


# build_container()
# print(json.dumps(container, indent=4))


print(json.dumps(read_yml("../controller_configuration/roles/dispatch/tasks/main.yml"), indent=4))
