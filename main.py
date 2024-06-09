import json
import yaml
import os
import re


def read_yml(filepath):
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)

    return data


def parse_yml_section(section):
    role_requirements = []
    role_variables = []
    role_dependencies = []

    for (key, value) in section.items():
        if isinstance(value, dict):
            result = parse_yml_section(value)
            for req in result[0]:
                role_requirements.append(req)
            for var in result[1]:
                role_variables.append(var)
            for dep in result[2]:
                role_dependencies.append(dep)
        elif isinstance(value, list):
            pass
        else:
            # need to add requirements

            # search for variables, currently handles only non default variable
            match_var = re.search(r'{{ [a-zA-Z_-]* }}', str(value))
            if (match_var):
                # print(match_var)
                role_variables.append(match_var.group(0))
            # search for dependencies, currently handles only roles with FQCN
            match_dep = re.search(r'[a-zA-Z-]*\.[a-zA-Z-]*\.[a-zA-Z-]*', key)
            if (match_dep):
                role_dependencies.append(match_dep.group(0))

    return (role_requirements,
            role_variables,
            role_dependencies)


# var name|default value (t/f)|required (t/f)|description|example|
def parse_yml(role_data, fqcn):
    role_name = fqcn
    role_description = f"< enter {fqcn} description >"
    role_requirements = []
    role_variables = []
    role_dependencies = []
    for section in role_data:
        result = parse_yml_section(section)
        for req in result[0]:
            role_requirements.append(req)
        for var in result[1]:
            role_variables.append(var)
        for dep in result[2]:
            role_dependencies.append(dep)

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


def build_container(namespace, collection):
    container = {
        namespace: {
            collection: {}
        }
    }
    roles_path = f"../{collection}/roles"

    for role in os.listdir(roles_path):
        role_path = f"{roles_path}/{role}"
        main_path = f"{role_path}/tasks/main.yml"
        if os.path.isdir(role_path) and os.path.isfile(main_path):
            container[namespace][collection][role] = parse_yml(read_yml(main_path), f"{collection}.{role}")
    return container


container = build_container("redhat", "controller_configuration")
print(json.dumps(container, indent=4))

file = "../controller_configuration/roles/bulk_host_create/tasks/main.yml"

# print(json.dumps(read_yml(file), indent=4))
# print(parse_yml(read_yml(file), "controller_configuration.bulk_host_create"))
