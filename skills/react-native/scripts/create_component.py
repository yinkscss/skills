#!/usr/bin/env python3
"""
Generate a React Native component template.

Usage:
    create_component.py <component-name> [--path <path>] [--type <type>]

Examples:
    create_component.py Button
    create_component.py UserCard --path ./src/components
    create_component.py Modal --type screen
"""

import sys
import argparse
from pathlib import Path


def create_component(component_name, output_path, component_type="component"):
    """
    Create a component file with template code.
    
    Args:
        component_name: Name of the component (PascalCase)
        output_path: Directory where component should be created
        component_type: Type of component (component or screen)
    """
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine file extension (check if TypeScript is used)
    use_ts = (Path(".") / "tsconfig.json").exists()
    ext = "tsx" if use_ts else "jsx"
    
    file_path = output_dir / f"{component_name}.{ext}"
    
    if file_path.exists():
        print(f"❌ Error: {file_path} already exists")
        return False
    
    # Generate component code
    if component_type == "screen":
        content = f'''import {{ View, Text, StyleSheet }} from 'react-native';

export function {component_name}() {{
  return (
    <View style={{styles.container}}>
      <Text style={{styles.title}}>{component_name}</Text>
    </View>
  );
}}

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
  }},
  title: {{
    fontSize: 24,
    fontWeight: 'bold',
  }},
}});
'''
    else:  # component
        if use_ts:
            content = f'''import {{ View, Text, StyleSheet }} from 'react-native';

interface {component_name}Props {{
  // Add props here
}}

export function {component_name}({{}}: {component_name}Props) {{
  return (
    <View style={{styles.container}}>
      <Text>{component_name}</Text>
    </View>
  );
}}

const styles = StyleSheet.create({{
  container: {{
    // Add styles here
  }},
}});
'''
        else:
            content = f'''import {{ View, Text, StyleSheet }} from 'react-native';

export function {component_name}() {{
  return (
    <View style={{styles.container}}>
      <Text>{component_name}</Text>
    </View>
  );
}}

const styles = StyleSheet.create({{
  container: {{
    // Add styles here
  }},
}});
'''
    
    file_path.write_text(content)
    print(f"✅ Created {file_path}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate a React Native component template"
    )
    parser.add_argument(
        "component_name",
        help="Name of the component (PascalCase)"
    )
    parser.add_argument(
        "--path",
        default="./components",
        help="Path where component should be created (default: ./components)"
    )
    parser.add_argument(
        "--type",
        choices=["component", "screen"],
        default="component",
        help="Type of component to create (default: component)"
    )
    
    args = parser.parse_args()
    
    if not args.component_name:
        print("❌ Error: Component name is required")
        sys.exit(1)
    
    # Validate component name (should be PascalCase)
    if not args.component_name[0].isupper():
        print(f"⚠️  Warning: Component name should be PascalCase (e.g., {args.component_name.capitalize()})")
    
    success = create_component(
        args.component_name,
        args.path,
        args.type
    )
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
