# Brightness Control

This tool brings simple, graphical hardware control for external monitors straight to your Linux desktop. It was created to provide an easy way to change your monitor's brightness on Linux, similar to the experience provided by the Twinkle Tray app on Windows.

### Features
* **Simple GUI:** Adjust external monitor brightness via a clean GTK interface.
* **Advanced Color Control:** Includes expandable settings to fine-tune Contrast, Red, Green, and Blue levels.
* **Hardware Detection:** Automatically scans for monitors supporting DDC/CI commands.
* **Persistent Settings:** Saves your preferences and restores them the next time you open the app.

### Requirements
To run this application (either manually or via the installer), your system needs:
* **Python 3** with **GTK 3** bindings (`gi.repository`).
* **`ddcutil`**: The backend tool used to communicate with your monitor.
* **I2C Permissions**: Your user must have permission to access `/dev/i2c-*` devices.

### Installation

#### Option 1: Full Installation (Recommended)
The provided `install.sh` script is designed to make the process easier by automating the dependency checks, hardware configuration, and menu integration.
1. Download both the python script and `install.sh` into the same folder.
2. Make the script executable: 
   ```bash
   chmod +x install.sh
   ```
3. Run the installer as a normal user (it will prompt for `sudo` only when needed): 
   ```bash
   ./install.sh
   ```
4. **CRITICAL:** You must log out and log back in for the new hardware permissions to take effect.

*Note: The installer automatically installs `ddcutil`, enables the `i2c-dev` module, adds your user to the `i2c` group, and creates a desktop shortcut.*

#### Option 2: Quick Run (Portable)
If you already have the dependencies installed and your user has the correct permissions (i.e., you are in the `i2c` group), you can run the script directly without installing anything to your system:
```bash
python3 brightness-control.py
```

### Usage
Once installed and logged back in, search for **Brightness Control** in your application launcher. The app will show a loading spinner while it scans for compatible monitors before displaying the control sliders.
