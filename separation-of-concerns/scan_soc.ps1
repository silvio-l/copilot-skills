param(
  [string]$RepoRoot = (Get-Location).Path,
  [switch]$ChangedOnly,
  [int]$Top = 25,
  [switch]$Json
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoPath = (Resolve-Path -LiteralPath $RepoRoot).Path

$codeExtensions = @(
  '.dart', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.cjs',
  '.py', '.go', '.java', '.kt', '.swift', '.rs', '.cs',
  '.cpp', '.c', '.h', '.hpp', '.php', '.rb'
)

$excludedPathFragments = @(
  '\.git\',
  '\.dart_tool\',
  '\build\',
  '\dist\',
  '\coverage\',
  '\node_modules\',
  '\Pods\',
  '\DerivedData\'
)

$generatedFilePatterns = @(
  '\.g\.dart$',
  '\.freezed\.dart$',
  'app_localizations.*\.dart$',
  'generated_.*',
  'generated_plugin_registrant',
  'generated_plugins\.cmake'
)

$uiTokens = @(
  'package:flutter/material.dart',
  'package:flutter/widgets.dart',
  'go_router',
  'Navigator.',
  'context.push',
  'context.go',
  'SwiftUI',
  'Jetpack Compose',
  'react',
  'jsx'
)

$dataTokens = @(
  'drift',
  'sqflite',
  'sqlite',
  'NativeDatabase',
  'database',
  'repository',
  'dao',
  'query(',
  'select(',
  'insert(',
  'update(',
  'delete('
)

$networkTokens = @(
  'dio',
  'package:http',
  'axios',
  'fetch(',
  'retrofit',
  'URLSession'
)

$fileSystemTokens = @(
  'File(',
  'Directory(',
  'Process(',
  'Platform.',
  'stdin',
  'stdout'
)

$stateTokens = @(
  'Provider',
  'ConsumerWidget',
  'StatefulWidget',
  'StateNotifier',
  'ChangeNotifier',
  'Bloc',
  'Cubit',
  'setState('
)

function Test-MatchAny {
  param(
    [string]$Content,
    [string[]]$Patterns
  )

  foreach ($pattern in $Patterns) {
    if ($Content -match [regex]::Escape($pattern)) {
      return $true
    }
  }

  return $false
}

function Get-Layer {
  param([string]$RelativePath)

  $path = $RelativePath.ToLowerInvariant()

  if ($path -match '(screens|widgets|components|pages|views|ui)') { return 'presentation' }
  if ($path -match '(providers|controllers|viewmodels|view_models|bloc|cubits|notifiers)') { return 'application' }
  if ($path -match '(services|service|usecases|use_cases|domain|engines|calculators)') { return 'domain' }
  if ($path -match '(repositories|repository|dao|database|datasources|data_sources|store|persistence)') { return 'data' }
  if ($path -match '(models|entities|dto|dtos|contracts|types)') { return 'model' }

  return 'general'
}

$fileSizeGuidance = @{
  presentation = @{ Target = 250; Review = 350 }
  application  = @{ Target = 220; Review = 320 }
  domain       = @{ Target = 200; Review = 280 }
  data         = @{ Target = 220; Review = 320 }
  model        = @{ Target = 160; Review = 220 }
  general      = @{ Target = 300; Review = 450 }
}

function Get-FileSizeSignal {
  param(
    [int]$LineCount,
    [string]$Layer
  )

  $guidance = $fileSizeGuidance[$Layer]
  if (-not $guidance) {
    $guidance = $fileSizeGuidance['general']
  }

  if ($LineCount -gt $guidance.Review) {
    return [pscustomobject]@{
      Reason   = "File exceeds best-practice size guidance for $Layer files ($LineCount lines; target <= $($guidance.Target), hard review > $($guidance.Review))."
      Score    = 2
      Target   = $guidance.Target
      Review   = $guidance.Review
    }
  }

  if ($LineCount -gt $guidance.Target) {
    return [pscustomobject]@{
      Reason   = "File is above the preferred size for $Layer files ($LineCount lines; target <= $($guidance.Target), hard review > $($guidance.Review))."
      Score    = 1
      Target   = $guidance.Target
      Review   = $guidance.Review
    }
  }

  return [pscustomobject]@{
    Reason = $null
    Score  = 0
    Target = $guidance.Target
    Review = $guidance.Review
  }
}

function Get-FilesToScan {
  if ($ChangedOnly) {
    $statusOutput = git -C $repoPath status --porcelain
    if (-not $statusOutput) {
      return @()
    }

    $relativeFiles = $statusOutput |
      ForEach-Object {
        $line = $_.Trim()
        if ($line.Length -lt 4) { return }
        if ($line.StartsWith('?? ')) {
          $line.Substring(3)
          return
        }
        $line.Substring(3)
      } |
      Where-Object { $_ } |
      Sort-Object -Unique

    return $relativeFiles |
      ForEach-Object {
        $absolute = Join-Path $repoPath $_
        if (-not (Test-Path -LiteralPath $absolute)) { return }
        $item = Get-Item -LiteralPath $absolute
        if ($item.PSIsContainer) { return }
        if ($codeExtensions -notcontains $item.Extension.ToLowerInvariant()) { return }
        $item
      }
  }

  return Get-ChildItem -LiteralPath $repoPath -Recurse -File |
    Where-Object { $codeExtensions -contains $_.Extension.ToLowerInvariant() }
}

$results = New-Object System.Collections.Generic.List[object]

foreach ($file in Get-FilesToScan) {
  $fullPath = $file.FullName
  $normalizedPath = $fullPath.Replace('/', '\')

  if ($excludedPathFragments | Where-Object { $normalizedPath -match [regex]::Escape($_) }) {
    continue
  }

  $relativePath = $fullPath.Substring($repoPath.Length).TrimStart('\')

  if ($generatedFilePatterns | Where-Object { $relativePath -match $_ }) {
    continue
  }

  $content = Get-Content -LiteralPath $fullPath -Raw -ErrorAction SilentlyContinue
  if ([string]::IsNullOrWhiteSpace($content)) {
    continue
  }

  $lineCount = (Get-Content -LiteralPath $fullPath | Measure-Object -Line).Lines
  $layer = Get-Layer -RelativePath $relativePath
  $sizeSignal = Get-FileSizeSignal -LineCount $lineCount -Layer $layer
  $reasons = New-Object System.Collections.Generic.List[string]
  $score = 0

  $hasUi = Test-MatchAny -Content $content -Patterns $uiTokens
  $hasData = Test-MatchAny -Content $content -Patterns $dataTokens
  $hasNetwork = Test-MatchAny -Content $content -Patterns $networkTokens
  $hasFileSystem = Test-MatchAny -Content $content -Patterns $fileSystemTokens
  $hasState = Test-MatchAny -Content $content -Patterns $stateTokens

  $concernCount = @($hasUi, $hasData, $hasNetwork, $hasFileSystem, $hasState) |
    Where-Object { $_ } |
    Measure-Object |
    Select-Object -ExpandProperty Count

  switch ($layer) {
    'presentation' {
      if ($hasData) {
        $reasons.Add('Presentation file touches persistence/repository concerns.')
        $score += 3
      }
      if ($hasNetwork) {
        $reasons.Add('Presentation file touches networking directly.')
        $score += 2
      }
      if ($hasFileSystem) {
        $reasons.Add('Presentation file touches filesystem/process concerns.')
        $score += 2
      }
      if ($sizeSignal.Score -gt 0) {
        $reasons.Add($sizeSignal.Reason)
        $score += $sizeSignal.Score
      }
    }
    'application' {
      if ($hasFileSystem -or $hasNetwork) {
        $reasons.Add('Application/orchestration file mixes infrastructure concerns.')
        $score += 2
      }
      if ($sizeSignal.Score -gt 0) {
        $reasons.Add($sizeSignal.Reason)
        $score += $sizeSignal.Score
      }
    }
    'domain' {
      if ($hasUi) {
        $reasons.Add('Domain/service file imports UI or navigation concerns.')
        $score += 3
      }
      if ($hasData) {
        $reasons.Add('Domain/service file depends on persistence details.')
        $score += 2
      }
      if ($sizeSignal.Score -gt 0) {
        $reasons.Add($sizeSignal.Reason)
        $score += $sizeSignal.Score
      }
    }
    'data' {
      if ($hasUi) {
        $reasons.Add('Data/repository file imports UI or navigation concerns.')
        $score += 3
      }
      if ($sizeSignal.Score -gt 0) {
        $reasons.Add($sizeSignal.Reason)
        $score += $sizeSignal.Score
      }
    }
    'model' {
      if ($hasUi -or $hasData -or $hasNetwork -or $hasFileSystem) {
        $reasons.Add('Model/entity file owns runtime concerns beyond data shape.')
        $score += 3
      }
      if ($sizeSignal.Score -gt 0) {
        $reasons.Add($sizeSignal.Reason)
        $score += $sizeSignal.Score
      }
    }
    default {
      if ($sizeSignal.Score -gt 0) {
        $reasons.Add($sizeSignal.Reason)
        $score += $sizeSignal.Score
      }
    }
  }

  if ($concernCount -ge 3) {
    $reasons.Add("File mixes multiple concern clusters ($concernCount detected).")
    $score += 2
  }

  $classLikeCount = ([regex]::Matches(
      $content,
      '(?m)^\s*(class|interface|enum|struct|typedef|extension|trait)\s+\w+'
    )).Count
  if ($classLikeCount -ge 5) {
    $reasons.Add("File declares many top-level types ($classLikeCount).")
    $score += 1
  }

  if ($score -le 0) {
    continue
  }

  $severity = if ($score -ge 5) {
    'HIGH'
  } elseif ($score -ge 3) {
    'MEDIUM'
  } else {
    'LOW'
  }

  $suggestion = switch ($layer) {
    'presentation' { 'Push IO/business rules into providers, services, or repositories.' }
    'application' { 'Extract orchestration helpers or move pure rules into services.' }
    'domain' { 'Keep services pure and move UI/IO outward.' }
    'data' { 'Keep repositories infrastructure-only and move UI outward.' }
    'model' { 'Strip models back to data shape and lightweight invariants.' }
    default { 'Split by reason to change and move side effects to the edge.' }
  }

  $results.Add([pscustomobject]@{
      Severity   = $severity
      Layer      = $layer
      File       = $relativePath
      Lines      = $lineCount
      SizeTarget = $sizeSignal.Target
      SizeReview = $sizeSignal.Review
      Reasons    = $reasons -join ' '
      Suggestion = $suggestion
      Score      = $score
    })
}

$ordered = $results |
  Sort-Object @{ Expression = 'Score'; Descending = $true }, @{ Expression = 'Lines'; Descending = $true } |
  Select-Object -First $Top

if ($Json) {
  $ordered | ConvertTo-Json -Depth 4
  exit 0
}

if (-not $ordered) {
  Write-Output 'SOC scan found no obvious hotspots in the selected files.'
  exit 0
}

Write-Output 'SOC scan hotspots:'
foreach ($item in $ordered) {
  Write-Output ''
  Write-Output ("[{0}] {1} ({2}, {3} lines; target <= {4}, hard review > {5})" -f $item.Severity, $item.File, $item.Layer, $item.Lines, $item.SizeTarget, $item.SizeReview)
  Write-Output ("  Reasons: {0}" -f $item.Reasons)
  Write-Output ("  Suggestion: {0}" -f $item.Suggestion)
}
