# Zeref OS — MCP Integration

**Version:** 2.0.0 | **Updated:** May 2026

---

## Overview

MCP (Model Context Protocol) connects Zeref OS to external tools and services. This transforms Claude from a text-only assistant into a workspace-aware operator that can read files, update project boards, search emails, and manage calendars.

**Connected tools unlock:**
- Reading Notion pages instead of requiring copy-paste
- Creating Linear tickets directly from Zeref outputs
- Pulling Google Drive documents into context
- Updating Figma designs via MCP
- Searching Gmail threads without leaving Claude

---

## Connector Priority

Install in this order — highest ROI first:

| Priority | Connector | Why |
|----------|-----------|-----|
| 1 | **Notion** | Primary knowledge base + project dashboard |
| 2 | **Google Drive** | Document storage, research access |
| 3 | **Linear** | Task and issue tracking |
| 4 | **Gmail** | Email context for decisions |
| 5 | **Google Calendar** | Scheduling and deadline awareness |
| 6 | **Figma** | Design file access |
| 7 | **Canva** | Brand asset creation |
| 8 | **GitHub** | Repo context and PR management |

---

## Setup: Claude Desktop App (Cowork)

### Step 1 — Open Connectors Panel
Claude Desktop → Left sidebar → **Connectors** (plug icon)

### Step 2 — Add Notion
1. Click **+ Add Connector**
2. Search: **Notion**
3. Click **Connect**
4. Authorize with your Notion account
5. Select workspace(s) to grant access
6. Click **Allow Access**

**Verify:**
```
What pages do I have in Notion?
```
Zeref should return your Notion page list.

### Step 3 — Add Google Drive
1. Click **+ Add Connector**
2. Search: **Google Drive**
3. Click **Connect** → Sign in with Google
4. Grant Drive read access
5. Done

**Verify:**
```
List my recent Google Drive files
```

### Step 4 — Add Linear
1. Click **+ Add Connector**
2. Search: **Linear**
3. Click **Connect** → Authorize with Linear account
4. Select workspace

**Verify:**
```
What issues are assigned to me in Linear?
```

### Step 5 — Add Gmail
1. Click **+ Add Connector**
2. Search: **Gmail**
3. Connect with Google (same account as Drive)
4. Grant mail read access

### Step 6 — Add Google Calendar
Same Google authorization as Gmail — usually connects automatically.

---

## Setup: Claude Code CLI

For Claude Code users, MCP servers are configured in `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_API_TOKEN": "your_notion_integration_token"
      }
    },
    "google-drive": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-drive"],
      "env": {
        "GOOGLE_CLIENT_ID": "your_client_id",
        "GOOGLE_CLIENT_SECRET": "your_client_secret"
      }
    },
    "linear": {
      "command": "npx",
      "args": ["-y", "@linear/mcp-server"],
      "env": {
        "LINEAR_API_KEY": "your_linear_api_key"
      }
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_pat"
      }
    },
    "figma": {
      "command": "npx",
      "args": ["-y", "@figma/mcp-server"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "your_figma_token"
      }
    }
  }
}
```

**Get API tokens:**
- Notion: Settings → Integrations → Create internal integration → Copy token
- Linear: Settings → API → Create new API key
- GitHub: Settings → Developer Settings → Personal Access Tokens → Generate
- Figma: Settings → Account → Personal Access Tokens → Create

---

## Notion Setup for Zeref Dashboard

The Notion connector is most powerful when your workspace is structured for Zeref.

### Recommended Notion Structure

```
Zeref OS Workspace/
  📋 Installation Hub        ← This guidebook in Notion
  🎯 Active Projects         ← Current work with status
  ⚡ Skills Fleet            ← Skill documentation
  🔌 MCP Integration Tracker ← Connector status
  🧠 Memory System           ← Long-term knowledge
  📚 Learning Path           ← Progress tracking
  📁 Template Library        ← Reusable templates
```

### Create the Dashboard
See [09_Notion_Dashboard.md](09_Notion_Dashboard.md) for full dashboard setup.

### Zeref + Notion in practice
```
"Create a Linear issue for the user research task I just described"
→ Zeref creates issue via Linear MCP

"Pull the brief from my Notion page 'Q2 Product Strategy'"
→ Zeref fetches page content via Notion MCP

"Add this decision to my Decision Log in Notion"
→ Zeref appends to the page via Notion MCP
```

---

## Figma Integration

Figma MCP enables Zeref to read design context directly.

### What you can do
- Get component specs without leaving Claude
- Read frame structure and layer hierarchy
- Extract design tokens and variables
- Comment on designs programmatically

### Setup
```bash
# In Claude Code settings.json (above)
# Or via Claude Desktop Connectors → Figma
```

**Usage example:**
```
"Read the current state of my mobile nav design in Figma"
→ Zeref pulls frame content, component list, and measurements
```

---

## GitHub Integration

GitHub MCP enables repo-aware operations.

### What you can do
- Read file contents without copy-paste
- Create branches and commits
- Open pull requests
- Search code across the repo
- Comment on PRs

### Permissions needed
```
Scopes: repo, read:user, user:email
```

**Usage example:**
```
"What changed in the last 3 commits?"
→ Zeref reads git log via GitHub MCP
```

---

## Canva Integration

Canva MCP enables brand asset creation.

### What you can do
- Create designs from templates
- Export designs in multiple formats
- Access brand kit

### Setup
Claude Desktop → Connectors → Canva → Authorize

**Usage example:**
```
"Create a LinkedIn banner using my brand colors"
→ Zeref generates via Canva MCP
```

---

## MCP Troubleshooting

### Connector not responding
```
"Test my Notion connection"
→ If Zeref can't list pages, reconnect the integration
```

### Permission errors
- Notion: Check integration has access to specific pages (share page with integration)
- GitHub: Verify scopes include `repo` not just `public_repo`
- Google: Ensure Drive API is enabled in Google Cloud Console

### Connector slow to respond
- Large Notion workspaces: Be specific — "fetch page [title]" not "search all pages"
- GitHub: Use specific file paths not broad searches

---

## What Zeref Will NOT Do Via MCP

Even with full connector access:
- ❌ Send emails without explicit confirmation
- ❌ Delete files, pages, or tickets
- ❌ Publish or post publicly
- ❌ Move money or execute purchases
- ❌ Invite users or change permissions

All write operations are proposed first — you approve before execution.

---

## Next Steps

- [05_Memory_System.md](05_Memory_System.md) — How memory + MCP work together
- [06_Workflow_Examples.md](06_Workflow_Examples.md) — MCP in real workflows
