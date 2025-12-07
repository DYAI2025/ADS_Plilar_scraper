# Claude Code - Repository Zugriffsproblem / Repository Access Issue

## 🇩🇪 Problem (Deutsch)

**Symptom:** Bei der Verwendung von Claude Code können Sie nur dieses Repository auswählen, während alle anderen Repositories ausgegraut bleiben.

### Ursache

Das Problem liegt an der **OAuth Token Berechtigung** für die Claude Code GitHub Action. Der `CLAUDE_CODE_OAUTH_TOKEN` hat nur Zugriff auf dieses spezifische Repository erhalten.

## Lösung - Repository Zugriff erweitern

### Option 1: GitHub App Installation erweitern (Empfohlen)

1. **Gehen Sie zu GitHub Settings:**
   - Öffnen Sie: https://github.com/settings/installations
   - Oder: GitHub Profil → Settings → Applications → Installed GitHub Apps

2. **Finden Sie "Claude for GitHub":**
   - Klicken Sie auf "Configure" neben der Claude-App

3. **Repository Access erweitern:**
   - Unter "Repository access" sehen Sie die aktuelle Konfiguration
   - Wählen Sie eine der Optionen:
     - **"All repositories"** - Claude hat Zugriff auf alle Ihre Repos (jetzt und in Zukunft)
     - **"Only select repositories"** - Fügen Sie weitere Repos zur Liste hinzu

4. **Speichern:**
   - Klicken Sie auf "Save"
   - Die Änderungen werden sofort wirksam

### Option 2: Neuen OAuth Token generieren

Falls Option 1 nicht funktioniert, müssen Sie möglicherweise den OAuth Token neu generieren:

1. **Alten Token widerrufen:**
   - Gehen Sie zu: https://github.com/settings/apps/authorizations
   - Widerrufen Sie die Berechtigung für Claude Code

2. **Neu authentifizieren:**
   - Gehen Sie zu Ihrem anderen Repository
   - Erstellen Sie einen Issue oder PR
   - Taggen Sie `@claude` im Kommentar
   - Folgen Sie dem OAuth Flow mit erweiterten Berechtigungen

3. **Token im Repository aktualisieren:**
   - Für jedes Repository: Settings → Secrets and variables → Actions
   - Update den `CLAUDE_CODE_OAUTH_TOKEN` Secret

## Überprüfung

Nach der Änderung:

1. **Testen Sie Claude in einem anderen Repository:**
   - Erstellen Sie einen Issue
   - Kommentieren Sie mit `@claude` und einer Aufgabe
   - Claude sollte nun antworten können

2. **Prüfen Sie die Workflow-Logs:**
   - Gehen Sie zu Actions tab
   - Schauen Sie nach fehlgeschlagenen Claude Workflows
   - Authentifizierungsfehler sollten verschwunden sein

---

## 🇬🇧 Problem (English)

**Symptom:** When using Claude Code, you can only select this repository while all other repositories remain greyed out.

### Cause

The issue is related to the **OAuth token permissions** for the Claude Code GitHub Action. The `CLAUDE_CODE_OAUTH_TOKEN` has only been granted access to this specific repository.

## Solution - Expand Repository Access

### Option 1: Expand GitHub App Installation (Recommended)

1. **Go to GitHub Settings:**
   - Open: https://github.com/settings/installations
   - Or: GitHub Profile → Settings → Applications → Installed GitHub Apps

2. **Find "Claude for GitHub":**
   - Click "Configure" next to the Claude app

3. **Expand Repository Access:**
   - Under "Repository access" you'll see the current configuration
   - Choose one of the options:
     - **"All repositories"** - Claude has access to all your repos (now and future)
     - **"Only select repositories"** - Add more repos to the list

4. **Save:**
   - Click "Save"
   - Changes take effect immediately

### Option 2: Generate New OAuth Token

If Option 1 doesn't work, you may need to regenerate the OAuth token:

1. **Revoke old token:**
   - Go to: https://github.com/settings/apps/authorizations
   - Revoke the authorization for Claude Code

2. **Re-authenticate:**
   - Go to your other repository
   - Create an issue or PR
   - Tag `@claude` in a comment
   - Follow the OAuth flow with expanded permissions

3. **Update token in repositories:**
   - For each repository: Settings → Secrets and variables → Actions
   - Update the `CLAUDE_CODE_OAUTH_TOKEN` secret

## Verification

After making changes:

1. **Test Claude in another repository:**
   - Create an issue
   - Comment with `@claude` and a task
   - Claude should now be able to respond

2. **Check workflow logs:**
   - Go to Actions tab
   - Look for failed Claude workflows
   - Authentication errors should be gone

---

## Technische Details / Technical Details

### Workflow Configuration

This repository uses Claude Code via GitHub Actions:

```yaml
# .github/workflows/claude.yml
uses: anthropics/claude-code-action@v1
with:
  claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

### Required Permissions

Claude Code requires these GitHub permissions:
- `contents: read` - Read repository content
- `pull-requests: read` - Read PR information
- `issues: read` - Read issue information
- `id-token: write` - Generate OIDC tokens
- `actions: read` - Read CI results

### Common Errors

**Error:** "Resource not accessible by integration"
- **Cause:** OAuth token doesn't have access to the repository
- **Solution:** Follow Option 1 above

**Error:** "Bad credentials"
- **Cause:** Token is invalid or revoked
- **Solution:** Follow Option 2 above

**Error:** "Not Found"
- **Cause:** Repository doesn't exist or token has no access
- **Solution:** Check repository name and token permissions

## Weitere Hilfe / Further Help

- [Claude Code GitHub Action Documentation](https://github.com/anthropics/claude-code-action)
- [GitHub Apps Documentation](https://docs.github.com/en/apps)
- [OAuth Troubleshooting](https://docs.github.com/en/apps/oauth-apps/maintaining-oauth-apps/troubleshooting-authorization-request-errors)

## Support

Bei weiteren Fragen / For further questions:
- Öffnen Sie einen Issue in diesem Repository / Open an issue in this repository
- Konsultieren Sie die [CLAUDE.md](../CLAUDE.md) für technische Details / Consult CLAUDE.md for technical details
