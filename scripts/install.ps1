$ErrorActionPreference = "Stop"
$Repo = "tacosandtypescript-debug/SpaceFlow"
$AppDir = Join-Path $env:LOCALAPPDATA "SpaceFlow"
$BinDir = Join-Path $AppDir "bin"

function Find-Python {
    foreach ($candidate in @("py", "python")) {
        $command = Get-Command $candidate -ErrorAction SilentlyContinue
        if ($command) {
            try {
                & $candidate -c "import sys; assert sys.version_info >= (3,10)" 2>$null
                if ($LASTEXITCODE -eq 0) { return $candidate }
            } catch {}
        }
    }
    return $null
}

$Python = Find-Python
if (-not $Python) {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "Instala Python 3.10 o superior y ejecuta de nuevo este instalador."
    }
    winget install --id Python.Python.3.12 --scope user --accept-source-agreements --accept-package-agreements
    $Python = "py"
}

if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install --id Gyan.FFmpeg --scope user --accept-source-agreements --accept-package-agreements
    } else {
        throw "Instala FFmpeg y ejecuta de nuevo este instalador."
    }
}

& $Python -m pip install --user --upgrade yt-dlp
New-Item -ItemType Directory -Force -Path $AppDir, $BinDir | Out-Null
$Release = "https://github.com/$Repo/releases/latest/download"
$NewApp = Join-Path $AppDir "spaceflow.pyz.new"
$App = Join-Path $AppDir "spaceflow.pyz"
$Checksums = Join-Path $AppDir "SHA256SUMS"
Invoke-WebRequest "$Release/spaceflow.pyz" -OutFile $NewApp
Invoke-WebRequest "$Release/SHA256SUMS" -OutFile $Checksums

$Expected = ((Get-Content $Checksums | Where-Object { $_ -match "spaceflow\.pyz$" }) -split "\s+")[0]
$Actual = (Get-FileHash -Algorithm SHA256 $NewApp).Hash.ToLowerInvariant()
if (-not $Expected -or $Expected.ToLowerInvariant() -ne $Actual) {
    Remove-Item -Force $NewApp
    throw "El checksum de SpaceFlow no coincide."
}
Move-Item -Force $NewApp $App

$Launcher = Join-Path $BinDir "spaceflow.cmd"
"@echo off`r`n$Python `"$App`" %*`r`n" | Set-Content -Encoding ASCII $Launcher
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if (($UserPath -split ";") -notcontains $BinDir) {
    [Environment]::SetEnvironmentVariable("Path", "$UserPath;$BinDir", "User")
}

Write-Host "SpaceFlow instalado. Abre otra terminal y ejecuta:"
Write-Host "spaceflow --version"
Write-Host "spaceflow"
Write-Host "Las cookies son opcionales y solo hacen falta si X exige iniciar sesión."
