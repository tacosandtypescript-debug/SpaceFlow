$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Required = @(
    "VERSION",
    "pyproject.toml",
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
    "src/spaceflow/__init__.py",
    "scripts/install.sh",
    "scripts/install.ps1",
    ".github/workflows/ci.yml",
    ".github/workflows/release.yml"
)

foreach ($relative in $Required) {
    if (-not (Test-Path (Join-Path $Root $relative))) {
        throw "Falta el archivo requerido: $relative"
    }
}

$Version = (Get-Content (Join-Path $Root "VERSION") -Raw).Trim()
$PyProject = Get-Content (Join-Path $Root "pyproject.toml") -Raw
$Init = Get-Content (Join-Path $Root "src/spaceflow/__init__.py") -Raw
$Changelog = Get-Content (Join-Path $Root "CHANGELOG.md") -Raw
if ($PyProject -notmatch [regex]::Escape("version = `"$Version`"")) {
    throw "pyproject.toml no coincide con VERSION $Version"
}
if ($Init -notmatch [regex]::Escape("__version__ = `"$Version`"")) {
    throw "__init__.py no coincide con VERSION $Version"
}
if ($Changelog -notmatch [regex]::Escape("## [$Version]")) {
    throw "CHANGELOG.md no contiene la versión $Version"
}

$TrackedCandidates = Get-ChildItem $Root -Recurse -File | Where-Object {
    $_.FullName -notmatch '[\\/](\.git|dist|build|\.venv|__pycache__)[\\/]'
}
$ForbiddenNames = $TrackedCandidates | Where-Object {
    $_.Name -match '(?i)^cookies\.txt$|cookies.*\.txt$|\.mp3$|\.m4a$|\.part$'
}
if ($ForbiddenNames) {
    throw "Hay archivos privados o generados en el árbol: $($ForbiddenNames.FullName -join ', ')"
}

$tokens = $null
$errors = $null
[System.Management.Automation.Language.Parser]::ParseFile(
    (Join-Path $Root "scripts/install.ps1"), [ref]$tokens, [ref]$errors
) | Out-Null
if ($errors.Count) {
    throw "install.ps1 contiene errores de sintaxis: $($errors.Message -join '; ')"
}

$Python = Get-Command py -ErrorAction SilentlyContinue
if (-not $Python) {
    $candidate = Get-Command python -ErrorAction SilentlyContinue
    if ($candidate -and $candidate.Source -notmatch 'WindowsApps') { $Python = $candidate }
}
if ($Python) {
    & $Python.Source -m unittest discover -s (Join-Path $Root "tests") -v
    if ($LASTEXITCODE -ne 0) { throw "Fallaron las pruebas Python" }
}
else {
    Write-Warning "No hay un Python real; las pruebas de ejecución quedan para CI/dispositivo."
}

Write-Host "SpaceFlow ${Version}: validación de release correcta."
