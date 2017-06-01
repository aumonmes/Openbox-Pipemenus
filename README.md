# Openbox Pipemenus
A set of different pipemenus for openbox


## pipe-dirbrowser.sh
This is a pipemenu to browse folders recursively. It opens files and directories using `xdg-open` so it's not necessary to be configuring preferred applications in the script.

### Usage
```xml
<!--
  $SCRIPT // Path to the script
  $PATH   // Path to start browsing
  $LABEL  // Name to show for the pipemenu
-->
<menu execute="$SCRIPT $PATH" id="pipe-dirbrowser" label="$LABEL" />
```

### Configuration
Inside the script there's two variables to set some configuration
```sh
SHOW_HIDDEN=false;   # Allow/disable listing hidden files
SHOW_FULLPATH=false; # Show the full path of the folder in the title or only the current folder's name
```

### Known bugs
* It can't open files with an apostrofe `'` in their names


## pipe-virsh.py
This is a pipemenu to manage virtual machines using `virsh`. It uses Python 3.

### Usage
```xml
<!--
  $SCRIPT // Path to the script
  $LABEL  // Name to show for the pipemenu
-->
<menu execute="$SCRIPT" id="pipe-virsh" label="$LABEL" />
```

### Configuration
The only configuration is to show/hide unicode characters for the actions, in case the user's font doesn't have them
```python
FULL_UNICODE = False
```
