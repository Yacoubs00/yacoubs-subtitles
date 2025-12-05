# Setup Instructions for GitHub Pages

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the **+** icon in the top right → **New repository**
3. Repository name: `yacoubs-subtitles-repo`
4. Description: `Kodi subtitle addon with multiple providers`
5. Make it **Public**
6. ✅ Check "Add a README file" (or you'll use the one here)
7. Click **Create repository**

## Step 2: Upload Files to GitHub

### Option A: Using Git Command Line

```bash
cd ~/projects/yacoubs-subtitles-repo

# Initialize git
git init
git add .
git commit -m "Initial commit - Yacoub's Subs v6.3.0"

# Add your GitHub repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/yacoubs-subtitles-repo.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Option B: Using GitHub Web Interface

1. Go to your repository on GitHub
2. Click **Add file** → **Upload files**
3. Drag and drop these files:
   - `index.html`
   - `README.md`
   - `addons.xml`
   - `addons.xml.md5`
   - `repository.yacoubs.subs-1.0.0.zip`
   - `service.subtitles.yacoubs-6.3.0.zip`
4. Also upload the folders:
   - `repository.yacoubs.subs/`
   - `service.subtitles.yacoubs/`
5. Commit the changes

## Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. Scroll down to **Pages** (left sidebar)
4. Under **Source**, select:
   - Branch: `main`
   - Folder: `/ (root)`
5. Click **Save**
6. Wait 1-2 minutes for deployment
7. Your site will be live at: `https://YOUR_USERNAME.github.io/yacoubs-subtitles-repo/`

## Step 4: Update URLs in Files

After creating the repository, update these files with your actual GitHub username:

### 1. Update `index.html`
Replace all instances of `YOUR_USERNAME` with your GitHub username:
- Line with repository download link
- Line with direct install link
- Links in support section

### 2. Update `README.md`
Replace `YOUR_USERNAME` with your GitHub username in:
- Installation links
- Support/issues link

### 3. Update `repository.yacoubs.subs/addon.xml`
Replace `YOUR_USERNAME` in the URLs:
```xml
<info compressed="false">https://raw.githubusercontent.com/YOUR_USERNAME/yacoubs-subtitles-repo/main/addons.xml</info>
<checksum>https://raw.githubusercontent.com/YOUR_USERNAME/yacoubs-subtitles-repo/main/addons.xml.md5</checksum>
<datadir zip="true">https://raw.githubusercontent.com/YOUR_USERNAME/yacoubs-subtitles-repo/main/</datadir>
```

### 4. Re-create the repository zip after updating
```bash
cd ~/projects/yacoubs-subtitles-repo
rm repository.yacoubs.subs-1.0.0.zip
zip -r repository.yacoubs.subs-1.0.0.zip repository.yacoubs.subs/
```

### 5. Update addons.xml
Replace `YOUR_USERNAME` in the addon metadata

### 6. Regenerate MD5
```bash
cd ~/projects/yacoubs-subtitles-repo
md5sum addons.xml > addons.xml.md5
```

## Step 5: Push Updates

```bash
git add .
git commit -m "Update URLs with actual GitHub username"
git push
```

## Step 6: Test Installation

1. Visit your GitHub Pages URL: `https://YOUR_USERNAME.github.io/yacoubs-subtitles-repo/`
2. Download the repository zip from the website
3. Install in Kodi to verify it works

## File Structure

```
yacoubs-subtitles-repo/
├── index.html                          # GitHub Pages website
├── README.md                           # Repository documentation
├── addons.xml                          # Kodi addon index
├── addons.xml.md5                      # MD5 checksum
├── repository.yacoubs.subs-1.0.0.zip   # Repository installer
├── service.subtitles.yacoubs-6.3.0.zip # Addon installer
├── repository.yacoubs.subs/            # Repository source
│   ├── addon.xml
│   ├── icon.png
│   └── fanart.jpg
└── service.subtitles.yacoubs/          # Addon source
    ├── addon.xml
    ├── main.py
    └── ... (all addon files)
```

## Updating the Addon

When you release a new version:

1. Update the addon in `service.subtitles.yacoubs/`
2. Create new zip: `service.subtitles.yacoubs-X.X.X.zip`
3. Update `addons.xml` with new version number
4. Regenerate MD5: `md5sum addons.xml > addons.xml.md5`
5. Update `index.html` with new version and download links
6. Commit and push to GitHub
7. Users with the repository installed will auto-update!

## Notes

- The repository zip allows users to get automatic updates
- Direct install zip is for one-time installation
- GitHub Pages is free for public repositories
- Your addon will be accessible at: `https://YOUR_USERNAME.github.io/yacoubs-subtitles-repo/`

## Example Repository

See [a4k-openproject.github.io](https://a4k-openproject.github.io/) for a similar setup.
