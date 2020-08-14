# Importify
Import and export your configuration like a boss !!

## Installation
Install using pypi distribution using following command.

```
pip install importify
```

## Quick Start
Following is a recommended usage.

1. Define configuration class.

    - Must inherit Serializable
    - Must call super constructor
    - Serializable can consist json serializable types and nested Serializable object.
    
    example:
    
    ```python
    from importify import Serializable


    class Config(Serializable):
        def __init__(self):
            super(Config, self).__init__() 
            self.use_gpu = True
            self.batch_size = 32
            self.model_config = ModelConfig()

    class ModelConfig(Serializable):
        def __init__(self):
            super(ModelConfig, self).__init__()
            self.hidden_dim = 256
            self.output_dim = 128
    ```

2. Parse arguments

    - Arguments are named the same as object variables.
    - Nested variables are divided with dot symbol.
    
    (CODE)
    
    ```python
    # Initialize Serializable inherited configuration class
    config = Config()

    # Parse
    config.parse()
    ```
    
    2-1. Parse command line arguments.

        (BASH)
        
        ```
        python -m your_module --use_gpu False
        ```

    2-2. Import from pre-exported configuration json file. Use ```--load_json``` option.
    
        (BASH)
        
        ```
        python -m your_module --load_json PATH_TO_JSON_FILE
        ```

3. Export current settings to json.

    example:
    
    ```python
    config = Config()
   
    saved_status = config.export_json(path=PATH_TO_JSON_FILE)
    ```
   
## Usage
Please refer to [https://github.com/litcoderr/importify/tree/master/examples](examples) code.

## Contributions
Please commit any issues or pull requests. Every bit of contributions are welcomed.
If this ever goes viral, I'll make a legitimate template for issues and PRs. Thanks.

