#!/usr/bin/env python3
"""
Home Assistant Blueprint Validation Tool

This script provides both YAML linting and blueprint structure validation.

Usage:
    python validate.py              # Run all validations (lint + validate)
    python validate.py lint         # Run only YAML linting
    python validate.py validate     # Run only blueprint validation
    python validate.py help         # Show this help

Requirements:
    pip install -r requirements.txt
"""

import sys
import subprocess
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional


# ============================================================================
# Home Assistant YAML Tag Support
# ============================================================================

def input_constructor(loader, node):
    """Constructor for !input tag"""
    return f"!input {loader.construct_scalar(node)}"


def include_constructor(loader, node):
    """Constructor for !include tag"""
    return f"!include {loader.construct_scalar(node)}"


def secret_constructor(loader, node):
    """Constructor for !secret tag"""
    return f"!secret {loader.construct_scalar(node)}"


# Register custom Home Assistant YAML tags
yaml.SafeLoader.add_constructor('!input', input_constructor)
yaml.SafeLoader.add_constructor('!include', include_constructor)
yaml.SafeLoader.add_constructor('!secret', secret_constructor)


# ============================================================================
# YAML Linting
# ============================================================================

def run_yamllint(path: str = ".") -> bool:
    """Run yamllint on the specified path"""
    print("\n" + "=" * 60)
    print("Running YAML Linter (yamllint)")
    print("=" * 60)

    try:
        result = subprocess.run(
            ["yamllint", path],
            capture_output=False,
            text=True
        )
        success = result.returncode == 0

        if success:
            print("\n[PASS] YAML linting passed!")
        else:
            print("\n[FAIL] YAML linting failed!")

        return success

    except FileNotFoundError:
        print("\n[ERROR] yamllint not found!")
        print("Install it with: pip install -r requirements.txt")
        return False


# ============================================================================
# Blueprint Validation
# ============================================================================

class ValidationError:
    def __init__(self, file: str, message: str, line: Optional[int] = None):
        self.file = file
        self.message = message
        self.line = line

    def __str__(self):
        location = f":{self.line}" if self.line else ""
        return f"{self.file}{location}: {self.message}"


class BlueprintValidator:
    REQUIRED_BLUEPRINT_KEYS = ['blueprint', 'trigger', 'action']
    REQUIRED_BLUEPRINT_META = ['name', 'description', 'domain']
    VALID_DOMAINS = ['automation', 'script']

    def __init__(self):
        self.errors: List[ValidationError] = []
        self.warnings: List[ValidationError] = []

    def add_error(self, file: str, message: str, line: Optional[int] = None):
        """Add an error to the error list"""
        self.errors.append(ValidationError(file, message, line))

    def add_warning(self, file: str, message: str, line: Optional[int] = None):
        """Add a warning to the warning list"""
        self.warnings.append(ValidationError(file, message, line))

    def validate_all(self) -> bool:
        """Validate all blueprints in the blueprints directory"""
        print("\n" + "=" * 60)
        print("Validating Home Assistant Blueprints")
        print("=" * 60 + "\n")

        blueprints_dir = Path(__file__).parent.parent / 'blueprints'

        if not blueprints_dir.exists():
            self.add_error('blueprints/', 'Blueprints directory not found')
            return False

        files = list(blueprints_dir.glob('*.yaml')) + list(blueprints_dir.glob('*.yml'))

        if not files:
            print("[WARN] No blueprint files found in blueprints/\n")
            return True

        print(f"Found {len(files)} blueprint file(s)\n")

        for file in files:
            self.validate_blueprint(file)

        return self.print_results()

    def validate_blueprint(self, file_path: Path):
        """Validate a single blueprint file"""
        rel_path = file_path.relative_to(Path.cwd())
        print(f"Validating: {rel_path}")

        # Step 1: Read and parse YAML
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                blueprint = yaml.safe_load(content)
        except yaml.YAMLError as e:
            line = getattr(e, 'problem_mark', None)
            line_num = line.line + 1 if line else None
            self.add_error(str(rel_path), f"YAML syntax error: {e}", line_num)
            return
        except Exception as e:
            self.add_error(str(rel_path), f"Failed to read or parse file: {e}")
            return

        # Step 2: Validate blueprint structure
        self.validate_structure(str(rel_path), blueprint)

        # Step 3: Validate blueprint metadata
        if blueprint and 'blueprint' in blueprint:
            self.validate_metadata(str(rel_path), blueprint['blueprint'])

        # Step 4: Validate inputs
        if blueprint and 'blueprint' in blueprint and 'input' in blueprint['blueprint']:
            self.validate_inputs(str(rel_path), blueprint['blueprint']['input'])

        # Step 5: Validate triggers
        if blueprint and 'trigger' in blueprint:
            self.validate_triggers(str(rel_path), blueprint['trigger'])

        # Step 6: Validate actions
        if blueprint and 'action' in blueprint:
            self.validate_actions(str(rel_path), blueprint['action'])

        # Step 7: Check for common mistakes
        self.check_common_mistakes(str(rel_path), blueprint, content)

    def validate_structure(self, file: str, blueprint: Any):
        """Validate blueprint has required top-level keys"""
        if not blueprint or not isinstance(blueprint, dict):
            self.add_error(file, 'Blueprint must be a valid YAML object')
            return

        for key in self.REQUIRED_BLUEPRINT_KEYS:
            if key not in blueprint:
                self.add_error(file, f"Missing required top-level key: '{key}'")

    def validate_metadata(self, file: str, meta: Dict[str, Any]):
        """Validate blueprint metadata"""
        for key in self.REQUIRED_BLUEPRINT_META:
            if key not in meta:
                self.add_error(file, f"Missing required blueprint metadata: '{key}'")

        # Validate domain
        if 'domain' in meta and meta['domain'] not in self.VALID_DOMAINS:
            self.add_error(
                file,
                f"Invalid domain: '{meta['domain']}'. Must be one of: {', '.join(self.VALID_DOMAINS)}"
            )

        # Check description length
        if 'description' in meta and isinstance(meta['description'], str) and len(meta['description']) < 10:
            self.add_warning(file, 'Blueprint description is very short (< 10 characters)')

    def validate_inputs(self, file: str, inputs: Any):
        """Validate inputs"""
        if not isinstance(inputs, dict):
            self.add_error(file, 'Blueprint inputs must be an object')
            return

        reserved_keywords = ['blueprint', 'trigger', 'condition', 'action']

        for input_name, input_def in inputs.items():
            # Check for required input properties
            if not isinstance(input_def, dict):
                continue

            if 'name' not in input_def:
                self.add_warning(file, f"Input '{input_name}' missing 'name' property")

            if 'selector' not in input_def:
                self.add_warning(file, f"Input '{input_name}' missing 'selector' property")

            # Check for invalid input names (reserved keywords)
            if input_name in reserved_keywords:
                self.add_error(file, f"Input name '{input_name}' is a reserved keyword")

    def validate_triggers(self, file: str, triggers: Any):
        """Validate triggers"""
        if not isinstance(triggers, list):
            self.add_error(file, 'Triggers must be an array')
            return

        if len(triggers) == 0:
            self.add_warning(file, 'No triggers defined')
            return

        for trigger in triggers:
            if isinstance(trigger, dict) and 'platform' not in trigger:
                self.add_error(file, 'Trigger missing required "platform" key')

    def validate_actions(self, file: str, actions: Any):
        """Validate actions"""
        if not isinstance(actions, list):
            self.add_error(file, 'Actions must be an array')
            return

        if len(actions) == 0:
            self.add_warning(file, 'No actions defined')

    def check_common_mistakes(self, file: str, blueprint: Any, content: str):
        """Check for common mistakes"""
        # Check for tabs (should use spaces)
        if '\t' in content:
            self.add_warning(file, 'File contains tabs. YAML should use spaces for indentation')

        lines = content.split('\n')

        for i, line in enumerate(lines):
            line_num = i + 1

            # Check for common choose/default indentation issue
            if line.strip().startswith('default:'):
                default_indent = len(line) - len(line.lstrip())

                # Look backwards for the matching choose
                for j in range(i - 1, max(0, i - 50), -1):
                    prev_line = lines[j]
                    if '- choose:' in prev_line.strip() or prev_line.strip() == 'choose:':
                        choose_indent = len(prev_line) - len(prev_line.lstrip())
                        expected_default_indent = choose_indent if prev_line.strip().startswith('-') else choose_indent + 2

                        if default_indent != expected_default_indent:
                            self.add_warning(
                                file,
                                f"Possible indentation issue: 'default' at column {default_indent} may be misaligned with 'choose' at column {choose_indent}",
                                line_num
                            )
                        break

            # Check for common template mistakes (skip if line starts with block scalar indicators)
            if '{{' in line and '}}' not in line:
                # Skip if this is a multiline template (block scalar)
                stripped = line.strip()
                if not any(stripped.endswith(c) for c in ['>', '|', '>-', '|-', '>+', '|+']):
                    self.add_warning(file, 'Possible unclosed template expression', line_num)

            # Check for !input usage in wrong places
            if '  - condition: !input' in line:
                self.add_warning(file, 'Possible incorrect !input usage in condition list', line_num)

        # Check mode is set (recommended for automations)
        if blueprint and isinstance(blueprint, dict):
            if blueprint.get('blueprint', {}).get('domain') == 'automation':
                if 'mode' not in blueprint:
                    self.add_warning(file, 'Consider setting "mode" for automation (e.g., restart, single, parallel)')

            # Check for default values in inputs
            if 'blueprint' in blueprint and 'input' in blueprint['blueprint']:
                inputs_without_defaults = [
                    name for name, def_ in blueprint['blueprint']['input'].items()
                    if isinstance(def_, dict) and 'default' not in def_
                ]

                if inputs_without_defaults:
                    preview = ', '.join(inputs_without_defaults[:3])
                    if len(inputs_without_defaults) > 3:
                        preview += '...'
                    self.add_warning(
                        file,
                        f"{len(inputs_without_defaults)} input(s) without default values: {preview}"
                    )

    def print_results(self) -> bool:
        """Print validation results"""
        print('\n' + '=' * 60)

        if self.warnings:
            print('\n[WARNINGS]\n')
            for warning in self.warnings:
                print(f"  {warning}")

        if self.errors:
            print('\n[ERRORS]\n')
            for error in self.errors:
                print(f"  {error}")

        print('\n' + '=' * 60)

        if not self.errors and not self.warnings:
            print('\n[PASS] All blueprints are valid!\n')
            return True
        else:
            print(f'\nResults: {len(self.errors)} error(s), {len(self.warnings)} warning(s)\n')
            return len(self.errors) == 0


# ============================================================================
# Main CLI Interface
# ============================================================================

def show_help():
    """Show help message"""
    print(__doc__)
    print("Available commands:")
    print("  python validate.py              - Run all validations (default)")
    print("  python validate.py lint         - Run only YAML linting")
    print("  python validate.py validate     - Run only blueprint validation")
    print("  python validate.py help         - Show this help message")
    print()


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "all"

    if command in ["help", "-h", "--help"]:
        show_help()
        sys.exit(0)

    success = True

    if command in ["all", "lint"]:
        if not run_yamllint():
            success = False

    if command in ["all", "validate"]:
        validator = BlueprintValidator()
        if not validator.validate_all():
            success = False

    if command not in ["all", "lint", "validate"]:
        print(f"[ERROR] Unknown command: {command}")
        print("Run 'python validate.py help' for usage information.\n")
        sys.exit(1)

    if command == "all":
        print("\n" + "=" * 60)
        if success:
            print("[PASS] All validations passed!")
        else:
            print("[FAIL] Some validations failed. See above for details.")
        print("=" * 60 + "\n")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
