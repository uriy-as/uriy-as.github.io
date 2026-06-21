param(
    [string]$Token = "8308743016:AAEwu53QB_rwy5Di40YON4NBZA4A6SbgRQ0",
    [string]$ChatId = "@webstudio_chanel",
    [string]$StateFile = "C:\Users\Admin\.telegram-poster-state.json"
)

$PostsFile = "C:\Users\Admin\Documents\site\.github\scripts\posts.json"
$ErrorActionPreference = "Stop"

function Write-Status { param([string]$msg) Write-Host $msg }

function Read-JsonFile {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return $null }
    try { return Get-Content $Path -Raw -Encoding UTF8 | ConvertFrom-Json }
    catch { Write-Status "WARN: Invalid JSON in $Path - $_"; return $null }
}

function Write-JsonFile {
    param([string]$Path, $Data)
    $tmp = $Path + ".tmp"
    $bak = $Path + ".bak"
    $Data | ConvertTo-Json -Compress | Set-Content -Path $tmp -Encoding UTF8 -Force
    if (Test-Path $Path) { Copy-Item -Path $Path -Destination $bak -Force }
    Move-Item -Path $tmp -Destination $Path -Force
}

$Parsed = Read-JsonFile $PostsFile
if ($null -eq $Parsed) { Write-Status "FAIL: Cannot read posts.json"; exit 1 }
if ($Parsed.Count -eq 0) { Write-Status "FAIL: posts.json is empty"; exit 1 }

$State = Read-JsonFile $StateFile
if ($null -eq $State -or $null -eq $State.used) { $State = @{ used = @() } }

$unused = @()
for ($i = 0; $i -lt $Parsed.Count; $i++) {
    if ($State.used -notcontains $i) { $unused += $i }
}
if ($unused.Count -eq 0) {
    $State.used = @()
    $unused = @(0..($Parsed.Count-1))
}

$nextIdx = $unused[0]
$Post = $Parsed[$nextIdx]

try {
    $body = @{ chat_id = $ChatId; text = $Post[2]; parse_mode = "HTML" }
    $result = Invoke-RestMethod -Uri "https://api.telegram.org/bot$Token/sendMessage" -Method Post -Body $body -TimeoutSec 20
    if ($result.ok) {
        $State.used += $nextIdx
        Write-JsonFile $StateFile $State
        Write-Status "OK: Sent ($nextIdx) $($Post[1])"
    } else {
        Write-Status "FAIL: API returned not ok"; exit 1
    }
} catch {
    Write-Status "FAIL: $_"; exit 1
}