#!/bin/bash

set -e

echo "Installing fnm..."
brew install fnm

echo "Configuring zsh..."

if ! grep -q 'fnm env --use-on-cd' ~/.zshrc 2>/dev/null; then
cat <<'EOF' >> ~/.zshrc

# fnm (Fast Node Manager)
eval "$(fnm env --use-on-cd)"
EOF
fi

echo "Loading fnm for current session..."
eval "$(fnm env)"

echo "Installing latest LTS Node.js..."
fnm install --lts

echo "Setting LTS as default..."
fnm default lts-latest

echo ""
echo "Installation complete."
echo ""

node -v
npm -v

echo ""
echo "Restart your terminal or run:"
echo "source ~/.zshrc"