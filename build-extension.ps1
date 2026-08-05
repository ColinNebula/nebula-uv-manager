$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$candidates = @(
    "$Env:ProgramFiles\Blender Foundation\Blender\blender.exe",
    "$Env:ProgramFiles\Blender Foundation\Blender 5.2\blender.exe",
    "$Env:ProgramFiles\Blender Foundation\Blender 5.1\blender.exe",
    "$Env:ProgramFiles\Blender Foundation\Blender 5.0\blender.exe",
    "$Env:ProgramFiles\Blender Foundation\Blender 4.2\blender.exe"
)

$blenderCmd = Get-Command blender -ErrorAction SilentlyContinue
if ($blenderCmd) {
    $blenderExe = $blenderCmd.Source
} else {
    $blenderExe = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
}

if (-not $blenderExe) {
    Write-Error "Could not find blender.exe. Install Blender 4.2+ or add it to PATH."
}

Write-Host "Using Blender:" $blenderExe
Write-Host "Running extension validate..."
& $blenderExe --command extension validate

Write-Host "Running extension build..."
& $blenderExe --command extension build

$zip = Get-ChildItem -Path $scriptDir -Filter "*.zip" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if ($zip) {
    Write-Host "Built package:" $zip.FullName
} else {
    Write-Warning "Build completed but no zip was found in $scriptDir"
}
