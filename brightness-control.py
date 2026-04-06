#!/usr/bin/env python3
import gi
import os
import json
import subprocess
import threading

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

CONFIG_DIR = os.path.expanduser("~/.config/brightness_control")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# VCP Codes for DDC/CI hardware control
VCP = {
    "brightness": "10",
    "contrast": "12",
    "red": "16",
    "green": "18",
    "blue": "1a"
}

class BrightnessWindow(Gtk.Window):
    def __init__(self):
        super().__init__()
        
        # UI Setup
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.set_title("Brightness Control")
        self.set_titlebar(self.header)

        self.set_border_width(12)
        self.set_default_size(400, -1)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.main_box)

        # Loading Spinner View
        self.spinner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.spinner = Gtk.Spinner()
        self.spinner.start()
        self.spinner_box.pack_start(self.spinner, True, True, 10)
        self.spinner_box.pack_start(Gtk.Label(label="Scanning for monitors..."), False, False, 0)
        self.main_box.pack_start(self.spinner_box, True, True, 0)

        self.settings = self.load_settings()
        
        # Scan hardware in a separate thread to prevent UI lag
        threading.Thread(target=self.detect_monitors, daemon=True).start()

    def load_settings(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    return json.load(f)
            except: pass
        return {}

    def save_setting(self, display_id, feature, value):
        if display_id not in self.settings:
            self.settings[display_id] = {}
        self.settings[display_id][feature] = value
        os.makedirs(CONFIG_DIR, exist_ok=True)
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.settings, f)
        except: pass

    def detect_monitors(self):
        monitors = []
        try:
            # Brief mode is faster for detection
            output = subprocess.check_output(['/usr/bin/ddcutil', 'detect', '--brief'], text=True)
            for line in output.split('\n'):
                if line.startswith('Display'):
                    parts = line.split()
                    if len(parts) >= 2:
                        d_id = parts[1]
                        monitors.append({'id': d_id, 'name': f"Display {d_id}"})
        except: pass
        GLib.idle_add(self.build_ui, monitors)

    def create_slider(self, label_text, icon_name, default_val, display_id, vcp_key):
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.MENU)
        
        label = Gtk.Label(label=label_text)
        label.set_width_chars(10)
        label.set_xalign(0)

        adj = Gtk.Adjustment(float(default_val), 0, 100, 1, 10, 0)
        scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adj)
        scale.set_hexpand(True)
        scale.set_digits(0)
        
        scale.connect("button-release-event", self.on_slider_change, display_id, vcp_key)
        
        hbox.pack_start(icon, False, False, 0)
        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(scale, True, True, 0)
        return hbox

    def build_ui(self, monitors):
        self.spinner.stop()
        self.main_box.remove(self.spinner_box)

        if not monitors:
            lbl = Gtk.Label(label="No DDC/CI monitors detected.\nEnsure i2c-dev is loaded and you are in the i2c group.")
            self.main_box.pack_start(lbl, True, True, 20)
        else:
            for mon in monitors:
                m_id = str(mon['id'])
                m_cache = self.settings.get(m_id, {})

                frame = Gtk.Frame(label=f" {mon['name']} ")
                vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
                vbox.set_border_width(10)
                frame.add(vbox)

                # Brightness (Main)
                val_b = m_cache.get("brightness", 50)
                vbox.pack_start(self.create_slider("Brightness", "display-brightness-symbolic", val_b, m_id, "brightness"), False, False, 0)

                # Advanced Section
                expander = Gtk.Expander(label="Advanced Settings (Contrast/RGB)")
                adv_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
                adv_vbox.set_border_width(5)
                
                adv_vbox.pack_start(self.create_slider("Contrast", "contrast-high-symbolic", m_cache.get("contrast", 50), m_id, "contrast"), False, False, 0)
                adv_vbox.pack_start(self.create_slider("Red", "color-management-symbolic", m_cache.get("red", 100), m_id, "red"), False, False, 0)
                adv_vbox.pack_start(self.create_slider("Green", "color-management-symbolic", m_cache.get("green", 100), m_id, "green"), False, False, 0)
                adv_vbox.pack_start(self.create_slider("Blue", "color-management-symbolic", m_cache.get("blue", 100), m_id, "blue"), False, False, 0)

                expander.add(adv_vbox)
                vbox.pack_start(expander, False, False, 0)
                self.main_box.pack_start(frame, False, False, 5)

        self.show_all()

    def on_slider_change(self, control, event, display_id, vcp_key):
        val = int(control.get_value())
        self.save_setting(display_id, vcp_key, val)
        vcp_code = VCP[vcp_key]
        subprocess.Popen(['/usr/bin/ddcutil', '--display', display_id, 'setvcp', vcp_code, str(val)])

if __name__ == "__main__":
    win = BrightnessWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
