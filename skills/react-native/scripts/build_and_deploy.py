#!/usr/bin/env python3
"""
Helper script for EAS Build and deployment workflows.

Usage:
    build_and_deploy.py [--platform <platform>] [--profile <profile>] [--submit]

Examples:
    build_and_deploy.py --platform ios
    build_and_deploy.py --platform android --profile production
    build_and_deploy.py --platform all --submit
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


def check_eas_cli():
    """Check if EAS CLI is installed."""
    success, _, _ = run_command("eas --version", check=False)
    return success


def configure_eas():
    """Configure EAS Build if not already configured."""
    eas_json = Path("eas.json")
    
    if eas_json.exists():
        print("✅ EAS already configured")
        return True
    
    print("📝 Configuring EAS Build...")
    success, stdout, stderr = run_command("eas build:configure")
    
    if not success:
        print(f"❌ Error configuring EAS:")
        print(stderr)
        return False
    
    print("✅ EAS configured successfully")
    return True


def build_app(platform, profile=None):
    """
    Build the app using EAS Build.
    
    Args:
        platform: Platform to build for (ios, android, all)
        profile: Build profile to use
    """
    print(f"🔨 Building for {platform}...")
    
    cmd = f"eas build --platform {platform}"
    if profile:
        cmd += f" --profile {profile}"
    
    success, stdout, stderr = run_command(cmd)
    
    if not success:
        print(f"❌ Build failed:")
        print(stderr)
        return False
    
    print("✅ Build started successfully")
    print("Check build status at: https://expo.dev")
    return True


def submit_app(platform):
    """
    Submit the app to app stores.
    
    Args:
        platform: Platform to submit for (ios, android)
    """
    print(f"📤 Submitting {platform} app to app store...")
    
    success, stdout, stderr = run_command(f"eas submit --platform {platform}")
    
    if not success:
        print(f"❌ Submission failed:")
        print(stderr)
        return False
    
    print("✅ Submission started successfully")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Helper for EAS Build and deployment"
    )
    parser.add_argument(
        "--platform",
        choices=["ios", "android", "all"],
        default="all",
        help="Platform to build for (default: all)"
    )
    parser.add_argument(
        "--profile",
        help="Build profile to use (from eas.json)"
    )
    parser.add_argument(
        "--submit",
        action="store_true",
        help="Submit to app store after build"
    )
    parser.add_argument(
        "--configure",
        action="store_true",
        help="Configure EAS Build if not already configured"
    )
    
    args = parser.parse_args()
    
    # Check if EAS CLI is installed
    if not check_eas_cli():
        print("❌ Error: EAS CLI not found")
        print("Install with: npm install -g eas-cli")
        sys.exit(1)
    
    # Configure if requested
    if args.configure:
        if not configure_eas():
            sys.exit(1)
    
    # Build
    if not build_app(args.platform, args.profile):
        sys.exit(1)
    
    # Submit if requested
    if args.submit:
        if args.platform == "all":
            print("⚠️  Cannot submit 'all' platforms. Specify ios or android.")
        else:
            if not submit_app(args.platform):
                sys.exit(1)
    
    print("\n✅ Complete!")
    print("\nFor more details, see references/deployment.md")


if __name__ == "__main__":
    main()
