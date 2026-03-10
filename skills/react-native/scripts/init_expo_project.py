#!/usr/bin/env python3
"""
Initialize a new Expo React Native project with common configurations.

Usage:
    init_expo_project.py <project-name> [--template <template>] [--typescript]

Examples:
    init_expo_project.py MyApp
    init_expo_project.py MyApp --template navigation
    init_expo_project.py MyApp --typescript
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(cmd, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr


def init_expo_project(project_name, template=None, use_typescript=False):
    """
    Initialize a new Expo project.
    
    Args:
        project_name: Name of the project
        template: Template to use (blank, navigation, tabs, etc.)
        use_typescript: Whether to use TypeScript template
    """
    print(f"🚀 Initializing Expo project: {project_name}")
    
    # Determine template
    if template:
        template_arg = f"--template {template}"
    elif use_typescript:
        template_arg = "--template blank-typescript"
    else:
        template_arg = "--template blank"
    
    # Create Expo project
    cmd = f"npx create-expo-app@latest {project_name} {template_arg}"
    print(f"Running: {cmd}")
    
    success, stdout, stderr = run_command(cmd)
    
    if not success:
        print(f"❌ Error creating Expo project:")
        print(stderr)
        return False
    
    print(f"✅ Project created successfully")
    print(f"\nNext steps:")
    print(f"  cd {project_name}")
    print(f"  npx expo start")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new Expo React Native project"
    )
    parser.add_argument(
        "project_name",
        help="Name of the project to create"
    )
    parser.add_argument(
        "--template",
        help="Template to use (blank, navigation, tabs, etc.)",
        default=None
    )
    parser.add_argument(
        "--typescript",
        action="store_true",
        help="Use TypeScript template"
    )
    
    args = parser.parse_args()
    
    if not args.project_name:
        print("❌ Error: Project name is required")
        sys.exit(1)
    
    success = init_expo_project(
        args.project_name,
        args.template,
        args.typescript
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
