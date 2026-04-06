#!/bin/bash

# Ensure script is not run as root, but can call sudo
if [ "$EUID" -eq 0 ]; then
  echo "Please do not run this script as root/sudo directly."
  echo "The script will ask for sudo when needed."
  exit 1
fi

echo "Starting installation of Monitor Control control..."

# 1. Check for Python script
if [ ! -f "brightness-control.py" ]; then
    echo "Error: brightness-control.py not found in the current directory."
    exit 1
fi

# 2. Install ddcutil if missing
if ! command -v ddcutil &> /dev/null; then
    echo "Installing ddcutil dependency..."
    sudo apt update && sudo apt install -y ddcutil
fi

# 3. Setup Hardware Permissions
echo "Configuring I2C kernel module and permissions..."
sudo modprobe i2c-dev

# Add to /etc/modules so it persists after reboot
if ! grep -q "i2c-dev" /etc/modules; then
    echo "i2c-dev" | sudo tee -a /etc/modules > /dev/null
    echo "Added i2c-dev to /etc/modules."
fi

# Add user to i2c group
if ! groups $USER | grep -q "\bi2c\b"; then
    sudo usermod -aG i2c $USER
    echo "Added $USER to i2c group."
fi

# 4. Install Files
echo "Installing application files..."
mkdir -p "$HOME/.local/bin"
cp brightness-control.py "$HOME/.local/bin/brightness-control"
chmod +x "$HOME/.local/bin/brightness-control"

# 5. Create Desktop Entry
mkdir -p "$HOME/.local/share/applications"
cat <<EOF > "$HOME/.local/share/applications/brightness-control.desktop"
[Desktop Entry]
Name=Brightness Control
Comment=Advanced Brightness and Color Control
Exec=$HOME/.local/bin/brightness-control
Icon=display-brightness-symbolic
Terminal=false
Type=Application
Categories=Utility;Settings;
EOF

update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null

echo "Installation complete."
echo "CRITICAL: You must LOG OUT and LOG IN again for group permissions to apply."
echo "After logging back in, you can find 'Monitor Control' in your application menu."
