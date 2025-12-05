<picture align="center">
  <img src="icon.png" alt="Yacoub's Subs Logo" width="300"/>
</picture>

# Yacoub's Subs - Kodi Subtitle Addon

A comprehensive subtitle addon for Kodi with support for multiple providers and languages.

## Features

- 🎬 **Multiple Providers**: OpenSubtitles, SubDL, SubSource, YIFY, Podnapisi, and more
- 📺 **Content Types**: Movies, TV Shows, and Anime support
- ⚡ **Fast & Reliable**: Optimized search and download
- 🔧 **User Configurable**: API credentials required

## Installation

### Method 1: Add Source as File Manager Source

1. In Kodi, go to **Settings → File Manager → Add source**
2. Click **< None >**
3. Enter path: `https://yacoubs00.github.io/`
4. Name it: `Yacoub's Repo`
5. Click **OK**
6. Go to **Settings → Add-ons → Install from zip file**
7. Select **Yacoub's Repo** source
8. Install **repository.yacoubs-1.0.0.zip**
9. Then install the addon from the repository

### Method 3: Direct Addon Install

1. Download from GitHub Releases: [Latest Release](https://github.com/Yacoubs00/yacoubs-subtitles/releases/latest)
2. In Kodi, go to **Settings → Add-ons → Install from zip file**
3. Select the downloaded **service.subtitles.yacoubs-1.1.0.zip** file

## Configuration

### Basic Setup

After installation:
1. Go to **Settings → Subtitles**
2. Enable **Yacoub's Subs**
3. (Optional) Set it as default subtitle service

### Provider Configuration

Some providers require API credentials for full functionality:

#### OpenSubtitles (Recommended)
1. Create free account at [OpenSubtitles.com](https://www.opensubtitles.com/)
2. Go to **Add-on Settings → Accounts**
3. Enter your OpenSubtitles username and password

#### SubDL (Recommended)
- Configure API key in Add-on Settings if you have one
- Works without API key with rate limits

#### SubSource (Recommended)
- Configure API key in Add-on Settings if you have one
- Works without API key with rate limits

> 💡 **Tip**: Other providers (YIFY, Podnapisi, Kitsunekko, Witanime) work without configuration!

## Providers Status

| Provider | Languages | Content Type | API Required | Status |
|----------|-----------|--------------|--------------|--------|
| OpenSubtitles | 40+ languages | Movies, TV, Anime | Yes | ✅ Working |
| SubDL | Multi-language | Movies, TV | Yes | ✅ Working |
| SubSource | Multi-language | Movies, TV | Yes | ✅ Working |
| YIFY | English | Movies | No | ✅ Working |
| Podnapisi | Multi-language | Movies, TV | No | Partial |


## Usage

1. **Play a video** in Kodi
2. Click the **Subtitles button** (speech bubble icon)
3. Select **Yacoub's Subs**
4. Choose your preferred subtitle from the results
5. Enjoy your content!

## Version History

- **v1.1.0** (Current) - Enhanced stability and provider improvements
- **v1.0.0** - Initial public release


## Credits

This addon is based on [a4kSubtitles](https://github.com/a4k-openproject/a4kSubtitles) by a4k-openproject.

**Author**: Yacoub00

## License

MIT License - See the original a4kSubtitles project for full license details.
