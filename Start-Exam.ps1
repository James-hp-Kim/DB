[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
if (-not (Get-Command codex.cmd -ErrorAction SilentlyContinue)) { throw 'Codex CLI is missing. Install it and reopen PowerShell.' }
& codex.cmd -m gpt-6.1-sol -C $PSScriptRoot
exit $LASTEXITCODE
