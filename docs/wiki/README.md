# Wiki Source

This directory contains the **source markdown** for the Zeref OS GitHub Wiki.

## How to publish to GitHub Wiki

GitHub Wikis are a separate repo: `https://github.com/<owner>/<repo>.wiki.git`. To publish:

### 1. Enable Wikis on GitHub

Go to: `https://github.com/kanadhiayash/zeref-os/settings` → **Features** → check **Wikis**.

### 2. Create the first page via the web UI

GitHub creates the wiki repo only after the first page exists. Click **Wiki** tab on the repo → **Create the first page** → save (any content; will be overwritten).

### 3. Clone + push wiki content

```bash
git clone https://github.com/kanadhiayash/zeref-os.wiki.git /tmp/zeref-os.wiki
cp docs/wiki/*.md /tmp/zeref-os.wiki/
cd /tmp/zeref-os.wiki
git add .
git commit -m "Initial wiki — Zeref OS v1.0.0"
git push
```

### 4. Set the sidebar

`_Sidebar.md` here becomes the wiki's left sidebar. Already included.

## Pages

| File | URL slug |
|---|---|
| `Home.md` | `Home` (landing page) |
| `Installation.md` | `Installation` |
| `Architecture.md` | `Architecture` |
| `Memory-Model.md` | `Memory-Model` |
| `Privacy-Model.md` | `Privacy-Model` |
| `Team-Packs.md` | `Team-Packs` |
| `Pattern-Detection.md` | `Pattern-Detection` |
| `Decision-Log.md` | `Decision-Log` |
| `Model-Debates.md` | `Model-Debates` |
| `Versioning-History.md` | `Versioning-History` |
| `FAQ.md` | `FAQ` |
| `Glossary.md` | `Glossary` |
| `Inspirations.md` | `Inspirations` |
| `_Sidebar.md` | (sidebar — auto-rendered, no URL) |

13 content pages + 1 sidebar.

## Updating the wiki

After updates here on `main`:

```bash
cd /tmp/zeref-os.wiki
cp /path/to/zeref-os/docs/wiki/*.md .
git commit -am "Update wiki from main"
git push
```

Or set up a GitHub Action to sync automatically (not currently wired).
