from __future__ import annotations

import json
import os
import re
import tempfile
from typing import List, cast

import autoflake
import black
import isort
import jinja2
import uritemplate
from datamodel_code_generator import __main__ as datamodel_code_generator

from codegen import config, models, patches, utils


def generate_models() -> None:
    with tempfile.TemporaryDirectory() as patched_dir:
        for entry in os.scandir(config.SCHEMAS_MODELS_DIR):
            entry = cast(os.DirEntry, entry)

            if not (entry.is_file() and entry.name.endswith(".json")):
                continue

            model_name, _ = os.path.splitext(entry.name)
            generate_model(model_name, patch_schema(entry.path, patched_dir))


def patch_schema(path: str, patched_dir: str) -> str:
    name, _ = os.path.splitext(os.path.basename(path))
    patch = patches.PATCHES.get(name)
    if patch is None:
        return path

    with open(path) as f:
        schema = json.load(f)
    patch(schema)

    patched_path = os.path.join(patched_dir, os.path.basename(path))
    with open(patched_path, "w") as f:
        f.write(utils.json_dumps(schema))
    return patched_path


def generate_model(model_name: str, schema_path: str) -> None:
    model_dir = os.path.join(config.MODULE_MODELS_DIR, model_name)
    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(model_dir, "__init__.py")

    datamodel_code_generator.main(
        args=[
            "--input",
            schema_path,
            "--input-file-type",
            "jsonschema",
            "--output",
            model_path,
            "--output-model-type",
            "pydantic_v2.BaseModel",
            "--use-field-description",
            "--class-name",
            "Model",
            "--disable-timestamp",
            # can't use due to "enforced constraints" error
            # "--keep-model-order",
            "--enable-faux-immutability",
            "--allow-extra-fields",
            "--enum-field-as-literal",
            "all",
            # "--field-constraints",
            # can't use due to unsupported backport of typing.Annotated
            # "--use-annotated",
            "--target-python-version",
            "3.10",
            "--formatters",
            "builtin",
        ]
    )


def generate_resources() -> None:
    model_names: List[str] = []

    with open(config.SCHEMAS_DISCOVERY_PATH) as f:
        schema = json.load(f)

    for entry in os.scandir(config.SCHEMAS_MODELS_DIR):
        name, ext = os.path.splitext(entry.name)
        if ext == ".json" and name not in config.IGNORED_MODELS:
            model_names.append(name)

    t_resources = []

    for resource_name, resource in schema["resources"].items():
        print(resource_name)
        if resource_name == "pelican" or resource_name in config.IGNORED_RESOURCES:
            continue

        t_resource = models.Resource(
            name=resource_name,
            class_name=resource_name.capitalize(),
            imported_models=model_names,
            operations=[],
        )
        t_resources.append(t_resource)

        for operation_name, operation in resource.items():
            op_id = f"{resource_name}.{operation_name}"
            if op_id in config.IGNORED_OPERATIONS:
                continue

            operation_name = utils.py_safe(operation_name)

            uri = operation["uri"]
            uri = utils.replace_expiry(uri)
            uri_template = uritemplate.URITemplate(uri)

            if "auth_header_primary" not in operation["authentication"]:
                print(f"skiping {op_id}: does not support token auth")
                continue

            try:
                assert operation["accept"] is not None
                accepts = list(operation["accept"].values())
                if not accepts and op_id in config.RETURN_BYTES:
                    accepts = ["*/*"]

                assert operation["content_type"] is not None
                content_types = list(operation["content_type"].values())

                if "multipart/form-data" in content_types:
                    content_types = ["multipart/form-data"]

                if len(content_types) > 1:
                    raise ValueError(f"multiple content types: {content_types}")

                for ct in accepts + content_types:
                    model_name = utils.model_from_content_type(ct)
                    if model_name is not None and model_name not in model_names:
                        raise ValueError(f"missing schema for {model_name}")

                t_op = models.Operation(
                    method=operation["http_method"],
                    name=operation_name,
                    uri_template=uri_template.uri,
                    parameters=[],
                    content_types=content_types,
                    accepts=accepts,
                )
                t_resource.operations.append(t_op)

            except ValueError as e:
                print(f"skiping {resource_name}.{operation_name}: {e}")
                continue

            for content_type in content_types:
                t_op.parameters.append(
                    models.Parameter(
                        name="_data",
                        is_data=True,
                        content_type=models.ContentType(value=content_type),
                    )
                )

            resource_param = operation.get("resource_parameter")
            url_params = {p["name"]: p for p in operation.get("uri_parameters", [])}
            query_vars = {v.strip("*") for m in re.finditer(r"\{[?&]([^}]+)\}", uri) for v in m.group(1).split(",")}

            for arg in uri_template.variable_names:
                if resource_param and arg == resource_param["name"]:
                    t_op.parameters.append(
                        models.Parameter(
                            name=resource_param["name"],
                            type=resource_param.get("type"),
                            default=resource_param.get("default"),
                            is_uri=True,
                        )
                    )

                elif arg in url_params:
                    param = url_params[arg]
                    t_op.parameters.append(
                        models.Parameter(
                            name=param.get("name"),
                            enum=param.get("enum"),
                            type=param.get("type"),
                            default=param.get("default"),
                            is_uri=True,
                            optional=arg in query_vars and "default" not in param,
                        )
                    )

            t_op.parameters.sort(key=lambda x: x.sort_key)

            try:
                for p in t_op.parameters:
                    p.signature
                t_op.response_annotation
                for rt in t_op.response_types:
                    rt.return_expr
            except ValueError as e:
                print(f"skiping {op_id}: {e}")
                t_resource.operations.remove(t_op)

        t_resource.operations.sort(key=lambda x: x.name)

        if not t_resource.operations:
            print(f"skiping resource {resource_name}: no supported operations")
            t_resources.remove(t_resource)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(config.TEMPLATES_DIR),
        undefined=jinja2.StrictUndefined,
    )

    client_template = env.get_template("client.py")
    os.makedirs(config.MODULE_RESOURCES_DIR, exist_ok=True)
    with open(os.path.join(config.MODULE_RESOURCES_DIR, "client.py"), "w") as f:
        f.write(client_template.render())

    with open(os.path.join(config.MODULE_RESOURCES_DIR, "__init__.py"), "w") as f:
        f.write("\n")

    resource_template = env.get_template("resource.py.jinja2")

    for t_resource in t_resources:
        output = resource_template.render(resource=t_resource)
        try:
            output = isort.code(output)

            output = autoflake.fix_code(output, expand_star_imports=True)
            output = autoflake.fix_code(output, remove_all_unused_imports=True)
            output = autoflake.fix_code(output, remove_unused_variables=True)

            mode = black.Mode()
            mode.line_length = 512
            output = black.format_file_contents(output, fast=False, mode=mode)

            output = isort.code(output)

        except Exception:
            print(t_resource.name)
            print(output)
            raise

        with open(os.path.join(config.MODULE_RESOURCES_DIR, f"{t_resource.name}.py"), "w") as f:
            f.write(output)


def generate_all() -> None:
    generate_models()
    generate_resources()
