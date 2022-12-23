# Flet as System Tray Icon

A simple program using PyStray to expose the possibility of a Flet app being made a System Tray icon without any issues.
This program has been tested only on Windows. I hope it works on your device too. Let me know in the issue tracker if not.

### Requirements
Three main requirements:

- [Flet](https://pypi.org/project/flet/) (for the GUI)
- [PyStray](https://pypi.org/project/pystray/) (for the System tray icon)
- [Pillow](https://pypi.org/project/pillow/) (required by PyStray for the Tray icon's image)

All these are in the `requirements.txt` file. For simplicity:

```bash
pip install -r requirements.txt
```

### Running the App
After installing the dependencies, you can run the app by executing the `main.py` file:

```bash
python main.py
```

### Capture
<img src="_sample/sample.mp4">

