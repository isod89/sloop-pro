# SLOOP Pro (SLOOP on the M-Vave SMK-37): build the three model packages in WSL, make the site, open the installer.
#   INSTALL-SLOOP-PRO.bat          build, then serve the installer and the editor on http://localhost:8767
#   build-sloop-pro.ps1 -NoServe   build only (the packages and their SHA-256 in build\release\)
#   build-sloop-pro.ps1 -Diag      a diagnostic build: the USB serial console in (HOME menu > USB > USB SERIAL ON, then
#                                  a terminal on the keyboard's COM port: status, smk, padtest, leds)
# Settings (environment, all optional):
#   SLOOP_WSL_DISTRO   the WSL distribution with the JieLi toolchain (default MinUI-Build, as SLOOP's own script)
#   SLOOP_TOOLCHAIN    the toolchain's Linux path (default /root/fm1-codex-deps/jieli/toolchain)
#   SLOOP_SDK          a Windows folder with cpu/wl82/tools from the AC79 SDK (default: build\deps\ac79 here, else the one
#                      of a SLOOP / sloop-fm1 folder next to this one)
# From a SLOOP folder next to this one it also takes the sample cache (build\genwav, gen_samples.cache: a faster first
# build) and the editor's audio preview (build\preview), when they are not here yet.
# SLICE stays out (FELUCCA_SLICE=0), as in SLOOP's build.
param([switch]$NoServe, [switch]$Diag)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$distro = if ($env:SLOOP_WSL_DISTRO) { $env:SLOOP_WSL_DISTRO } else { 'MinUI-Build' }
$tc = if ($env:SLOOP_TOOLCHAIN) { $env:SLOOP_TOOLCHAIN } else { '/root/fm1-codex-deps/jieli/toolchain' }
$sdk = $env:SLOOP_SDK
if (-not $sdk) {
  foreach ($c in @('build\deps\ac79', '..\SLOOP\build\deps\ac79', '..\SLOOP\sloop-2.8.1\build\deps\ac79',
                   '..\sloop-fm1\build\deps\ac79')) {
    if (Test-Path (Join-Path $c 'cpu\wl82\tools\uboot.boot')) { $sdk = $c; break }
  }
}
if (-not $sdk -or -not (Test-Path (Join-Path $sdk 'cpu\wl82\tools\uboot.boot'))) {
  throw "The AC79 SDK files were not found: copy build\deps\ac79 from your sloop-fm1 folder here, or set SLOOP_SDK"
}
foreach ($b in @('..\SLOOP\sloop-2.8.1\build', '..\SLOOP\build')) {   # (optional: caches and the audio preview)
  if (-not (Test-Path $b)) { continue }
  New-Item -ItemType Directory -Force build | Out-Null
  if (-not (Test-Path build\genwav) -and (Test-Path "$b\genwav")) { Copy-Item -Recurse "$b\genwav" build\genwav }
  if (-not (Test-Path build\gen_samples.cache) -and (Test-Path "$b\gen_samples.cache")) { Copy-Item "$b\gen_samples.cache" build\ }
  if (-not (Test-Path build\preview) -and (Test-Path "$b\preview")) { Copy-Item -Recurse "$b\preview" build\preview }
}
$m = Select-String -Path firmware\src\felucca.c -Pattern 'define FELUCCA_VERSION "SLOOP PRO ([^"]+)"' | Select-Object -First 1
if (-not $m) { throw "firmware\src\felucca.c: no SLOOP PRO version" }
$ver = $m.Matches[0].Groups[1].Value
Write-Host ""
Write-Host "  S L O O P   P R O   $ver" -ForegroundColor White
Write-Host "  ---- ---- ---- ----" -ForegroundColor DarkGray
Write-Host "  WSL $distro, toolchain $tc, SDK $sdk" -ForegroundColor DarkGray
Remove-Item Env:FELUCCA_SLICE -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force build\release | Out-Null
$models = @(@('pro', 'sloop-pro.fwsc', 'SMK-37 Pro / Starrykey 37 Play'), @('elite', 'sloop-pro-elite.fwsc', 'SMK-37 Elite'), @('mke', 'sloop-pro-mke.fwsc', 'MKE-P37'))
$first = $true
foreach ($mdl in $models) {
  Write-Host "== Building SLOOP Pro for the $($mdl[2]) (WSL $distro)" -ForegroundColor Cyan
  $a = @('tools/build_windows.py', '--distro', $distro, '--toolchain', $tc, '--sdk', $sdk, '--slice', '0', '--board', 'smk37', '--model', $mdl[0])
  if (-not $first) { $a += '--skip-generate' }
  if ($Diag) { $a += '--cdc' }
  python @a
  if ($LASTEXITCODE -ne 0) { throw "The build failed ($($mdl[2]))" }
  Copy-Item (Join-Path build $mdl[1]) (Join-Path build\release $mdl[1]) -Force
  $first = $false
}
$pk = $models | ForEach-Object { Join-Path build\release $_[1] }
Write-Host "== Packages (build\release)" -ForegroundColor Cyan
foreach ($p in $pk) { $h = (Get-FileHash -Algorithm SHA256 $p).Hash.ToLower(); Write-Host "  $p  $h" }
Get-FileHash -Algorithm SHA256 $pk | ForEach-Object { "$($_.Hash.ToLower())  $(Split-Path $_.Path -Leaf)" } | Set-Content build\release\SHA256SUMS.txt
Write-Host "== Making the installer site" -ForegroundColor Cyan
python web/make_site.py --pro $ver build/sloop-pro-site @pk
if ($LASTEXITCODE -ne 0) { throw "make_site failed" }
if ($NoServe) { exit 0 }
Write-Host ""
Write-Host "Installer: http://localhost:8767/webapp/installer/  (Chrome or Edge, the SMK-37 on USB)" -ForegroundColor Green
Write-Host "Editor:    http://localhost:8767/webapp/editor/" -ForegroundColor Green
Write-Host "Keep this window open during the install. Ctrl+C stops the server."
Start-Process "http://localhost:8767/webapp/installer/"
python -m http.server 8767 --bind 127.0.0.1 --directory build/sloop-pro-site
