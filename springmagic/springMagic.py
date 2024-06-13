import sys
import os
import inspect


def main():
    # Add SprinMagic path to PYTHON_PATH
    script_name = inspect.getframeinfo(inspect.currentframe()).filename
    script_path = os.path.dirname(os.path.abspath(script_name))
    path_name = os.path.dirname(script_path)

    if os.path.exists(path_name) and path_name not in sys.path:
        sys.path.append(path_name)

    # Import SpringMagic module

    # Recompile SpringMagic module if modification has been made

    from . import main as app
    from . import mkDevTools as dev

    import springmagic
    dev.refresh(springmagic)
    # Launch SpringMagic
    app.main()

    # Remove SprinMagic path from PYTHON_PATH
    sys.path.remove(path_name)
