# Home Assistant Contact Sensor Blueprints

Smart notifications when doors, windows, or other contact sensors are left open too long.

---

## 🎯 Which Blueprint Should I Use?

### Option 1: **Global Notification (Multiple Sensors)** ⭐ RECOMMENDED

**Best for:** Most users who want simple, global settings for all their contact sensors.

✅ **One automation for all sensors**
✅ **Visual UI configuration** (no YAML editing!)
✅ **Select sensors from dropdown** (filtered to show only doors/windows)
✅ **Select devices from dropdown** (no typing service names!)
✅ **Easy to share** (import button)
✅ **Quick setup** (5 minutes)

⚠️ **Global settings** - all sensors use the same delay
⚠️ **New sensors need to be added** - edit automation to select them

**[📥 Click to Import](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/molant/ha-blueprints/blob/main/blueprints/contact_sensor_global_notification.yaml)**

---

### Option 2: **Hierarchical Notification (Per Sensor)**

**Best for:** Users who need different delays for different sensors/areas/floors.

✅ **Hierarchical configuration** (Entity → Area → Floor → Global)
✅ **Per-sensor customization** (fridge 2min, doors 5min, windows 10min)
✅ **Visual configuration** (point-and-click setup)

⚠️ **One automation per sensor** (not scalable for many sensors)
⚠️ **More complex setup** (requires YAML configuration file)

**[📥 Click to Import](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/molant/ha-blueprints/blob/main/blueprints/contact_sensor_hierarchical_notification.yaml)**

---

## Quick Comparison

| Feature | Global | Hierarchical |
|---------|--------|--------------|
| **Automations needed** | 1 for all sensors | 1 per sensor |
| **Sensor selection** | Multi-select dropdown | Individual selection |
| **Configuration** | Visual sliders/toggles | Visual + YAML file |
| **Per-sensor delays** | No (global only) | Yes ✅ |
| **Setup time** | 5 minutes | 15-30 minutes |
| **Best for** | Most users ⭐ | Advanced customization |

---

## Installation - Global Notification

### Quick Setup (5 Minutes)

1. **Import the blueprint** - Click the badge:

   [![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/molant/ha-blueprints/blob/main/blueprints/contact_sensor_global_notification.yaml)

2. **Create automation** from blueprint:
   - Go to **Settings → Automations → Create Automation → Use Blueprint**
   - Select **"Contact Sensor Left Open - Global Notification"**

3. **Configure settings:**
   - **Contact Sensors**: Select all sensors to monitor
     - The dropdown filters to show only doors, windows, garage doors, etc.
     - You can select multiple sensors at once
     - **Tip:** Click the dropdown, then use Ctrl+A (or Cmd+A) to select all visible sensors
   - **Delay**: How long before alerting (default: 10 minutes)
   - **Devices to Notify**: Select your mobile devices
   - **Critical Notification**: Toggle ON for iOS critical alerts (optional)

4. **Save!**

**Done!** All selected contact sensors are now monitored with one automation.

### Adding New Sensors Later

When you add a new contact sensor:
1. Go to **Settings → Automations**
2. Find your "Contact Sensor Left Open" automation
3. Click **Edit**
4. In **Contact Sensors**, add the new sensor to the list
5. **Save**

---

## Installation - Hierarchical Notification

### Setup (15-30 Minutes)

1. **Import the blueprint:**

   [![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/molant/ha-blueprints/blob/main/blueprints/contact_sensor_hierarchical_notification.yaml)

2. **Create a configuration helper:**
   - Go to **Settings → Devices & Services → Helpers**
   - Click **Create Helper** → **Text**
   - **Name**: `Contact Sensor Config`
   - **Max length**: 5000
   - Click **Create**

3. **Add your hierarchical configuration:**
   - See [`config/contact_sensor_config.yaml`](config/contact_sensor_config.yaml) for examples
   - Go to **Developer Tools** → **States**
   - Find your `input_text.contact_sensor_config` entity
   - Paste your configuration and click **Set State**

4. **Create automation for each sensor:**
   - Go to **Settings → Automations → Create Automation → Use Blueprint**
   - Select **"Contact Sensor Left Open - Hierarchical Notification"**
   - Configure for one sensor
   - Repeat for each sensor you want to monitor

---

## Features

### Common Features (Both Blueprints)

- ✅ **Auto-clear notifications** - Automatically dismiss when sensor closes
- ✅ **Critical iOS notifications** - Bypass Do Not Disturb mode
- ✅ **Repeat alerts** - Optional recurring notifications while sensor remains open
- ✅ **Customizable messages** - Use variables like sensor name, area, time open
- ✅ **Additional conditions** - Only alert when home, during specific hours, etc.
- ✅ **Custom actions** - Trigger lights, TTS, or other automations

### Global Notification Specific

- ✅ **Multi-sensor selection** - One automation monitors many sensors
- ✅ **Device selection** - Choose notification targets from dropdown
- ✅ **Simple configuration** - Just sliders and toggles

### Hierarchical Notification Specific

- ✅ **Four-tier hierarchy** - Entity → Area → Floor → Global
- ✅ **Per-sensor delays** - Fridge: 2min, Doors: 5min, Windows: 10min
- ✅ **Binary sensor groups** - Monitor multiple sensors as one

---

## Configuration Examples

### Global Notification - Basic Setup

**Settings in the automation:**
- **Contact Sensors**: Select all doors and windows
- **Delay**: 10 minutes
- **Devices to Notify**: Your phone
- **Critical Notification**: OFF

**Result:** All selected sensors alert after 10 minutes if left open.

---

### Global Notification - Security Focused

**Settings in the automation:**
- **Contact Sensors**: All exterior doors and windows
- **Delay**: 5 minutes
- **Devices to Notify**: All family phones
- **Critical Notification**: ON
- **Additional Conditions**: Only when away from home

**Result:** Critical alerts on all phones after 5 minutes, only when away.

---

### Hierarchical Notification - Advanced

**Configuration in helper:**
```yaml
global_defaults:
  delay_minutes: 10
  critical: false

floor_overrides:
  Upstairs:
    delay_minutes: 15  # Bedrooms - longer delays

area_overrides:
  "Front Door":
    delay_minutes: 5
    critical: true
  Kitchen:
    delay_minutes: 8

entity_overrides:
  binary_sensor.fridge_door:
    delay_minutes: 2
    critical: true
```

**Result:**
- Fridge: 2min critical
- Front Door: 5min critical
- Kitchen sensors: 8min standard
- Upstairs sensors: 15min standard
- All others: 10min standard

See [`config/contact_sensor_config.yaml`](config/contact_sensor_config.yaml) for more examples.

---

## Troubleshooting

### Sensors not showing in dropdown

**Issue:** Contact sensors don't appear in the sensor selection dropdown.

**Solution:**
1. Check that the sensor has the correct `device_class`:
   - Go to **Developer Tools → States**
   - Find your sensor
   - Check the `device_class` attribute
   - Should be: `door`, `window`, `opening`, or `garage_door`

2. If missing or incorrect, add to `customize.yaml`:
```yaml
binary_sensor.my_sensor:
  device_class: door
```

---

### Notifications not working

**Check:**
1. ✅ Mobile app is installed and logged in
2. ✅ Notification permissions granted in phone settings
3. ✅ Selected the correct devices in the automation
4. ✅ Test by triggering manually: **Developer Tools → Actions** → Test your notify service

---

### Critical notifications not working (iOS)

**Check:**
1. ✅ Go to iOS **Settings → Notifications → Home Assistant**
2. ✅ Ensure **Critical Alerts** is enabled
3. ✅ Test with a manual critical notification

---

## Tips & Best Practices

### For Global Notification Users

**Tip 1: Select All Sensors at Once**
- Click the Contact Sensors dropdown
- Use **Ctrl+A** (Windows/Linux) or **Cmd+A** (Mac) to select all
- Or manually select the sensors you want

**Tip 2: Create Multiple Automations for Different Delays**
- Create one automation for "Quick alerts" (doors, 5min)
- Create another for "Slow alerts" (windows, 15min)
- Each automation has its own sensor list and delay

**Tip 3: Use Labels to Organize**
- Assign labels to sensors in Home Assistant
- Makes it easier to remember which sensors are monitored
- Example labels: "monitored", "security", "climate"

---

### For Hierarchical Notification Users

See the full documentation in [`config/contact_sensor_config.yaml`](config/contact_sensor_config.yaml).

---

## Support & Contributing

- 🐛 **Issues**: [GitHub Issues](https://github.com/molant/ha-blueprints/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/molant/ha-blueprints/discussions)
- ⭐ **Star the repo** if you find this useful!

---

## License

MIT License - Use and share freely!

---

## Changelog

### v2.0.0
- Added Global Notification blueprint with multi-sensor selection
- Added device selection dropdown (no more typing service names!)
- Removed package approach (use blueprints instead)
- Updated documentation

### v1.0.0
- Initial release with Hierarchical Notification blueprint
- Four-tier hierarchy support
- Critical iOS notifications
- Auto-clear and repeat notifications
