$script:QaProbeScript = Join-Path $PSScriptRoot 'probe_python.py'
function Resolve-QaPython {
    param([string]$Requested)
    if ($Requested) {
        $qaResolved = & $Requested -X utf8 $script:QaProbeScript
        if ($LASTEXITCODE -ne 0) { throw 'The requested Python failed the version/SQLite FTS check.' }
        return ($qaResolved | Select-Object -Last 1).Trim()
    }
    $qaCommand = Get-Command python -ErrorAction SilentlyContinue
    if ($qaCommand) {
        $qaResolved = & $qaCommand.Source -X utf8 $script:QaProbeScript 2>$null
        if ($LASTEXITCODE -eq 0 -and $qaResolved) { return ($qaResolved | Select-Object -Last 1).Trim() }
    }
    $qaLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($qaLauncher) {
        $qaResolved = & $qaLauncher.Source -3 -X utf8 $script:QaProbeScript 2>$null
        if ($LASTEXITCODE -eq 0 -and $qaResolved) { return ($qaResolved | Select-Object -Last 1).Trim() }
    }
    throw 'Install Python 3.11+ with SQLite/FTS5 and reopen PowerShell. Or pass -PythonExe with its full path.'
}
