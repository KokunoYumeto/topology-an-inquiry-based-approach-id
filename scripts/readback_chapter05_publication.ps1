param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[0-9a-f]{40}$')]
    [string]$Commit
)

$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$destination = Join-Path $repo 'tmp\chapter05-public-readback'
if (Test-Path -LiteralPath $destination) {
    throw "Readback directory already exists: $destination"
}
New-Item -ItemType Directory -Path $destination | Out-Null

$raw = "https://raw.githubusercontent.com/KokunoYumeto/topology-an-inquiry-based-approach-id/$Commit"
$pages = 'https://kokunoyumeto.github.io/topology-an-inquiry-based-approach-id'
$checks = @(
    [pscustomobject]@{ Name = 'raw-readme'; Url = "$raw/README.md"; Local = 'README.md' },
    [pscustomobject]@{ Name = 'raw-manifest'; Url = "$raw/qa/CHAPTER05_HTML_MANIFEST.json"; Local = 'qa\CHAPTER05_HTML_MANIFEST.json' },
    [pscustomobject]@{ Name = 'raw-chapter'; Url = "$raw/source/chap_glb.ptx"; Local = 'source\chap_glb.ptx' },
    [pscustomobject]@{ Name = 'raw-exercises'; Url = "$raw/source/sec_glb_exer.ptx"; Local = 'source\sec_glb_exer.ptx' },
    [pscustomobject]@{ Name = 'raw-companion'; Url = "$raw/companion/chapter_05_greatest_lower_bound_self_study.ptx"; Local = 'companion\chapter_05_greatest_lower_bound_self_study.ptx' },
    [pscustomobject]@{ Name = 'raw-guides'; Url = "$raw/companion/chapter_05_intro_guides.ptx"; Local = 'companion\chapter_05_intro_guides.ptx' },
    [pscustomobject]@{ Name = 'pages-root'; Url = "$pages/"; Local = 'docs\index.html' },
    [pscustomobject]@{ Name = 'pages-wrapper'; Url = "$pages/o003-c90-chapters-01-05-reader.html"; Local = 'docs\o003-c90-chapters-01-05-reader.html' },
    [pscustomobject]@{ Name = 'pages-chapter'; Url = "$pages/chap_glb.html"; Local = 'docs\chap_glb.html' },
    [pscustomobject]@{ Name = 'pages-intro'; Url = "$pages/sec_glb_intro.html"; Local = 'docs\sec_glb_intro.html' },
    [pscustomobject]@{ Name = 'pages-distance'; Url = "$pages/sec_dist_point_set.html"; Local = 'docs\sec_dist_point_set.html' },
    [pscustomobject]@{ Name = 'pages-summary'; Url = "$pages/sec_glb_summ.html"; Local = 'docs\sec_glb_summ.html' },
    [pscustomobject]@{ Name = 'pages-exercises'; Url = "$pages/sec_glb_exer.html"; Local = 'docs\sec_glb_exer.html' },
    [pscustomobject]@{ Name = 'pages-companion'; Url = "$pages/o003-c90-ch05-companion.html"; Local = 'docs\o003-c90-ch05-companion.html' },
    [pscustomobject]@{ Name = 'pages-css'; Url = "$pages/external/o003-readable-layout.css"; Local = 'docs\external\o003-readable-layout.css' },
    [pscustomobject]@{ Name = 'pdf-01-02'; Url = "$pages/downloads/topologi-pendekatan-berbasis-inkuiri-bab-01-02-id.pdf"; Local = 'docs\downloads\topologi-pendekatan-berbasis-inkuiri-bab-01-02-id.pdf' },
    [pscustomobject]@{ Name = 'pdf-01-03'; Url = "$pages/downloads/topologi-pendekatan-berbasis-inkuiri-bab-01-03-id.pdf"; Local = 'docs\downloads\topologi-pendekatan-berbasis-inkuiri-bab-01-03-id.pdf' },
    [pscustomobject]@{ Name = 'pdf-01-04'; Url = "$pages/downloads/topologi-pendekatan-berbasis-inkuiri-bab-01-04-id.pdf"; Local = 'docs\downloads\topologi-pendekatan-berbasis-inkuiri-bab-01-04-id.pdf' },
    [pscustomobject]@{ Name = 'pdf-01-05'; Url = "$pages/downloads/topologi-pendekatan-berbasis-inkuiri-bab-01-05-id.pdf"; Local = 'docs\downloads\topologi-pendekatan-berbasis-inkuiri-bab-01-05-id.pdf' }
)

$rows = foreach ($check in $checks) {
    $local = Join-Path $repo $check.Local
    $download = Join-Path $destination ($check.Name + '.bin')
    $url = $check.Url + '?o003_readback=chapter05_20260822'
    $response = Invoke-WebRequest -Uri $url -OutFile $download -PassThru -UseBasicParsing -TimeoutSec 30
    $downloadItem = Get-Item -LiteralPath $download
    $localItem = Get-Item -LiteralPath $local
    $downloadHash = (Get-FileHash -LiteralPath $download -Algorithm SHA256).Hash.ToLowerInvariant()
    $localHash = (Get-FileHash -LiteralPath $local -Algorithm SHA256).Hash.ToLowerInvariant()
    [pscustomobject]@{
        name = $check.Name
        status = [int]$response.StatusCode
        bytes = $downloadItem.Length
        sha256 = $downloadHash
        expected_bytes = $localItem.Length
        expected_sha256 = $localHash
        exact = ($downloadItem.Length -eq $localItem.Length -and $downloadHash -eq $localHash)
        url = $check.Url
    }
}

$result = [ordered]@{
    schema_version = 1
    commit = $Commit
    checked_at_utc = (Get-Date).ToUniversalTime().ToString('o')
    status = if (@($rows | Where-Object { -not $_.exact -or $_.status -ne 200 }).Count -eq 0) { 'pass' } else { 'fail' }
    checks = @($rows)
}
$result | ConvertTo-Json -Depth 5
if ($result.status -ne 'pass') {
    exit 1
}
