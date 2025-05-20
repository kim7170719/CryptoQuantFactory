def safe_import(module_name, fallback=None):
    try:
        module = __import__(module_name)
        return module
    except ImportError:
        if fallback:
            print(f"Using fallback for {module_name}")
            return fallback
        else:
            print(f"Module {module_name} not found and no fallback provided.")
            return None
