[CmdletBinding()]
param([string]$PythonExe)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'scripts/Resolve-Python.ps1')
$qaPython = Resolve-QaPython -Requested $PythonExe
Write-Output "Python: $qaPython"
& $qaPython -X utf8 (Join-Path $PSScriptRoot 'plugins/expert-hub/skills/expert/scripts/expert.py') status
if ($LASTEXITCODE -ne 0) { throw 'Knowledge check failed.' }
if (Get-Command codex -ErrorAction SilentlyContinue) { & codex --version }
else { Write-Output 'Codex CLI not found. Desktop-only users can use the standalone skill; CLI is optional for the basic skill.' }
& $qaPython -X utf8 (Join-Path $PSScriptRoot 'scripts/probe_python.py') --packages
Write-Output 'Optional analysis packages do not affect knowledge search or standard-library CSV monitoring.'
