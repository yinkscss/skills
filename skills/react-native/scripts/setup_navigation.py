#!/usr/bin/env python3
"""
Set up React Navigation in an Expo project.

Usage:
    setup_navigation.py [--type <type>] [--path <path>]

Examples:
    setup_navigation.py
    setup_navigation.py --type tabs
    setup_navigation.py --type drawer --path ./MyApp
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(cmd, cwd=None, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=check,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr


def install_packages(project_path, nav_type="stack"):
    """Install React Navigation packages."""
    print("📦 Installing React Navigation packages...")
    
    # Base packages
    base_packages = [
        "@react-navigation/native",
        "react-native-screens",
        "react-native-safe-area-context"
    ]
    
    # Type-specific packages
    type_packages = {
        "stack": ["@react-navigation/native-stack"],
        "tabs": ["@react-navigation/bottom-tabs"],
        "drawer": ["@react-navigation/drawer", "react-native-gesture-handler", "react-native-reanimated"]
    }
    
    packages = base_packages + type_packages.get(nav_type, type_packages["stack"])
    
    # Install with expo install for Expo-compatible versions
    for package in packages:
        if package.startswith("@react-navigation") or package in ["react-native-screens", "react-native-safe-area-context"]:
            cmd = f"npx expo install {package}"
        else:
            cmd = f"npm install {package}"
        
        print(f"  Installing {package}...")
        success, stdout, stderr = run_command(cmd, cwd=project_path)
        
        if not success:
            print(f"❌ Error installing {package}:")
            print(stderr)
            return False
    
    print("✅ All packages installed successfully")
    return True


def create_navigation_setup(project_path, nav_type="stack"):
    """Create navigation setup files."""
    print(f"📝 Creating {nav_type} navigation setup...")
    
    # Create navigation directory
    nav_dir = Path(project_path) / "navigation"
    nav_dir.mkdir(exist_ok=True)
    
    # Create navigation file based on type
    if nav_type == "stack":
        content = '''import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { HomeScreen } from '../screens/HomeScreen';

const Stack = createNativeStackNavigator();

export function Navigation() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
'''
    elif nav_type == "tabs":
        content = '''import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { HomeScreen } from '../screens/HomeScreen';

const Tab = createBottomTabNavigator();

export function Navigation() {
  return (
    <NavigationContainer>
      <Tab.Navigator>
        <Tab.Screen name="Home" component={HomeScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
'''
    else:  # drawer
        content = '''import { NavigationContainer } from '@react-navigation/native';
import { createDrawerNavigator } from '@react-navigation/drawer';
import { HomeScreen } from '../screens/HomeScreen';

const Drawer = createDrawerNavigator();

export function Navigation() {
  return (
    <NavigationContainer>
      <Drawer.Navigator>
        <Drawer.Screen name="Home" component={HomeScreen} />
      </Drawer.Navigator>
    </NavigationContainer>
  );
}
'''
    
    nav_file = nav_dir / "index.tsx"
    nav_file.write_text(content)
    print(f"✅ Created {nav_file}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Set up React Navigation in an Expo project"
    )
    parser.add_argument(
        "--type",
        choices=["stack", "tabs", "drawer"],
        default="stack",
        help="Navigation type to set up (default: stack)"
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Path to Expo project (default: current directory)"
    )
    
    args = parser.parse_args()
    
    project_path = Path(args.path).resolve()
    
    if not (project_path / "package.json").exists():
        print("❌ Error: Not an Expo project (package.json not found)")
        sys.exit(1)
    
    print(f"📱 Setting up {args.type} navigation in {project_path}")
    
    # Install packages
    if not install_packages(project_path, args.type):
        sys.exit(1)
    
    # Create navigation setup
    if not create_navigation_setup(project_path, args.type):
        sys.exit(1)
    
    print("\n✅ Navigation setup complete!")
    print(f"\nNext steps:")
    print(f"  1. Import Navigation in your App.tsx")
    print(f"  2. Add screens to the navigator")
    print(f"  3. See references/navigation.md for detailed patterns")


if __name__ == "__main__":
    main()
