# Venezuela Currency Calculator

Currency calculator with auto-updated BCV exchange rates.

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

### System Requirements

The icon generation script requires the Cairo graphics library:

```bash
brew install cairo
```

**macOS Setup:** You need to set the library path so Python can find Cairo:

```bash
# For Apple Silicon (M1/M2/M3):
export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib

# For Intel Macs:
export DYLD_FALLBACK_LIBRARY_PATH=/usr/local/lib
```

Add this to your `~/.zshrc` or `~/.bashrc` to make it permanent.

### Generating iOS PWA Icons

To generate PNG icons for iOS from the SVG source:

```bash
uv run generate_ios_icons.py
```

This will create PNG files in `icons/` for all iOS/iPadOS icon sizes:
- 40, 58, 60, 76, 80, 87, 114, 120, 128, 136, 152, 167, 180, 192, 1024

Including icons for iPhone, iPad, iPad Pro, Apple Watch, App Store, and Android Chrome.
