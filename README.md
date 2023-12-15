# module

This library allows you to create small subsections of a larger network (to be executed on a remote server)

## Installation
You can install using either pip or conda
### Install using pip
```shell
pip install moduler
```

## Usage

Example with Pytorch

```python
import moduler as md

import torch
import torch.nn as nn

import os
os.environ["BABS_API_KEY"] = "your_api_key"

model = nn.Sequential(
        nn.Linear(28 * 28, 128),        # module will run locally
        nn.ReLU(),                      # module will run locally
        md.Module(md.ModuleType.LINEAR, in_features=128, out_features=56),  # module will run on server
        nn.Linear(56, 10),              # module will run locally
    )

result = model(torch.randn(28 * 28))
print(result)
```

Example with Tensorflow

```python
# coming soon...
```