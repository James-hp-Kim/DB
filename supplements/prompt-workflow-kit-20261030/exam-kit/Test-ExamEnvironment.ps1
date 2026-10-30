[CmdletBinding()]
param([switch]$RequireDatabase)
$ErrorActionPreference = 'Stop'
$examRoot = Split-Path -Parent $PSScriptRoot
$examRequired = @('.agents/skills/prompt-refine/SKILL.md', '.agents/skills/fact-grounding/SKILL.md', 'exam-kit/START.md')
$examMissing = @($examRequired | Where-Object { -not (Test-Path -LiteralPath (Join-Path $examRoot $_) -PathType Leaf) })
$examPython = $null
foreach ($examName in @('python', 'python3', 'py')) {
    $examCommand = Get-Command $examName -ErrorAction SilentlyContinue
    if (-not $examCommand) { continue }
    try {
        $examProbe = & $examCommand.Source -B -S -c "import sqlite3,sys; c=sqlite3.connect(':memory:'); c.execute('CREATE VIRTUAL TABLE t USING fts5(x)'); print('EXAM_OK' if sys.version_info >= (3,11) else 'OLD_PYTHON')" 2>$null
        if ($LASTEXITCODE -eq 0 -and $examProbe -contains 'EXAM_OK') { $examPython = $examCommand.Source; break }
    } catch { continue }
}
$examDbPresent = Test-Path -LiteralPath (Join-Path $examRoot 'plugins/expert-hub/skills/expert/scripts/expert.py') -PathType Leaf
$examBasicReady = $examMissing.Count -eq 0
$examDatabaseReady = $examDbPresent -and [bool]$examPython
[ordered]@{
    instruction_files_ready = $examBasicReady
    missing_files = $examMissing
    python_311_fts5_available = [bool]$examPython
    hub_files_present = $examDbPresent
    database_cli_ready = $examDatabaseReady
    mcp_required_for_cli = $false
    third_party_packages_required_for_core = $false
    codex_app_discovery_verified = $false
    note = 'Open the repository in Codex and read exam-kit/START.md. Without Python, instructions remain readable but the DB CLI cannot run. This probe does not test model behavior.'
} | ConvertTo-Json
if (-not $examBasicReady -or ($RequireDatabase -and -not $examDatabaseReady)) { exit 2 }
exit 0
