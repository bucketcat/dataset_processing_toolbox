#!/bin/bash

# Function to detect the package manager
detect_package_manager() {
    if command -v apt &> /dev/null; then
        echo "apt"  # Debian/Ubuntu
    elif command -v brew &> /dev/null; then
        echo "brew"  # macOS
    elif command -v pacman &> /dev/null; then
        echo "pacman"  # Arch
    elif command -v dnf &> /dev/null; then
        echo "dnf"  # Fedora
    else
        echo "unsupported"
    fi
}

# Install pipx based on the detected package manager
install_pipx() {
    local package_manager=$(detect_package_manager)
    
    case "$package_manager" in
        apt)
            sudo apt update
            sudo apt install pipx -y
            ;;
        brew)
            brew install pipx
            ;;
        pacman)
            sudo pacman -Syu --noconfirm pipx
            ;;
        dnf)
            sudo dnf install pipx -y
            ;;
        *)
            echo "Unsupported package manager. Please install pipx manually."
            exit 1
            ;;
    esac
}

# Install pipx
install_pipx

# Ensure pipx is in the PATH
pipx ensurepath

# Source the updated shell configuration to apply PATH changes in the same window
if [[ -f ~/.bashrc ]]; then
    source ~/.bashrc
elif [[ -f ~/.zshrc ]]; then
    source ~/.zshrc
elif [[ -f ~/.profile ]]; then
    source ~/.profile
else
    echo "Warning: No shell configuration file found. PATH changes may not take effect."
fi

# Notify the user
echo -e "\nInstallation complete! The PATH has been updated in this terminal window."
echo -e "You can now use pipx commands in this session."

# Optional: Verify the PATH update
echo -e "\nUpdated PATH: $PATH"

# Install huggingface-cli using pipx
pipx install huggingface-cli