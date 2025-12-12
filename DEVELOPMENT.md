# Development Guide

This guide explains how to develop and validate blueprints in this repository.

## Prerequisites

- **Python** (v3.8 or higher)
- **pip** (Python package manager)
- **Git**

## Setup

### 1. Install Dependencies

```bash
# Install Python dependencies (yamllint, PyYAML)
pip install -r requirements.txt

# Install pre-commit (optional, for git hooks)
pip install pre-commit
```

**Alternative: Using a virtual environment (recommended)**

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install pre-commit
```

### 2. Enable Pre-commit Hooks (Optional)

Pre-commit hooks will automatically validate your changes before each commit:

```bash
pre-commit install
```

## Linting and Validation

This repository includes comprehensive linting and validation tools to ensure blueprint quality.

### YAML Linting

We use [yamllint](https://yamllint.readthedocs.io/) to check YAML syntax and style.

```bash
# Lint all YAML files (using the validation script)
python scripts/validate.py lint

# Or run yamllint directly:
yamllint .                # All files
yamllint blueprints/      # Only blueprints
yamllint config/          # Only config files
```

**Configuration**: See [.yamllint](.yamllint) for linting rules.

### Blueprint Validation

We have a custom Python validator that checks Home Assistant blueprint structure:

```bash
# Validate all blueprints
python scripts/validate.py validate
```

The validator checks for:
- ✅ Valid YAML syntax
- ✅ Required blueprint keys (`blueprint`, `trigger`, `action`)
- ✅ Required metadata (`name`, `description`, `domain`)
- ✅ Valid domain values
- ✅ Proper input definitions
- ✅ Trigger platform specifications
- ✅ Common mistakes (tabs, unclosed templates, indentation issues)
- ⚠️ Warnings for missing defaults, mode settings, etc.

### Run All Checks

```bash
# Run both linting and validation (recommended)
python scripts/validate.py
```

## Common Issues and Fixes

### YAML Indentation Errors

**Problem**: `expected <block end>, but found '?'`

This usually means incorrect indentation. In Home Assistant blueprints, the `default` key in a `choose` action must align with the dash before `conditions`:

```yaml
# ❌ Wrong
- choose:
    - conditions:
        - condition: ...
      sequence:
        - service: ...
      default:  # Too far indented
        - service: ...

# ✅ Correct
- choose:
    - conditions:
        - condition: ...
      sequence:
        - service: ...
  default:  # Aligned with the dash before 'conditions'
    - service: ...
```

### Tabs vs Spaces

**Problem**: YAML files must use spaces, not tabs.

**Fix**: Configure your editor to use spaces (2 spaces per indent level):

**VSCode** (.vscode/settings.json):
```json
{
  "[yaml]": {
    "editor.tabSize": 2,
    "editor.insertSpaces": true
  }
}
```

### Condition Input Usage

**Problem**: `condition: !input additional_conditions` in a list

**Fix**: Use `!input` directly as the condition value, not in a list:

```yaml
# ❌ Wrong
condition:
  - condition: !input additional_conditions

# ✅ Correct
condition: !input additional_conditions
```

## Creating a New Blueprint

### 1. Create the Blueprint File

```bash
# Create in blueprints/ directory
touch blueprints/my_new_blueprint.yaml
```

### 2. Use the Template Structure

```yaml
blueprint:
  name: My Blueprint Name
  description: >
    A detailed description of what this blueprint does.
    Can span multiple lines.
  domain: automation

  input:
    # Define your inputs here
    my_sensor:
      name: Sensor
      description: The sensor to monitor
      selector:
        entity:
          domain: binary_sensor

# Optional automation settings
mode: restart
max_exceeded: silent

# Optional variables
variables:
  sensor_id: !input my_sensor

# Required: triggers
trigger:
  - platform: state
    entity_id: !input my_sensor

# Optional: conditions
condition: []

# Required: actions
action:
  - service: notify.notify
    data:
      message: "Sensor triggered"
```

### 3. Validate Your Blueprint

```bash
npm run validate
```

### 4. Test Import

Before committing, test importing the blueprint in Home Assistant:

1. Copy the blueprint content
2. Go to Settings → Automations & Scenes → Blueprints
3. Click Import Blueprint
4. Paste your local file path or use the GitHub URL format

## Git Workflow

### Before Committing

If you have pre-commit hooks installed:
```bash
git add .
git commit -m "Your message"
# Pre-commit hooks will run automatically
```

Manual validation:
```bash
python scripts/validate.py
git add .
git commit -m "Your message"
```

### Pull Request Checks

When you create a pull request, GitHub Actions will automatically:
1. ✅ Lint all YAML files
2. ✅ Validate all blueprints
3. ✅ Run additional checks

View the results in the "Actions" tab of your PR.

## Directory Structure

```
ha-blueprints/
├── .github/
│   └── workflows/
│       └── validate.yml       # CI/CD workflow
├── blueprints/                # Blueprint files
│   └── *.yaml
├── config/                    # Example configurations
│   └── *.yaml
├── scripts/
│   └── validate-blueprints.js # Custom validator
├── .yamllint                  # YAML linting config
├── .pre-commit-config.yaml    # Pre-commit hooks config
├── package.json               # Node.js dependencies and scripts
└── README.md                  # User documentation
```

## Validation Rules

### Required Blueprint Structure

Every blueprint MUST have:
- `blueprint` section with `name`, `description`, and `domain`
- `trigger` section (array)
- `action` section (array)

### Recommended Practices

- Set `mode` for automations (e.g., `restart`, `single`, `parallel`)
- Provide `default` values for inputs when sensible
- Use descriptive names and descriptions
- Add comments for complex logic
- Use 2-space indentation consistently
- Keep lines under 120 characters when possible

### Common Warnings

The validator will warn about:
- Missing default values for inputs
- Very short descriptions (< 10 characters)
- Missing `mode` setting for automations
- Tabs instead of spaces
- Possible unclosed template expressions
- Potential indentation issues

## Troubleshooting

### Validation Fails But YAML Looks Correct

1. Check for invisible characters (tabs, special spaces)
2. Verify indentation is exactly 2 spaces per level
3. Ensure no trailing spaces on empty lines
4. Check for smart quotes (`"` `"`) instead of straight quotes (`"`)

### Pre-commit Hooks Not Running

```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install

# Test hooks manually
pre-commit run --all-files
```

### yamllint Not Found

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install in a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Resources

- [Home Assistant Blueprint Documentation](https://www.home-assistant.io/docs/blueprint/)
- [YAML Specification](https://yaml.org/spec/)
- [yamllint Documentation](https://yamllint.readthedocs.io/)
- [Pre-commit Framework](https://pre-commit.com/)

## Getting Help

- Check the [README](README.md) for blueprint usage
- Review [existing blueprints](blueprints/) for examples
- Open an issue on GitHub for bugs or questions
