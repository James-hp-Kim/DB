[CmdletBinding()]
param([string]$PythonExe, [string]$SkillDestination, [switch]$ManualMcp)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'scripts/Resolve-Python.ps1')
try { $expertPython = Resolve-QaPython -Requested $PythonExe }
catch { throw 'Install Python 3.11+ from https://www.python.org/downloads/windows/ . Reopen the installer. See INSTALL_NEW_PC_KO.md.' }
& $expertPython -B -X utf8 (Join-Path $PSScriptRoot 'scripts/verify_release.py')
if ($LASTEXITCODE -ne 0) { throw 'Release integrity check failed. Do not install this copy.' }
$expertOptions = @{ PythonExe=$expertPython }
if ($SkillDestination) { $expertOptions.SkillDestination=$SkillDestination }
$expertCli = Get-Command codex -ErrorAction SilentlyContinue
if ($expertCli -and -not $ManualMcp) { $expertOptions.EnableMcp=$true }
& (Join-Path $PSScriptRoot 'Install.ps1') @expertOptions
if (-not $SkillDestination) { $SkillDestination = Join-Path ([Environment]::GetFolderPath('UserProfile')) '.agents/skills/expert' }
$expertDestination = [IO.Path]::GetFullPath($SkillDestination)
& $expertPython -B -X utf8 (Join-Path $expertDestination 'scripts/verify_install.py')
if ($LASTEXITCODE -ne 0) { throw 'Skill copied, but the new MCP connection check failed.' }
if (-not $expertCli -or $ManualMcp) {
    Write-Output 'MCP registration is still required. Use a supported Codex CLI or your app''s MCP settings if available. STDIO values:'
    Write-Output 'Name: expert-knowledge'
    Write-Output "Command: $expertPython"
    Write-Output ('Arguments: ' + (@('-B','-X','utf8',(Join-Path $expertDestination 'scripts/mcp_server.py')) | ConvertTo-Json -Compress))
    Write-Output 'Reconnect or restart the supported app, then open a new chat. See INSTALL_NEW_PC_KO.md.'
} else { Write-Output 'MCP registered. Reconnect or restart Codex, then start a new chat; UI labels vary by app.' }
Write-Output 'No optional upstream tools were installed. The bundled fact-grounding guide works without other skills.'
