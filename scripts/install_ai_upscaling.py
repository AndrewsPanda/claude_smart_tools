#!/usr/bin/env python3
"""Installation script for AI upscaling dependencies."""

import subprocess


def run_command(command: str) -> bool:
    """Run a command and return success status."""
    try:
        subprocess.run(command.split(), check=True, capture_output=True, text=True)
        print(f"✓ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {command}")
        print(f"Error: {e.stderr}")
        return False


def install_ai_upscaling_deps():
    """Install AI upscaling dependencies."""
    print("Installing AI upscaling dependencies...")
    print("This will download approximately 500MB of packages and models.")

    # Check if user wants to continue
    response = input("Continue? (y/N): ").lower()
    if response not in ["y", "yes"]:
        print("Installation canceled.")
        return False

    # Required packages for Real-ESRGAN
    packages = [
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "basicsr>=1.4.2",
        "realesrgan>=0.3.0",
    ]

    success = True
    for package in packages:
        print(f"\nInstalling {package}...")
        if not run_command(f"pip install {package}"):
            success = False
            print(f"Failed to install {package}")

    if success:
        print("\n✓ All AI upscaling dependencies installed successfully!")
        print("The image upscaler will now use Real-ESRGAN for maximum quality.")
    else:
        print("\n✗ Some dependencies failed to install.")
        print("The image upscaler will fall back to classical methods.")

    return success


if __name__ == "__main__":
    install_ai_upscaling_deps()
