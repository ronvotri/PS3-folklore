$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$homeDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$sha = 'da719ceb880c8d2903d09027379cb5226d9be45b'
$zip = Join-Path $homeDir 'github-Folklore-batch02.zip'
$extract = Join-Path $homeDir '_source-20261014-batch02'

try {
  Write-Host 'FOLKLORE CMC FIXED-BYTE BATCH 0.2 - TEST COPY ONLY'
  Write-Host 'This is NOT a full translation patch.'
  Write-Host 'This workflow needs a COPY of the game. Do not use your only original.'
  $game = (Read-Host 'Paste your TEST GAME COPY folder path').Trim().Trim('"')
  if (-not $game -or -not (Test-Path -LiteralPath $game -PathType Container)) {
    throw 'Test game copy folder does not exist.'
  }
  Write-Host '1 - PLAN ONLY (read-only)'
  Write-Host '2 - APPLY fixed-length eligible translated lines (writes to TEST COPY)'
  Write-Host '3 - RESTORE CMC regions from batch backup'
  $choice = (Read-Host 'Your choice (1/2/3)').Trim()
  if ($choice -notin @('1','2','3')) { throw 'Invalid choice.' }
  if ($choice -ne '1') {
    Write-Host 'WARNING: This action will write to your chosen game folder.'
    Write-Host 'Ensure RPCS3 is closed and this folder is NOT your only copy.'
    $confirm = Read-Host 'Type exactly TEST COPY to continue'
    if ($confirm -cne 'TEST COPY') { throw 'Not confirmed; nothing modified.' }
  }
  $pythonCommand = Get-Command 'py' -ErrorAction SilentlyContinue
  if ($pythonCommand) {
    $pyexe = 'py'
    $pyargs = @('-3')
  } elseif (Get-Command 'python' -ErrorAction SilentlyContinue) {
    $pyexe = 'python'
    $pyargs = @()
  } else { throw 'Python 3.10+ not found. Install Python first.' }

  if (-not (Test-Path -LiteralPath $extract -PathType Container)) {
    Write-Host 'Downloading pinned GitHub source (catalogs and tools only)...'
    $url = "https://github.com/ronvotri/PS3-folklore/archive/$sha.zip"
    Invoke-WebRequest -Uri $url -OutFile $zip -UseBasicParsing
    New-Item -ItemType Directory -Force -Path $extract | Out-Null
    Expand-Archive -LiteralPath $zip -DestinationPath $extract -Force
  }
  $repos = @(Get-ChildItem -LiteralPath $extract -Directory)
  if ($repos.Count -ne 1) { throw 'Unexpected source archive contents.' }
  $repo = $repos[0].FullName
  $tool = Join-Path $repo 'tools/cmc_batch_fixed.py'
  if (-not (Test-Path -LiteralPath $tool)) { throw 'Batch tool absent in pinned source.' }
  Push-Location $repo
  try {
    if ($choice -eq '3') {
      & $pyexe @pyargs $tool --game-root $game --action restore --confirm-test-copy
      if ($LASTEXITCODE -ne 0) { throw 'Restore refused or failed. Read error above.' }
      Write-Host 'RESTORE RESULT: see printed result. Backup retained.'
    } else {
      & $pyexe @pyargs $tool --game-root $game --action plan
      if ($LASTEXITCODE -ne 0) { throw 'Plan refused. Restore any previous CMC alpha patch on the TEST COPY first.' }
      $plan = Join-Path $repo 'dist/cmc-fixed-batch-plan.json'
      $share = Join-Path $homeDir 'GUI_CHO_CHATGPT_CMC_BATCH_PLAN.json'
      Copy-Item -LiteralPath $plan -Destination $share -Force
      Write-Host "Plan summary saved: $share"
      if ($choice -eq '2') {
        & $pyexe @pyargs $tool --game-root $game --action apply --confirm-test-copy
        if ($LASTEXITCODE -ne 0) { throw 'Apply refused or failed. Read error above.' }
        Write-Host 'INSTALL RESULT: test your GAME COPY in RPCS3. You can restore via option 3.'
      }
    }
  } finally { Pop-Location }
  Write-Host 'FINISHED.'
} catch {
  Write-Host ('ERROR: ' + $_.Exception.Message) -ForegroundColor Red
  exit 1
}
