param(
    [switch]$Permanent
)

$scriptsDir = Join-Path $PSScriptRoot "scripts"
$env:PATH = "$scriptsDir;$env:PATH"

if ($Permanent) {
    $userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    if ($userPath -split ";" -notcontains $scriptsDir) {
        [Environment]::SetEnvironmentVariable("PATH", "$scriptsDir;$userPath", "User")
        Write-Host "Added permanently to user PATH: $scriptsDir"
    } else {
        Write-Host "Already in user PATH: $scriptsDir"
    }
}
