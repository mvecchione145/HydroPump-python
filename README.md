[![Contributor Covenant](https://img.shields.io/badge/Contributor)]

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

### Backend Configuration

HydroPump supports different backends for storing configuration data. Currently, it supports file system backends with JSON and YAML file formats.

To configure a file system backend, you can create an instance of the `FileSystemBackend` class and specify the file extension:

```python
backend = hydropump.FileSystemBackend(file_extension="json")  # or "yaml"
```

Optionally you can specify the root directory in which to store the instruction files.

```python
backend = hydropump.FileSystemBackend(file_extension="json", root_directory="path/to/dir")
```

### Service Initialization

Once you have configured the backend, you can create a `Service` instance by passing the backend as a parameter:

```python
service = hydropump.Service(backend=backend)
```

Service will be the interfacing object for accessing, creating, deleting and editing instruction files.

### Creating Instructions

To create an instruction, you need to provide an instruction ID and a payload (configuration data) in the form of a dictionary. The instruction ID should be unique for each instruction.

```python
# instruction_id is optional if left blank a UUID will be generated
instruction_id = "client-12345"
payload = {
    "system": "darwin",
    "date_created": "2023-07-09 11:18:23.001"
}

service.create_instruction(instruction_id=instruction_id, payload=payload)
```

This will create a JSON file (or YAML file if configured) with the given payload.

### Retrieving Instructions

To retrieve an instruction, you can use the `get_instruction` method and provide the instruction ID:

```python
returned_payload = service.get_instruction(instruction_id=instruction_id)
```

This will return the payload (configuration data) associated with the given instruction ID.

### Example

Here's a complete example that demonstrates the usage of HydroPump:

```python
import hydropump

backend = hydropump.FileSystemBackend(file_extension="json")
service = hydropump.Service(backend=backend)

instruction_id = "client-12345"
payload = {
    "system": "darwin",
    "date_created": "2023-07-09 11:18:23.001"
}

service.create_instruction(instruction_id=instruction_id, payload=payload)

returned_payload = service.get_instruction(instruction_id=instruction_id)

print(returned_payload)
```

## Contributing

Contributions to HydroPump are welcome! If you find any issues or have suggestions for improvement, please open an issue on the [GitHub repository](https://github.com/your-username/hydropump). Pull requests are also appreciated.

Please make sure to follow the [contribution guidelines](docs/CONTRIBUTING.md) when submitting your contributions.

## License

HydroPump is released under the [MIT License](LICENSE).

---

Thank you for using HydroPump! We hope it helps simplify your configuration management process. If you have any questions or need further assistance, feel free to reach out to us at ~~[support@hydropump.com](mailto:support@hydropump.com)~~.