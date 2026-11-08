# Render the card faces to PNG with headless Microsoft Edge.
# Usage: pwsh -File tools/render.ps1 [-Only baize-front,qilin-back]
param(
  [string[]]$Only
)

$ErrorActionPreference = "Continue"
if ($Only) {
  $Only = @($Only | ForEach-Object { $_ -split "," } | ForEach-Object { $_.Trim() } | Where-Object { $_ })
}
$root = Split-Path -Parent $PSScriptRoot
$renders = Join-Path $root "cards\renders"
New-Item -ItemType Directory -Force -Path $renders | Out-Null

$edgeCandidates = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
  "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
  "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
)
$edge = $edgeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $edge) { throw "No Chromium browser found (Chrome or Edge)." }

$faces = @(
  @{ name = "baize-front"; file = "baize-front.html"; width = 750; height = 1050; scale = 2 },
  @{ name = "baize-back";  file = "baize-back.html";  width = 750; height = 1050; scale = 2 },
  @{ name = "qilin-front"; file = "qilin-front.html"; width = 750; height = 1050; scale = 2 },
  @{ name = "qilin-back";  file = "qilin-back.html";  width = 750; height = 1050; scale = 2 },
  @{ name = "baize-card";  file = "present-baize.html"; width = 1760; height = 1260; scale = 2 },
  @{ name = "qilin-card";  file = "present-qilin.html"; width = 1760; height = 1260; scale = 2 }
)

foreach ($face in $faces) {
  if ($Only -and ($Only -notcontains $face.name)) { continue }
  $out = Join-Path $renders ("{0}.png" -f $face.name)
  Remove-Item $out -Force -ErrorAction SilentlyContinue
  $url = "file:///" + ((Join-Path $root ("cards\" + $face.file)) -replace "\\", "/")
  $profile = Join-Path $env:TEMP ("dsh-card-" + [guid]::NewGuid().ToString("N"))
  try {
    & $edge --headless=new --disable-gpu --hide-scrollbars --no-first-run `
      "--user-data-dir=$profile" `
      "--force-device-scale-factor=$($face.scale)" `
      "--window-size=$($face.width),$($face.height)" `
      --virtual-time-budget=6000 `
      "--screenshot=$out" $url 2>&1 | Out-Null
    if (-not (Test-Path $out)) { throw "Render failed: $out" }
    $item = Get-Item $out
    Write-Host ("[ok] {0}  {1}x{2}px  {3:N0} bytes" -f $face.name, ($face.width * $face.scale), ($face.height * $face.scale), $item.Length)
  }
  finally {
    Remove-Item $profile -Recurse -Force -ErrorAction SilentlyContinue
  }
}
