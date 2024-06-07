import json
import yaml
import os


def read_yml(filepath):
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)

    return data


def parse_requirements(role_data):
    return []


def parse_variables(role_data):
    for key, value in role_data.items():
        if ("{{" in value):
            pass  # process line
    return []


def parse_dependencies(role_data):
    return []


def parse_data(role_data, fqcn):
    role_name = fqcn
    role_description = f"< enter {fqcn} description >"

    # requirements
    role_requirements = parse_requirements(role_data)

    # variables
    # var name | default value (t/f) | required (t/f) | description | example |
    role_variables = parse_variables(role_data)

    # dependencies
    role_dependencies = parse_dependencies(role_data)

    # misc
    role_example_playbook = ""
    role_licensce = "MIT"
    role_author_info = "RedHat (c) 2024"

    return (role_name,
            role_description,
            role_requirements,
            role_variables,
            role_dependencies,
            role_example_playbook,
            role_licensce,
            role_author_info)


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

file = "../controller_configuration/roles/bulk_host_create/tasks/main.yml"

print(json.dumps(read_yml(file), indent=4))
print(parse_data(read_yml(file), "controller_configuration.bulk_host_create"))
