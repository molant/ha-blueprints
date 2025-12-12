# Home Assistant Blueprints

A collection of advanced Home Assistant blueprints and packages with hierarchical configuration support for contact sensor monitoring.

---

## 📢 Contact Sensor Monitoring - Choose Your Approach

Get smart notifications when doors, windows, or other contact sensors are left open too long. Configure different delays and alert priorities using a four-tier hierarchy: **Entity → Area → Floor → Global**.

### **Key Features:**
- 🎯 **Four-tier hierarchy**: Entity-specific → Area-level → Floor-level → Global defaults
- 🚨 **Critical iOS notifications**: Bypass Do Not Disturb mode for important alerts
- 🔄 **Auto-clear notifications**: Automatically dismiss when sensor closes
- 🔁 **Repeat alerts**: Optional recurring notifications while sensor remains open
- 🎨 **Customizable messages**: Use variables like sensor name, area, time open
- ⚙️ **Additional conditions**: Only alert when home, during specific hours, etc.
- 🎬 **Custom actions**: Trigger additional automations on open/close events

---

## 🎯 Which Approach Should I Use?

### Option 1: **Blueprint - Global (All Sensors)** ⭐ RECOMMENDED

**Best for:** Most users who want simplicity with visual configuration.

✅ **One automation monitors ALL sensors automatically**
✅ **Visual UI configuration** (no YAML editing!)
✅ **New sensors work immediately** (no setup needed)
✅ **Easy to share** (import button)
✅ **Scales perfectly** (10 sensors or 100 sensors, same setup)

⚠️ **Global settings only** - all sensors use the same delay

**[Click to Import Blueprint](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/molant/ha-blueprints/blob/main/blueprints/contact_sensor_global_notification.yaml)**

---

### Option 2: **Blueprint - Hierarchical (Per Sensor)**

**Best for:** Users who need different delays for different sensors/areas/floors.

✅ **Hierarchical configuration** (Entity → Area → Floor → Global)
✅ **Per-sensor customization** (fridge 2min, doors 5min, windows 10min)
✅ **Visual configuration** (point-and-click setup)

⚠️ **One automation needed per sensor**
⚠️ New sensors require manual setup
⚠️ Requires YAML configuration file for hierarchy

**[Click to Import Blueprint](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/molant/ha-blueprints/blob/main/blueprints/contact_sensor_hierarchical_notification.yaml)**

---

### Option 3: **Package (Auto-Monitor All Sensors)**

**Best for:** Advanced users comfortable with YAML who want ultimate control.

✅ **One automation monitors ALL sensors automatically**
✅ **No blueprint needed** (standalone package)
✅ **Easy to customize** (edit YAML directly)

⚠️ Requires editing YAML files
⚠️ Global settings only (via input helpers)

**[📖 Package Installation](INSTALLATION.md)** | **[📦 Package File](packages/contact_sensor_auto_monitor.yaml)**

---

## Quick Comparison

| Feature | Blueprint - Global | Blueprint - Hierarchical | Package |
|---------|-------------------|-------------------------|---------|
| **Automations needed** | 1 for all sensors | 1 per sensor | 1 for all sensors |
| **New sensors** | Auto-detected ✅ | Manual setup | Auto-detected ✅ |
| **Configuration UI** | Visual ✅ | Visual + YAML | Edit YAML |
| **Per-sensor delays** | No (global only) | Yes ✅ (hierarchical) | No (global only) |
| **Easy to share** | Import button ✅ | Import button ✅ | Copy files |
| **Setup complexity** | Very Simple ✅ | Moderate | Moderate |
| **Recommended for** | Most users ⭐ | Custom config needs | YAML enthusiasts |

---

## Installation (Blueprint - Global)

### Quick Setup (5 Minutes)

1. **Import the blueprint** - Click the badge:

   [![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/molant/ha-blueprints/blob/main/blueprints/contact_sensor_global_notification.yaml)

2. **Create automation** from blueprint:
   - Go to **Settings → Automations → Create Automation → Use Blueprint**
   - Select **"Contact Sensor Left Open - Global Notification (All Sensors)"**

3. **Configure settings:**
   - **Delay**: How long before alerting (default: 10 minutes)
   - **Notification Service**: Your service (e.g., `notify.mobile_app_iphone`)
   - **Critical Notification**: Toggle ON for iOS critical alerts (optional)

4. **Save!**

Done! All contact sensors are now monitored with one automation.

---

## Installation (Package Approach)

**See the complete installation guide:** **[INSTALLATION.md](INSTALLATION.md)**

### Quick Start

1. **Enable packages** in `configuration.yaml`:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```

2. **Download the package file** to `/config/packages/contact_sensor_auto_monitor.yaml`

3. **Edit the notification service** in the package file:
   ```yaml
   notify_service: "notify.mobile_app_your_phone"  # Change this!
   ```

4. **Reload** configuration (Developer Tools → YAML → Reload All)

5. **Adjust settings** via UI (Settings → Helpers):
   - **Contact Sensor Delay (Minutes)**: How long before alerting (default: 10)
   - **Contact Sensor Critical Alert**: Toggle ON for iOS critical alerts

Done! All contact sensors are now monitored automatically with global settings.

**[📖 Full Installation Guide](INSTALLATION.md)** with troubleshooting, examples, and customization options.

---

## Installation (Blueprint Approach)

### Step 1: Import the Blueprint

Click the badge below to import the blueprint into your Home Assistant instance:

[![Import Blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://github.com/molant/ha-blueprints/blob/main/blueprints/contact_sensor_hierarchical_notification.yaml)

Or manually import via:
1. Navigate to **Settings** → **Automations & Scenes** → **Blueprints**
2. Click **Import Blueprint**
3. Enter the URL: `https://github.com/molant/ha-blueprints/blob/main/blueprints/contact_sensor_hierarchical_notification.yaml`

### Step 2: Create the Configuration Helper

The blueprint uses an `input_text` helper to store your hierarchical configuration.

1. Navigate to **Settings** → **Devices & Services** → **Helpers**
2. Click **Create Helper** → **Text**
3. Configure the helper:
   - **Name**: `Contact Sensor Config`
   - **Entity ID**: `input_text.contact_sensor_config` (or your preferred ID)
   - **Max length**: 5000 (or higher, depending on config size)
4. Click **Create**

### Step 3: Add Your Configuration

Copy the example configuration from [`config/contact_sensor_config.yaml`](config/contact_sensor_config.yaml) and paste it into your newly created helper:

1. Go to **Developer Tools** → **States**
2. Find your `input_text.contact_sensor_config` entity
3. Click on it and paste the configuration content (everything from the example file)
4. Click **Set State**

**Alternative Method** (for advanced users):

You can also manage the configuration in a separate YAML file using Home Assistant's `!include` directive:

```yaml
# configuration.yaml
input_text:
  contact_sensor_config:
    name: Contact Sensor Config
    max: 5000
    initial: !include config/contact_sensor_config.yaml
```

### Step 4: Create Automation from Blueprint

1. Navigate to **Settings** → **Automations & Scenes**
2. Click **Create Automation** → **Use Blueprint**
3. Select **Contact Sensor Left Open - Hierarchical Notification**
4. Configure the automation (see Configuration section below)

---

## Configuration

### Basic Setup

When creating an automation from the blueprint, you'll need to configure:

#### Required Settings:

- **Contact Sensor**: The binary sensor or group to monitor
- **Configuration Helper**: Select `input_text.contact_sensor_config` (or whatever you named it)
- **Notification Service**: Your notification service (e.g., `notify.mobile_app_iphone`)

#### Optional Settings:

- **Fallback Delay**: Used if config parsing fails (default: 10 minutes)
- **Fallback Critical**: Critical notification fallback (default: false)
- **Notification Title**: Template for notification title
- **Notification Message**: Template for notification message
- **Repeat Notifications**: Enable recurring alerts
- **Repeat Interval**: How often to repeat (if enabled)
- **Additional Conditions**: Extra conditions that must be met
- **Custom Actions**: Actions to run on open/close events

### Template Variables

You can use these variables in your notification title and message:

- `{{sensor_name}}` - Friendly name of the sensor
- `{{area}}` - Area the sensor is located in
- `{{floor}}` - Floor/level the sensor is located on
- `{{delay_minutes}}` - The threshold delay that was applied
- `{{time_open}}` - How long the sensor has been open (human-readable)

**Example Custom Message:**
```
⚠️ {{sensor_name}} in {{area}} has been open for {{time_open}}!
```

---

## Understanding the Hierarchy

The blueprint checks configurations in this order:

```
1. Entity-specific override (highest priority)
   ↓ (if not found)
2. Area-level override (rooms like Kitchen, Bedroom)
   ↓ (if not found)
3. Floor-level override (levels like Upstairs, Downstairs)
   ↓ (if not found)
4. Global default
   ↓ (if not found)
5. Blueprint fallback
```

**Why this order?**
- **Entity** overrides are most specific (individual sensor needs)
- **Area** overrides apply to rooms/spaces (Kitchen needs different settings than Bedroom)
- **Floor** overrides apply to entire levels (Upstairs bedrooms share similar needs)
- **Global** is the fallback for everything else

### Example Scenarios

#### Scenario 1: Fridge Door (Entity-Specific Override)

```yaml
# Entity: binary_sensor.fridge_door
# Area: Kitchen
# Floor: Downstairs

entity_overrides:
  binary_sensor.fridge_door:
    delay_minutes: 2
    critical: true
```

**Result**: Alert after **2 minutes** with **critical** notification (entity override wins)

---

#### Scenario 2: Front Door (Area-Level Override)

```yaml
# Entity: binary_sensor.front_door
# Area: "Front Door"
# Floor: Downstairs

area_overrides:
  "Front Door":
    delay_minutes: 5
    critical: true
```

**Result**: Alert after **5 minutes** with **critical** notification (area override wins)

---

#### Scenario 3: Guest Bedroom Window (Floor-Level Override)

```yaml
# Entity: binary_sensor.guest_bedroom_window
# Area: "Guest Bedroom" (no area override defined)
# Floor: Upstairs

floor_overrides:
  Upstairs:
    delay_minutes: 12
    critical: false
```

**Result**: Alert after **12 minutes** with **standard** notification (floor override applies)

---

#### Scenario 4: Random Sensor (Global Default)

```yaml
# Entity: binary_sensor.shed_door
# Area: "Shed" (no area override defined)
# Floor: not assigned to any floor

global_defaults:
  delay_minutes: 10
  critical: false
```

**Result**: Alert after **10 minutes** with **standard** notification (global default applies)

---

## Configuration Examples

### Example 1: Minimal Configuration

```yaml
global_defaults:
  delay_minutes: 10
  critical: false
```

Simple setup where all sensors alert after 10 minutes with standard notifications.

---

### Example 2: Area-Based Security Zones

```yaml
global_defaults:
  delay_minutes: 15
  critical: false

area_overrides:
  "Front Door":
    delay_minutes: 5
    critical: true

  "Back Door":
    delay_minutes: 5
    critical: true

  Garage:
    delay_minutes: 30
    critical: false
```

Entry points get quick, critical alerts. Garage has a longer delay. All other sensors use the 15-minute default.

---

### Example 3: Appliance-Specific Alerts

```yaml
global_defaults:
  delay_minutes: 10
  critical: false

entity_overrides:
  binary_sensor.fridge_door:
    delay_minutes: 2
    critical: true

  binary_sensor.freezer_door:
    delay_minutes: 3
    critical: true

  binary_sensor.dishwasher_door:
    delay_minutes: 30
    critical: false
```

Fridge and freezer get immediate critical alerts. Dishwasher is less urgent. Other sensors use global defaults.

---

### Example 4: Floor-Based Climate Control

```yaml
global_defaults:
  delay_minutes: 10
  critical: false

floor_overrides:
  Upstairs:
    delay_minutes: 12
    critical: false

  Downstairs:
    delay_minutes: 10
    critical: false

  Basement:
    delay_minutes: 20
    critical: false

entity_overrides:
  binary_sensor.attic_window:
    delay_minutes: 5
    critical: true  # Attic can heat up fast!
```

Different delays for different floors (levels). Upstairs bedrooms get 12 minutes, Basement gets 20 minutes. Attic window gets special handling. All other areas on each floor inherit that floor's settings.

---

### Example 5: Combined Floor and Area Hierarchy

```yaml
global_defaults:
  delay_minutes: 10
  critical: false

floor_overrides:
  Upstairs:
    delay_minutes: 15  # Bedrooms - longer delays
    critical: false

  Downstairs:
    delay_minutes: 10
    critical: false

area_overrides:
  "Master Bedroom":
    delay_minutes: 20  # Override floor setting for this room
    critical: false

  Kitchen:
    delay_minutes: 8
    critical: false

  "Front Door":
    delay_minutes: 5
    critical: true

entity_overrides:
  binary_sensor.fridge_door:
    delay_minutes: 2
    critical: true
```

This shows the full hierarchy in action:
- All Upstairs rooms default to 15 minutes (floor override)
- Master Bedroom gets 20 minutes (area override beats floor)
- Kitchen and Front Door have specific settings (area overrides)
- Fridge door gets highest priority (entity override)

---

## Using Binary Sensor Groups

You can monitor multiple sensors as a single unit using binary sensor groups:

### Step 1: Create a Binary Sensor Group

```yaml
# configuration.yaml
binary_sensor:
  - platform: group
    name: "All Exterior Doors"
    device_class: door
    entities:
      - binary_sensor.front_door
      - binary_sensor.back_door
      - binary_sensor.garage_door
      - binary_sensor.side_door
```

### Step 2: Create Automation

Create an automation using the blueprint and select `binary_sensor.all_exterior_doors` as the contact sensor.

### Step 3: Configure the Group in Your Config

```yaml
entity_overrides:
  binary_sensor.all_exterior_doors:
    delay_minutes: 5
    critical: true
```

**Result**: Any exterior door left open for 5 minutes triggers a critical notification. The notification clears when ALL doors are closed.

---

## Advanced Usage

### Conditional Notifications

Use **Additional Conditions** to only send alerts when specific conditions are met:

**Example: Only alert when away from home**
```yaml
# In the automation, add this condition:
condition:
  - condition: not
    conditions:
      - condition: zone
        entity_id: person.your_name
        zone: zone.home
```

**Example: Only alert during nighttime**
```yaml
condition:
  - condition: time
    after: "22:00:00"
    before: "06:00:00"
```

---

### Custom Actions

Use **Custom Actions** to trigger additional automations:

**Example: Flash lights when door left open**
```yaml
# Custom Actions (On Open Alert):
- service: light.turn_on
  target:
    entity_id: light.hallway
  data:
    flash: long

# Custom Actions (On Close):
- service: light.turn_off
  target:
    entity_id: light.hallway
```

**Example: Announce via TTS**
```yaml
# Custom Actions (On Open Alert):
- service: tts.google_translate_say
  target:
    entity_id: media_player.living_room_speaker
  data:
    message: "Warning: {{sensor_name}} has been left open"
```

---

### Repeat Notifications

Enable **Repeat Notifications** to get recurring reminders:

- **Enable Repeat Notifications**: ✓ On
- **Repeat Interval**: 30 minutes

The automation will send a new notification every 30 minutes while the sensor remains open. Each notification updates with the current time the sensor has been open.

---

## Tips and Best Practices

### 1. Start Simple
Begin with a basic global default and add overrides as needed:
```yaml
global_defaults:
  delay_minutes: 10
  critical: false
```

### 2. Use Floor Overrides for Broad Categorization
Set different defaults for different levels of your home:
```yaml
floor_overrides:
  Upstairs:
    delay_minutes: 15  # Bedrooms typically
  Downstairs:
    delay_minutes: 10  # Main living areas
  Basement:
    delay_minutes: 20  # Less frequently used
```

### 3. Use Area Overrides for Specific Rooms
Override floor settings for rooms with special requirements:
```yaml
area_overrides:
  Kitchen:
    delay_minutes: 8
  "Master Bedroom":
    delay_minutes: 20  # Overrides the Upstairs floor default
  "Front Door":
    delay_minutes: 5
    critical: true
```

### 4. Reserve Entity Overrides for Special Cases
Only use entity-specific overrides for sensors with unique requirements:
- Appliances (fridge, freezer)
- High-security items (safe, medicine cabinet)
- Sensors with unusual behavior

### 5. Understand the Hierarchy Benefits
Instead of setting 5 bedrooms individually, use:
```yaml
floor_overrides:
  Upstairs: 15 minutes  # All bedrooms inherit this

area_overrides:
  "Master Bedroom": 20 minutes  # Exception for one room
```

### 6. Critical Notifications
Use critical notifications sparingly. They bypass Do Not Disturb and can be disruptive:
- Entry points (when away)
- Security sensors
- Safety-critical appliances

### 7. Test Your Configuration
After making changes:
1. Leave a sensor open and verify the timing
2. Check that notifications appear correctly
3. Confirm critical notifications work as expected
4. Test that notifications clear when sensor closes
5. Use Home Assistant's Developer Tools → Template to verify which floor/area a sensor belongs to

### 8. Document Your Choices
Add comments in your configuration explaining why you chose specific values:
```yaml
entity_overrides:
  binary_sensor.fridge_door:
    delay_minutes: 2  # Food safety - need quick alert
    critical: true
```

### 9. Review and Adjust
Periodically review your configuration:
- Are the delays appropriate?
- Are you getting too many/too few notifications?
- Can any entity-specific overrides be consolidated to area or floor overrides?

---

## Troubleshooting

### Notifications Not Working

1. **Check the config helper**: Make sure `input_text.contact_sensor_config` contains valid YAML
2. **Verify notification service**: Test your notification service manually
3. **Check automation trace**: View the automation trace in Home Assistant to see what's happening
4. **Review conditions**: Make sure any additional conditions you added are being met

### Wrong Delay or Notification Type

1. **Check entity ID**: Ensure the entity ID in your config matches exactly (case-sensitive)
2. **Check area name**: Verify the area name matches exactly (case-sensitive)
3. **Check floor name**: Verify the floor name matches exactly (case-sensitive)
4. **Review hierarchy**: Remember: entity → area → floor → global → fallback
5. **Verify floor assignment**: Use Developer Tools → Template to check what floor Home Assistant has assigned to the sensor's area

### Config Helper Not Parsing

1. **Validate YAML**: Use a YAML validator to check your config syntax
2. **Check indentation**: YAML is sensitive to indentation (use spaces, not tabs)
3. **Review length limit**: Make sure your config fits within the helper's max length
4. **Check for special characters**: Some characters may need to be quoted

### Critical Notifications Not Working (iOS)

1. **Check iOS settings**: Ensure the Home Assistant app has critical notification permission
2. **Verify notification data**: Check the automation trace to see if critical data is being sent
3. **Test manually**: Send a test critical notification from Developer Tools

---

## Development

If you want to contribute or create your own blueprints, see [DEVELOPMENT.md](DEVELOPMENT.md) for:
- Setting up linting and validation (Python-based)
- Blueprint development guidelines
- Testing procedures
- Git workflow

### Quick Start for Contributors

```bash
# Install dependencies
pip install -r requirements.txt

# Validate your changes
python scripts/validate.py

# Or run specific checks:
python scripts/validate.py lint      # YAML linting only
python scripts/validate.py validate  # Blueprint validation only
```

---

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

## License

MIT License - feel free to use and modify as needed.

---

## Credits

Created for the Home Assistant community. Inspired by the need for flexible, per-sensor notification thresholds without creating dozens of individual automations.

---

## Support

If you find this blueprint useful, please star the repository and share it with others!

For issues or questions:
- Open an issue on GitHub
- Visit the Home Assistant Community Forum
- Check the Home Assistant Blueprint Exchange

---

## Changelog

### v1.0.0 (Initial Release)
- Four-tier hierarchical configuration system
- Entity, area, floor, and global override support
- Critical iOS notifications
- Auto-clear on sensor close
- Repeat notifications
- Binary sensor group support
- Customizable messages with variables (including floor)
- Additional conditions support
- Custom actions on open/close events
