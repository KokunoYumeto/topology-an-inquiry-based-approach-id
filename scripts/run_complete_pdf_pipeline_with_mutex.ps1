[CmdletBinding()]
param(
    [int]$MutexTimeoutMinutes = 15,
    [switch]$ResumeFromRun2
)

$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$pythonPath = [IO.Path]::GetFullPath((Join-Path $repoRoot '..\toolchain\pretext-1.7.5-py312\Scripts\python.exe'))
$mutexName = 'Global\InterlanguageTeXSlotV1'
$mutexReceipt = Join-Path $repoRoot 'qa\CHAPTERS01_20_COMPLETE_TEX_MUTEX.json'
$acquired = $false
$abandoned = $false
$requested = (Get-Date).ToUniversalTime()
$acquiredAt = $null
$releasedAt = $null
$stage = 'waiting-for-mutex'
$terminalStatus = 'running'
$failureMessage = $null
$mutex = [System.Threading.Mutex]::new($false, $mutexName)

function Write-PipelineState {
    $receipt = [ordered]@{
        schema_version = 1
        status = $terminalStatus
        stage = $stage
        process_id = $PID
        mutex = $mutexName
        abandoned_mutex_recovered = $abandoned
        requested_utc = $requested.ToString('o')
        acquired_utc = if ($null -eq $acquiredAt) { $null } else { $acquiredAt.ToString('o') }
        released_utc = if ($null -eq $releasedAt) { $null } else { $releasedAt.ToString('o') }
        failure = $failureMessage
        resume_from_verified_run_1 = [bool]$ResumeFromRun2
        scope = 'two clean strict TeX builds, normalized-byte comparison, immediate structure and all-page visual QA'
    }
    $json = ($receipt | ConvertTo-Json -Depth 5) + "`n"
    [IO.File]::WriteAllText($mutexReceipt, $json, [Text.UTF8Encoding]::new($false))
}

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)][string]$Program,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )
    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $Program $($Arguments -join ' ')"
    }
}

try {
    try {
        $acquired = $mutex.WaitOne([TimeSpan]::FromMinutes($MutexTimeoutMinutes))
    }
    catch [System.Threading.AbandonedMutexException] {
        $acquired = $true
        $abandoned = $true
    }
    if (-not $acquired) {
        throw "Timed out after $MutexTimeoutMinutes minutes waiting for $mutexName"
    }
    $acquiredAt = (Get-Date).ToUniversalTime()
    $stage = if ($ResumeFromRun2) { 'run-1-verified-resume' } else { 'run-1-build' }
    Write-PipelineState

    Set-Location -LiteralPath $repoRoot
    $common = @(
        'scripts/build_pretext_pdf_strict.py',
        'chapters01-20-complete-pdf',
        '--clean',
        '--expect-pdf', 'output/chapters01-20-complete-pdf/chapters_01_20_complete_reader.pdf',
        '--source-date-epoch', '1692057600',
        '--mainmatter-physical-page', '7',
        '--rewrite-uri', 'external/o003-epsilon-delta-lab.html=https://kokunoyumeto.github.io/topology-an-inquiry-based-approach-id/external/o003-epsilon-delta-lab.html'
    )

    if ($ResumeFromRun2) {
        Invoke-Checked $pythonPath @('scripts/qa_chapters01_20_complete_pdf_pipeline.py', 'record-run', '1', '--check')
    }
    else {
        Invoke-Checked $pythonPath ($common + @('--log', 'qa/CHAPTERS01_20_COMPLETE_PDF_BUILD_RUN1.log'))
        $stage = 'run-1-record'
        Write-PipelineState
        Invoke-Checked $pythonPath @('scripts/qa_chapters01_20_complete_pdf_pipeline.py', 'record-run', '1')
    }
    $stage = 'run-2-build'
    Write-PipelineState
    Invoke-Checked $pythonPath ($common + @('--log', 'qa/CHAPTERS01_20_COMPLETE_PDF_BUILD_RUN2.log'))
    $stage = 'run-2-record'
    Write-PipelineState
    Invoke-Checked $pythonPath @('scripts/qa_chapters01_20_complete_pdf_pipeline.py', 'record-run', '2')
    $stage = 'structure-and-render'
    Write-PipelineState
    Invoke-Checked $pythonPath @('scripts/inspect_pdf_structure.py', 'output/chapters01-20-complete-pdf/chapters_01_20_complete_reader.pdf', '--output', 'qa/CHAPTERS01_20_COMPLETE_PDF_STRUCTURE.json')
    Invoke-Checked $pythonPath @('scripts/qa_chapters01_20_complete_pdf_pipeline.py', 'prepare-render')

    $pdftoppmPath = (Get-Command pdftoppm -ErrorAction Stop).Source
    Invoke-Checked $pdftoppmPath @('-r', '120', '-png', 'output/chapters01-20-complete-pdf/chapters_01_20_complete_reader.pdf', 'tmp/pdfs/chapters01-20-complete-render/page')
    Invoke-Checked $pythonPath @('scripts/make_pdf_contact_sheets.py', 'tmp/pdfs/chapters01-20-complete-render', '--output-dir', 'tmp/pdfs/chapters01-20-complete-contact', '--columns', '4', '--rows', '3', '--thumbnail-width', '280')
    Invoke-Checked $pythonPath @('scripts/build_chapters01_20_complete_pdf_visual_qa.py', '--build-log', 'qa/CHAPTERS01_20_COMPLETE_PDF_BUILD_RUN2.log', '--renderer-label', 'Poppler pdftoppm 120 dpi')
    Invoke-Checked $pythonPath @('scripts/qa_chapters01_20_complete_pdf_pipeline.py', 'finalize')
    Invoke-Checked $pythonPath @('scripts/qa_chapters01_20_complete_pdf_pipeline.py', 'finalize', '--check')
    $stage = 'complete'
    $terminalStatus = 'pass'
}
catch {
    $terminalStatus = 'fail'
    $failureMessage = $_.Exception.Message
    throw
}
finally {
    if ($acquired) {
        $mutex.ReleaseMutex()
        $releasedAt = (Get-Date).ToUniversalTime()
    }
    $mutex.Dispose()
    Write-PipelineState
}
