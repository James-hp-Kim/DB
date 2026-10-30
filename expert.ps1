[CmdletBinding()]
param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Arguments)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'scripts/Resolve-Python.ps1')
$expertPython = Resolve-QaPython
& $expertPython -B -X utf8 (Join-Path $PSScriptRoot 'plugins/expert-hub/skills/expert/scripts/expert.py') @Arguments
exit $LASTEXITCODE
