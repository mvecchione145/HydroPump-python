# HydroPump-python
Configuration Management Library

HydroPump is an open-source Python library that provides a simple and efficient way to manage configuration files. It allows you to store and retrieve configuration data using different backends such as local file system and various cloud storage solutions.

## Installation

You can install HydroPump using pip:

```shell
pip install hydropump
```

## Usage

To use HydroPump, you need to import the `hydropump` module:

```python
import hydropump
```

### Example

Here's a complete example that demonstrates the usage of HydroPump:

```python
from hydropump import Service

service_config = {
    "backend_type": "FileSystem",
    "file_extension": "json",
}

service = Service(config=service_config)

template_id1 = "example_template1"
template1 = {"sqlEngine": "mysql"}
service.create_template(metadata={}, source=template1, template_id=template_id1)

template_id2 = "example_template2"
template2 = {
    "sqlEngine": "postgres",
    "cloudProvider": "AWS",
}
service.create_template(metadata={}, source=template2, template_id=template_id2)

instruction_id = "client-12345"
metadata = {
    "createdBy": "mvecchione145",
    # templates are compiled from left to right
    # (common keys in example_template1 will be
    # overridden by values in example_template2)
    "templates": ["example_template1", "example_template2"],
}
source = {"system": "darwin"}

service.create_instruction(
    instruction_id=instruction_id, metadata=metadata, source=source
)

instruction = service.get_instruction(instruction_id=instruction_id)

print(instruction)
# {
#   "instruction": {
#     "cloudProvider": "AWS",
#     "sqlEngine": "postgres",
#     "system": "darwin"
#   },
#   "metadata": {
#     "compiled": True,
#     "createdBy": "mvecchione145",
#     "createdAt": "YYYY-MM-DD HH:MM:SS.NNNNNN"
#     "templates": [
#       "example_template",
#       "example_template2"
#     ]
#   }
```

## Contributing

Contributions to HydroPump are welcome! If you find any issues or have suggestions for improvement, please open an issue on the [GitHub repository](https://github.com/mvecchione145/hydropump). Pull requests are also appreciated.

Please make sure to follow the [contribution guidelines](docs/CONTRIBUTING.md) when submitting your contributions.

## License

HydroPump is released under the [MIT License](LICENSE).

---

Thank you for using HydroPump! We hope it helps simplify your configuration management process. If you have any questions or need further assistance, feel free to reach out to us at ~~[support@hydropump.com](mailto:support@hydropump.com)~~.