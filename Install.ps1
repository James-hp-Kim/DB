[CmdletBinding()]
param(
    [ValidateSet('Skill','Plugin')][string]$Mode = 'Skill',
    [string]$PythonExe,
    [string]$SkillDestination,
    [switch]$EnableMcp
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'scripts/Resolve-Python.ps1')
$qaPython = Resolve-QaPython -Requested $PythonExe
$qaSkillSource = Join-Path $PSScriptRoot 'plugins/expert-hub/skills/expert'
& $qaPython -X utf8 (Join-Path $qaSkillSource 'scripts/expert.py') status
if ($LASTEXITCODE -ne 0) { throw 'Bundled knowledge database validation failed.' }

if ($Mode -eq 'Plugin') {
    if ($SkillDestination -or $EnableMcp) { throw 'Plugin mode already includes skill and MCP. Do not combine these options.' }
    if (-not (Get-Command codex -ErrorAction SilentlyContinue)) { throw 'Codex CLI is required for this installer mode. Use Skill mode or the documented desktop marketplace steps.' }
    # A portable plugin launches python from PATH on each computer, never a creator-machine path.
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Plugin mode requires a working python command on PATH. Add Python to PATH and reopen Codex.' }
    & python -X utf8 (Join-Path $PSScriptRoot 'scripts/probe_python.py')
    if ($LASTEXITCODE -ne 0) { throw 'python on PATH is not a supported interpreter.' }
    & codex plugin marketplace add $PSScriptRoot --json
    if ($LASTEXITCODE -ne 0) { throw 'Could not add the local marketplace.' }
    & codex plugin add 'expert-hub@expert-local' --json
    if ($LASTEXITCODE -ne 0) { throw 'Could not install the plugin.' }
    Write-Output 'Installed plugin expert-hub@expert-local. Start a new Codex chat and select $expert-hub:expert or $expert-hub:exam-setup.'
    return
}

if (-not $SkillDestination) {
    $qaUserProfile = [Environment]::GetFolderPath('UserProfile')
    $SkillDestination = Join-Path $qaUserProfile '.agents/skills/expert'
}
$qaDestination = [IO.Path]::GetFullPath($SkillDestination)
if (Test-Path -LiteralPath $qaDestination) {
    throw "Destination already exists; nothing was overwritten: $qaDestination. Use the existing install, or choose a new destination for review."
}
New-Item -ItemType Directory -Path (Split-Path -Parent $qaDestination) -Force | Out-Null
Copy-Item -LiteralPath $qaSkillSource -Destination $qaDestination -Recurse
& $qaPython -X utf8 (Join-Path $qaDestination 'scripts/expert.py') status
if ($LASTEXITCODE -ne 0) { throw 'Copied skill failed validation; inspect this destination before retrying.' }
if ($EnableMcp) {
    if (-not (Get-Command codex -ErrorAction SilentlyContinue)) { throw "Skill copied to $qaDestination. Codex CLI is required to register MCP; see the installation guide for manual configuration." }
    $qaMcpJson = & codex mcp list --json
    if ($LASTEXITCODE -ne 0) { throw 'Could not check existing MCP entries; the skill is installed but MCP was not changed.' }
    $qaMcpEntries = $qaMcpJson | ConvertFrom-Json
    if ($qaMcpEntries | Where-Object { $_.name -eq 'expert-knowledge' }) { throw 'An MCP server named expert-knowledge already exists; it was not overwritten. Review the existing entry first.' }
    & codex mcp add 'expert-knowledge' -- $qaPython -X utf8 (Join-Path $qaDestination 'scripts/mcp_server.py')
    if ($LASTEXITCODE -ne 0) { throw 'MCP registration failed; the standalone skill is still installed.' }
}
Write-Output "Skill installed at $qaDestination. Start a new Codex chat and run `$expert."
Write-Output 'If a custom test destination was used, it must be inside a configured skills location to be automatically discovered.'
