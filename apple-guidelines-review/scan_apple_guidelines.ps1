param(
  [string]$RepoRoot = (Get-Location).Path,
  [switch]$ChangedOnly,
  [int]$Top = 30,
  [switch]$Json
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false

$repoPath = (Resolve-Path -LiteralPath $RepoRoot).Path

$codeExtensions = @(
  '.swift', '.m', '.mm', '.h',
  '.plist', '.entitlements', '.pbxproj', '.storyboard', '.xib', '.xcprivacy',
  '.dart', '.ts', '.tsx', '.js', '.jsx',
  '.json', '.yaml', '.yml', '.gradle', '.kt', '.java'
)

$excludedPathFragments = @(
  '\.git\',
  '\.dart_tool\',
  '\build\',
  '\dist\',
  '\coverage\',
  '\node_modules\',
  '\Pods\',
  '\DerivedData\',
  '\test\',
  '\tests\',
  '__tests__',
  '\spec\',
  '\Specs\'
)

$generatedFilePatterns = @(
  '\.g\.dart$',
  '\.freezed\.dart$',
  'app_localizations.*\.dart$',
  'generated_.*',
  'generated_plugin_registrant',
  'Podfile\.lock$',
  'package-lock\.json$',
  'pnpm-lock\.yaml$',
  'yarn\.lock$'
)

$notes = New-Object System.Collections.Generic.List[string]
$findings = New-Object System.Collections.Generic.List[object]

function Test-GitRepo {
  & cmd.exe /d /c "git -C `"$repoPath`" rev-parse --is-inside-work-tree >nul 2>nul" | Out-Null
  return $LASTEXITCODE -eq 0
}

$isGitRepo = Test-GitRepo

function Get-FilesToScan {
  if ($ChangedOnly) {
    if (-not $isGitRepo) {
      $notes.Add('ChangedOnly requested, but no git repository was detected. Scanning the full repo scope instead.')
    } else {
      $relativeFiles = New-Object System.Collections.Generic.List[string]
      $gitCommands = @(
        @('diff', '--name-only', '--cached', '--diff-filter=ACMR'),
        @('diff', '--name-only', '--diff-filter=ACMR'),
        @('ls-files', '--others', '--exclude-standard')
      )

      foreach ($gitArgs in $gitCommands) {
        $output = & git -C $repoPath @gitArgs 2>$null
        foreach ($line in @($output)) {
          $candidate = ([string]$line).Trim()
          if ([string]::IsNullOrWhiteSpace($candidate)) {
            continue
          }
          $relativeFiles.Add($candidate)
        }
      }

      $relativeFiles = @($relativeFiles | Sort-Object -Unique)
      if (-not $relativeFiles -or $relativeFiles.Count -eq 0) {
        return @()
      }

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
  }

  return Get-ChildItem -LiteralPath $repoPath -Recurse -File |
    Where-Object { $codeExtensions -contains $_.Extension.ToLowerInvariant() }
}

function Get-Documents {
  $items = Get-FilesToScan
  foreach ($file in $items) {
    $normalizedPath = $file.FullName.Replace('/', '\')
    if ($excludedPathFragments | Where-Object { $normalizedPath -match [regex]::Escape($_) }) {
      continue
    }

    $relativePath = $file.FullName.Substring($repoPath.Length).TrimStart('\')
    if ($generatedFilePatterns | Where-Object { $relativePath -match $_ }) {
      continue
    }

    $lines = @(Get-Content -LiteralPath $file.FullName -ErrorAction SilentlyContinue)
    if (-not $lines -or $lines.Count -eq 0) {
      continue
    }

    [pscustomobject]@{
      FullPath     = $file.FullName
      RelativePath = $relativePath
      Extension    = $file.Extension.ToLowerInvariant()
      Lines        = $lines
      Content      = [string]::Join("`n", $lines)
    }
  }
}

function Find-FirstHit {
  param(
    [object[]]$Docs,
    [string[]]$Patterns
  )

  foreach ($doc in $Docs) {
    for ($index = 0; $index -lt $doc.Lines.Count; $index++) {
      $line = [string]$doc.Lines[$index]
      foreach ($pattern in $Patterns) {
        if ($line -match [regex]::Escape($pattern)) {
          return [pscustomobject]@{
            File    = $doc.RelativePath
            Line    = $index + 1
            Pattern = $pattern
            Snippet = $line.Trim()
          }
        }
      }
    }
  }

  return $null
}

function Get-PlistStringValues {
  param(
    [string]$Content,
    [string]$Key
  )

  $pattern = "<key>\s*$([regex]::Escape($Key))\s*</key>\s*<string>\s*(.*?)\s*</string>"
  $matches = [System.Text.RegularExpressions.Regex]::Matches(
    $Content,
    $pattern,
    [System.Text.RegularExpressions.RegexOptions]::Singleline
  )

  $values = New-Object System.Collections.Generic.List[string]
  foreach ($match in $matches) {
    $values.Add($match.Groups[1].Value.Trim())
  }

  return @($values)
}

function Get-PlistArrayValues {
  param(
    [string]$Content,
    [string]$Key
  )

  $pattern = "<key>\s*$([regex]::Escape($Key))\s*</key>\s*<array>(.*?)</array>"
  $match = [System.Text.RegularExpressions.Regex]::Match(
    $Content,
    $pattern,
    [System.Text.RegularExpressions.RegexOptions]::Singleline
  )

  if (-not $match.Success) {
    return @()
  }

  $arrayValues = [System.Text.RegularExpressions.Regex]::Matches(
    $match.Groups[1].Value,
    "<string>\s*(.*?)\s*</string>",
    [System.Text.RegularExpressions.RegexOptions]::Singleline
  )

  $values = New-Object System.Collections.Generic.List[string]
  foreach ($arrayValue in $arrayValues) {
    $values.Add($arrayValue.Groups[1].Value.Trim())
  }

  return @($values)
}

function Test-PlaceholderString {
  param([string]$Value)

  if ([string]::IsNullOrWhiteSpace($Value)) {
    return $true
  }

  return $Value -match '(?i)\b(todo|tbd|placeholder|describe|explain|required|purpose string|why needed)\b'
}

function Add-Finding {
  param(
    [string]$Severity,
    [string]$EvidenceClass,
    [string]$Category,
    [string]$Guideline,
    [string]$Evidence,
    [string]$Reason,
    [string]$Fix,
    [int]$Score
  )

  $findings.Add([pscustomobject]@{
      Severity      = $Severity
      EvidenceClass = $EvidenceClass
      Category      = $Category
      Guideline     = $Guideline
      Evidence      = $Evidence
      Reason        = $Reason
      Fix           = $Fix
      Score         = $Score
    })
}

$documents = @(Get-Documents)

if (-not $documents -or $documents.Count -eq 0) {
  $message = if ($ChangedOnly -and $isGitRepo) {
    'No Apple-relevant source files were found in the changed scope.'
  } else {
    'No Apple-relevant source files were found in the selected scope.'
  }

  if ($Json) {
    [pscustomobject]@{
      Notes    = @($notes)
      Findings = @()
      Message  = $message
    } | ConvertTo-Json -Depth 5
    exit 0
  }

  if ($notes.Count -gt 0) {
    Write-Output 'Scanner notes:'
    foreach ($note in $notes) {
      Write-Output ("- {0}" -f $note)
    }
    Write-Output ''
  }

  Write-Output $message
  exit 0
}

$plistDocs = @($documents | Where-Object { $_.Extension -eq '.plist' })
$privacyManifestDocs = @($documents | Where-Object { $_.Extension -eq '.xcprivacy' })
$allKeyNames = @(
  'NSCameraUsageDescription',
  'NSMicrophoneUsageDescription',
  'NSPhotoLibraryUsageDescription',
  'NSPhotoLibraryAddUsageDescription',
  'NSLocationWhenInUseUsageDescription',
  'NSLocationAlwaysAndWhenInUseUsageDescription',
  'NSLocationAlwaysUsageDescription',
  'NSContactsUsageDescription',
  'NSSpeechRecognitionUsageDescription',
  'NSMotionUsageDescription',
  'NSHealthShareUsageDescription',
  'NSHealthUpdateUsageDescription',
  'NSUserTrackingUsageDescription'
) | Sort-Object -Unique

$plistKeyValues = @{}
foreach ($keyName in $allKeyNames) {
  $plistKeyValues[$keyName] = @()
}

$backgroundModes = New-Object System.Collections.Generic.List[object]

foreach ($plistDoc in $plistDocs) {
  foreach ($keyName in $allKeyNames) {
    $values = Get-PlistStringValues -Content $plistDoc.Content -Key $keyName
    foreach ($value in $values) {
      $plistKeyValues[$keyName] += [pscustomobject]@{
        File  = $plistDoc.RelativePath
        Value = $value
      }
    }
  }

  $modes = Get-PlistArrayValues -Content $plistDoc.Content -Key 'UIBackgroundModes'
  foreach ($mode in $modes) {
    $backgroundModes.Add([pscustomobject]@{
        File = $plistDoc.RelativePath
        Mode = $mode
      })
  }
}

$permissionRules = @(
  [pscustomobject]@{
    Name      = 'camera'
    Tokens    = @('AVCaptureDevice', 'AVCaptureSession', 'UIImagePickerController.SourceType.camera', 'Permission.camera', 'permission.camera', 'package:camera/', 'react-native-image-picker')
    Keys      = @('NSCameraUsageDescription')
    KeyMode   = 'All'
    Guideline = '5.1.1(ii), 5.1.1(iii)'
    Fix       = 'Add a concrete camera purpose string and request camera access only when the related feature is invoked.'
  },
  [pscustomobject]@{
    Name      = 'microphone'
    Tokens    = @('AVAudioSession', 'AVAudioRecorder', 'Permission.microphone', 'permission.microphone', 'react-native-audio-recorder-player')
    Keys      = @('NSMicrophoneUsageDescription')
    KeyMode   = 'All'
    Guideline = '5.1.1(ii), 5.1.1(iii), 2.5.14'
    Fix       = 'Add a specific microphone purpose string and ensure consent is requested from a clear user action.'
  },
  [pscustomobject]@{
    Name      = 'speech recognition'
    Tokens    = @('SFSpeechRecognizer', 'speech_to_text')
    Keys      = @('NSSpeechRecognitionUsageDescription')
    KeyMode   = 'All'
    Guideline = '5.1.1(ii), 5.1.1(iii)'
    Fix       = 'Add a speech-recognition purpose string before using speech transcription features.'
  },
  [pscustomobject]@{
    Name      = 'photo library'
    Tokens    = @('PHPhotoLibrary', 'UIImagePickerController', 'Permission.photos', 'permission.photos', 'photo_manager', 'react-native-cameraroll')
    Keys      = @('NSPhotoLibraryUsageDescription')
    KeyMode   = 'All'
    Guideline = '5.1.1(ii), 5.1.1(iii)'
    Fix       = 'Add a photo-library purpose string or switch to a lower-privilege picker flow when possible.'
  },
  [pscustomobject]@{
    Name      = 'photo library add-only'
    Tokens    = @('UIImageWriteToSavedPhotosAlbum', 'Permission.photosAddOnly', 'permission.photosAddOnly')
    Keys      = @('NSPhotoLibraryAddUsageDescription')
    KeyMode   = 'All'
    Guideline = '5.1.1(ii), 5.1.1(iii)'
    Fix       = 'Add a photo-library add-only purpose string for save/export flows.'
  },
  [pscustomobject]@{
    Name      = 'location when in use'
    Tokens    = @('CLLocationManager', 'requestWhenInUseAuthorization', 'Permission.location', 'permission.location', 'geolocator')
    Keys      = @('NSLocationWhenInUseUsageDescription')
    KeyMode   = 'All'
    Guideline = '5.1.1(ii), 5.1.1(iii), 5.1.1(iv)'
    Fix       = 'Add a specific location purpose string and provide a fallback flow where practical if the user declines access.'
  },
  [pscustomobject]@{
    Name      = 'location always'
    Tokens    = @('requestAlwaysAuthorization')
    Keys      = @('NSLocationAlwaysAndWhenInUseUsageDescription', 'NSLocationAlwaysUsageDescription')
    KeyMode   = 'Any'
    Guideline = '5.1.1(ii), 5.1.1(iii), 5.1.1(iv)'
    Fix       = 'Add the required always-location purpose string for background or always-on location access.'
  },
  [pscustomobject]@{
    Name      = 'contacts'
    Tokens    = @('CNContactStore', 'contacts_service', 'Permission.contacts', 'permission.contacts')
    Keys      = @('NSContactsUsageDescription')
    KeyMode   = 'All'
    Guideline = '5.1.1(ii), 5.1.1(iii)'
    Fix       = 'Add a clear contacts purpose string and request only the minimum data needed for the feature.'
  },
  [pscustomobject]@{
    Name      = 'motion'
    Tokens    = @('CMMotionActivityManager', 'CMPedometer', 'Permission.sensors', 'permission.sensors')
    Keys      = @('NSMotionUsageDescription')
    KeyMode   = 'All'
    Guideline = '5.1.1(ii), 5.1.1(iii)'
    Fix       = 'Add a motion-data purpose string tied to the user-facing feature that needs it.'
  },
  [pscustomobject]@{
    Name      = 'health data read'
    Tokens    = @('HKHealthStore', 'health_kit_reporter', 'health')
    Keys      = @('NSHealthShareUsageDescription')
    KeyMode   = 'All'
    Guideline = '1.4.1, 5.1.1(ii), 5.1.1(iii)'
    Fix       = 'Add the HealthKit read/share purpose string and verify the feature only requests the scopes required for its core use case.'
  }
)

foreach ($permissionRule in $permissionRules) {
  $usageHit = Find-FirstHit -Docs $documents -Patterns $permissionRule.Tokens
  if (-not $usageHit) {
    continue
  }

  $matchingKeyValues = New-Object System.Collections.Generic.List[object]
  $missingKeys = New-Object System.Collections.Generic.List[string]

  foreach ($keyName in $permissionRule.Keys) {
    $keyValues = @($plistKeyValues[$keyName])
    if ($keyValues.Count -eq 0) {
      $missingKeys.Add($keyName)
      continue
    }

    foreach ($keyValue in $keyValues) {
      $matchingKeyValues.Add($keyValue)
    }
  }

  $keyMode = if ($permissionRule.PSObject.Properties.Name -contains 'KeyMode') {
    [string]$permissionRule.KeyMode
  } else {
    'All'
  }

  $isMissing = if ($keyMode -eq 'Any') {
    $matchingKeyValues.Count -eq 0
  } else {
    $missingKeys.Count -gt 0
  }

  if ($isMissing) {
    $expectedKeys = if ($keyMode -eq 'Any') {
      $permissionRule.Keys -join ' or '
    } else {
      $missingKeys -join ', '
    }

    Add-Finding `
      -Severity 'High' `
      -EvidenceClass 'Code-verifiable' `
      -Category 'privacy' `
      -Guideline $permissionRule.Guideline `
      -Evidence ("{0}:{1} references {2}; missing Info.plist purpose string(s): {3}." -f $usageHit.File, $usageHit.Line, $usageHit.Pattern, $expectedKeys) `
      -Reason ("Sensitive {0} access appears in code, but the repo does not expose the required user-facing purpose string coverage." -f $permissionRule.Name) `
      -Fix $permissionRule.Fix `
      -Score 9
    continue
  }

  $weakValue = $matchingKeyValues | Where-Object { Test-PlaceholderString -Value $_.Value } | Select-Object -First 1
  if ($weakValue) {
    Add-Finding `
      -Severity 'Medium' `
      -EvidenceClass 'Code-verifiable' `
      -Category 'privacy' `
      -Guideline $permissionRule.Guideline `
      -Evidence ("{0} contains a weak or placeholder purpose string for {1} access." -f $weakValue.File, $permissionRule.Name) `
      -Reason ("Apple review often questions vague permission copy because users cannot tell why {0} access is needed." -f $permissionRule.Name) `
      -Fix $permissionRule.Fix `
      -Score 6
  }
}

$healthDocs = @(
  $documents | Where-Object {
    $_.Content -match [regex]::Escape('HKHealthStore') -or
    $_.Content -match [regex]::Escape('health_kit_reporter')
  }
)
$healthWriteHit = Find-FirstHit -Docs $healthDocs -Patterns @(
  '.save(',
  'save(sample',
  'deleteObject(',
  'deleteObjects('
)
$healthUpdateValues = @($plistKeyValues['NSHealthUpdateUsageDescription'])

if ($healthWriteHit -and ($healthUpdateValues.Count -eq 0)) {
  Add-Finding `
    -Severity 'High' `
    -EvidenceClass 'Code-verifiable' `
    -Category 'privacy' `
    -Guideline '1.4.1, 5.1.1(ii), 5.1.1(iii)' `
    -Evidence ("{0}:{1} suggests HealthKit write access via {2}; NSHealthUpdateUsageDescription is missing." -f $healthWriteHit.File, $healthWriteHit.Line, $healthWriteHit.Pattern) `
    -Reason 'HealthKit write flows need the update usage description in addition to any read/share disclosure.' `
    -Fix 'Add NSHealthUpdateUsageDescription whenever the app writes or deletes HealthKit samples.' `
    -Score 9
}

$thirdPartyLoginHit = Find-FirstHit -Docs $documents -Patterns @(
  'GoogleSignIn',
  'GIDSignIn',
  'FBSDKLoginKit',
  'FacebookAuthProvider',
  'GoogleAuthProvider',
  'Login with Amazon',
  'WeChatOpenSDK',
  '@react-native-google-signin/google-signin',
  'react-native-fbsdk-next'
)
$appleLoginHit = Find-FirstHit -Docs $documents -Patterns @(
  'ASAuthorizationAppleIDProvider',
  'SignInWithAppleButton',
  'AppleIDAuthProvider',
  'sign_in_with_apple',
  'ASAuthorizationController'
)

if ($thirdPartyLoginHit -and -not $appleLoginHit) {
  Add-Finding `
    -Severity 'High' `
    -EvidenceClass 'Partial' `
    -Category 'auth' `
    -Guideline '4.8' `
    -Evidence ("{0}:{1} references {2}; no Sign in with Apple implementation signal was found." -f $thirdPartyLoginHit.File, $thirdPartyLoginHit.Line, $thirdPartyLoginHit.Pattern) `
    -Reason 'Third-party login often triggers the Sign in with Apple requirement when it is used for the app''s primary account.' `
    -Fix 'Add Sign in with Apple or explicitly confirm that a guideline 4.8 exception applies.' `
    -Score 9
}

$accountCreationHit = Find-FirstHit -Docs $documents -Patterns @(
  'createUser',
  'signUp',
  'signup',
  'createAccount',
  'Create Account',
  'Auth.auth().createUser'
)
$accountDeletionHit = Find-FirstHit -Docs $documents -Patterns @(
  'deleteAccount',
  'deleteUser',
  'removeAccount',
  'eraseAccount',
  'deactivateAccount',
  'accountDeletion',
  'deleteMyAccount'
)

if ($accountCreationHit -and -not $accountDeletionHit) {
  Add-Finding `
    -Severity 'High' `
    -EvidenceClass 'Partial' `
    -Category 'privacy' `
    -Guideline '5.1.1(v)' `
    -Evidence ("{0}:{1} suggests account creation or account-based auth; no account deletion signal was found." -f $accountCreationHit.File, $accountCreationHit.Line) `
    -Reason 'Apple expects account-based apps that support account creation to let users initiate account deletion in the app.' `
    -Fix 'Add an in-app deletion path or confirm that the app does not create a user account covered by guideline 5.1.1(v).' `
    -Score 9
}

$externalPaymentHit = Find-FirstHit -Docs $documents -Patterns @(
  'Stripe',
  'PaymentSheet',
  'STPAPIClient',
  'PayPal',
  'Braintree',
  'checkoutSession',
  'subscribeUrl',
  'purchaseUrl'
)
$iapHit = Find-FirstHit -Docs $documents -Patterns @(
  'StoreKit',
  'SKPaymentQueue',
  'Product.purchase',
  'Transaction.currentEntitlements',
  'in_app_purchase',
  'flutter_inapp_purchase',
  'react-native-iap',
  'RevenueCat',
  'Purchases.configure'
)

if ($externalPaymentHit -and -not $iapHit) {
  Add-Finding `
    -Severity 'High' `
    -EvidenceClass 'Partial' `
    -Category 'payments' `
    -Guideline '3.1.1' `
    -Evidence ("{0}:{1} references {2}; no StoreKit/IAP implementation signal was found." -f $externalPaymentHit.File, $externalPaymentHit.Line, $externalPaymentHit.Pattern) `
    -Reason 'If this flow sells digital goods, subscriptions, or feature unlocks, Apple expects in-app purchase unless a narrow exception applies.' `
    -Fix 'Confirm whether the flow sells digital goods. If yes, move it to StoreKit; if no, document the applicable guideline exception.' `
    -Score 9
}

$applePayHit = Find-FirstHit -Docs $documents -Patterns @(
  'PKPaymentAuthorizationController',
  'PKPaymentButton',
  'ApplePay'
)

if ($applePayHit) {
  Add-Finding `
    -Severity 'Low' `
    -EvidenceClass 'Manual' `
    -Category 'payments' `
    -Guideline '4.9' `
    -Evidence ("{0}:{1} references {2}." -f $applePayHit.File, $applePayHit.Line, $applePayHit.Pattern) `
    -Reason 'Apple Pay flows must disclose material purchase details and, for recurring charges, renewal and cancellation terms.' `
    -Fix 'Manually verify Apple Pay disclosure copy, recurring billing language, and branding conformance.' `
    -Score 3
}

$trackingSdkHit = Find-FirstHit -Docs $documents -Patterns @(
  'GoogleMobileAds',
  'GADMobileAds',
  'AppLovin',
  'AppsFlyer',
  'Adjust',
  'FBSDKCoreKit',
  'TikTokBusinessSDK'
)
$attApiHit = Find-FirstHit -Docs $documents -Patterns @(
  'ATTrackingManager',
  'AppTrackingTransparency'
)
$attPurposeValues = @($plistKeyValues['NSUserTrackingUsageDescription'])

if ($attApiHit -and ($attPurposeValues.Count -eq 0)) {
  Add-Finding `
    -Severity 'High' `
    -EvidenceClass 'Code-verifiable' `
    -Category 'tracking' `
    -Guideline '5.1.2(i)' `
    -Evidence ("{0}:{1} references {2}; NSUserTrackingUsageDescription is missing." -f $attApiHit.File, $attApiHit.Line, $attApiHit.Pattern) `
    -Reason 'Apps that invoke ATT APIs still need the matching Info.plist usage description to explain the tracking request to users.' `
    -Fix 'Add a concrete NSUserTrackingUsageDescription value before requesting tracking authorization.' `
    -Score 9
}

if ($trackingSdkHit -and ($attPurposeValues.Count -eq 0) -and -not $attApiHit) {
  Add-Finding `
    -Severity 'High' `
    -EvidenceClass 'Partial' `
    -Category 'tracking' `
    -Guideline '5.1.2(i), 2.5.18' `
    -Evidence ("{0}:{1} references {2}; no ATT API or NSUserTrackingUsageDescription signal was found." -f $trackingSdkHit.File, $trackingSdkHit.Line, $trackingSdkHit.Pattern) `
    -Reason 'Ad and tracking SDKs commonly require ATT posture review, user consent, and tighter scrutiny around targeted advertising.' `
    -Fix 'Confirm whether the SDKs perform tracking. If they do, add ATT handling and disclosure; if not, document the non-tracking configuration.' `
    -Score 8
}

$weakAttValue = $attPurposeValues | Where-Object { Test-PlaceholderString -Value $_.Value } | Select-Object -First 1
if ($weakAttValue) {
  Add-Finding `
    -Severity 'Medium' `
    -EvidenceClass 'Code-verifiable' `
    -Category 'tracking' `
    -Guideline '5.1.2(i)' `
    -Evidence ("{0} contains a weak or placeholder NSUserTrackingUsageDescription value." -f $weakAttValue.File) `
    -Reason 'ATT prompts need clear, user-facing purpose copy. Boilerplate or placeholder text weakens review trust.' `
    -Fix 'Replace the ATT purpose string with a concrete explanation of why tracking is requested.' `
    -Score 6
}

if ($privacyManifestDocs.Count -gt 0) {
  $manifestKeyHit = Find-FirstHit -Docs $privacyManifestDocs -Patterns @(
    'NSPrivacyTracking',
    'NSPrivacyCollectedDataTypes',
    'NSPrivacyAccessedAPITypes'
  )

  if (-not $manifestKeyHit) {
    $manifestDoc = $privacyManifestDocs | Select-Object -First 1
    Add-Finding `
      -Severity 'Low' `
      -EvidenceClass 'Code-verifiable' `
      -Category 'privacy' `
      -Guideline '5.1.1, 5.1.2' `
      -Evidence ("{0} is a privacy manifest file, but it does not contain the common NSPrivacy manifest keys." -f $manifestDoc.RelativePath) `
      -Reason 'The skill promises privacy-manifest coverage, so manifest files should at least expose the standard Apple privacy manifest structure.' `
      -Fix 'Confirm the `.xcprivacy` file is intentional and includes the relevant NSPrivacy keys for collected data, accessed APIs, and tracking posture.' `
      -Score 4
  }
}

if ($backgroundModes.Count -gt 0) {
  $firstMode = $backgroundModes | Select-Object -First 1
  $modeList = ($backgroundModes | Select-Object -ExpandProperty Mode | Sort-Object -Unique) -join ', '
  Add-Finding `
    -Severity 'Medium' `
    -EvidenceClass 'Manual' `
    -Category 'runtime' `
    -Guideline '2.5.4' `
    -Evidence ("{0} declares UIBackgroundModes: {1}." -f $firstMode.File, $modeList) `
    -Reason 'Background execution is allowed only for intended use cases, and Apple often asks whether the chosen modes are justified by core functionality.' `
    -Fix 'Keep only the modes the app genuinely needs and be ready to justify them in review notes.' `
    -Score 5
}

$privateApiHit = Find-FirstHit -Docs $documents -Patterns @(
  'PrivateFrameworks',
  '/System/Library/PrivateFrameworks'
)

if ($privateApiHit) {
  Add-Finding `
    -Severity 'High' `
    -EvidenceClass 'Code-verifiable' `
    -Category 'apis' `
    -Guideline '2.5.1' `
    -Evidence ("{0}:{1} references {2}." -f $privateApiHit.File, $privateApiHit.Line, $privateApiHit.Pattern) `
    -Reason 'Private framework usage is a direct App Review risk because Apple requires public APIs only.' `
    -Fix 'Remove the private framework dependency and replace it with a public API path.' `
    -Score 10
}

$dynamicCodeHit = Find-FirstHit -Docs $documents -Patterns @(
  'react-native-code-push',
  'CodePush.bundleURL',
  'ShorebirdUpdater'
)

if ($dynamicCodeHit) {
  Add-Finding `
    -Severity 'High' `
    -EvidenceClass 'Partial' `
    -Category 'runtime' `
    -Guideline '2.5.2, 4.7' `
    -Evidence ("{0}:{1} references {2}." -f $dynamicCodeHit.File, $dynamicCodeHit.Line, $dynamicCodeHit.Pattern) `
    -Reason 'Post-review code or feature swapping can create App Review risk if it changes app functionality outside the reviewed binary.' `
    -Fix 'Confirm the update path does not download executable code that changes features, or move the change into the shipped binary.' `
    -Score 8
}

$webViewHit = Find-FirstHit -Docs $documents -Patterns @(
  'WKWebView',
  'react-native-webview',
  'webview_flutter',
  'flutter_inappwebview'
)
$uiFileCount = @(
  $documents | Where-Object {
    $_.RelativePath -match '(?i)(view|screen|page|widget|storyboard|xib|contentview|swiftui|route|tab)'
  }
).Count

if ($webViewHit -and $uiFileCount -le 4) {
  Add-Finding `
    -Severity 'Medium' `
    -EvidenceClass 'Partial' `
    -Category 'hig' `
    -Guideline '4.2, HIG' `
    -Evidence ("{0}:{1} references {2}; the repo exposes only {3} obvious UI files." -f $webViewHit.File, $webViewHit.Line, $webViewHit.Pattern, $uiFileCount) `
    -Reason 'A WebView-heavy shell can trigger minimum-functionality questions if the app feels like a wrapped site rather than a native Apple experience.' `
    -Fix 'Confirm the app adds meaningful native value, workflows, and platform-appropriate UX beyond simply rendering web content.' `
    -Score 6
}

$recordingHit = Find-FirstHit -Docs $documents -Patterns @(
  'ReplayKit',
  'RPScreenRecorder',
  'startCapture',
  'startRecording'
)

if ($recordingHit) {
  Add-Finding `
    -Severity 'Medium' `
    -EvidenceClass 'Manual' `
    -Category 'privacy' `
    -Guideline '2.5.14' `
    -Evidence ("{0}:{1} references {2}." -f $recordingHit.File, $recordingHit.Line, $recordingHit.Pattern) `
    -Reason 'Recording user activity requires explicit consent plus a clear visual and/or audible indication while capture is active.' `
    -Fix 'Manually verify the capture UX includes consent, disclosure, and an obvious active-recording indicator.' `
    -Score 5
}

$placeholderHit = Find-FirstHit -Docs @($documents | Where-Object { $_.Extension -in @('.swift', '.dart', '.tsx', '.jsx', '.storyboard', '.xib') }) -Patterns @(
  'Coming Soon',
  'Lorem ipsum',
  'sample@example.com',
  'test@example.com',
  'example.com',
  'changeme'
)

if ($placeholderHit) {
  Add-Finding `
    -Severity 'Medium' `
    -EvidenceClass 'Partial' `
    -Category 'completeness' `
    -Guideline '2.1' `
    -Evidence ("{0}:{1} contains placeholder-style content ({2})." -f $placeholderHit.File, $placeholderHit.Line, $placeholderHit.Pattern) `
    -Reason 'Apple frequently rejects incomplete submissions with obvious placeholder content or unfinished review surfaces.' `
    -Fix 'Replace the placeholder content or confirm it cannot appear in production/review builds.' `
    -Score 5
}

$orderedFindings = @(
  $findings |
    Sort-Object @{ Expression = 'Score'; Descending = $true }, @{ Expression = 'Severity'; Descending = $true } |
    Select-Object -First $Top
)

if ($Json) {
  [pscustomobject]@{
    Notes    = @($notes)
    Findings = @($orderedFindings)
  } | ConvertTo-Json -Depth 6
  exit 0
}

if ($notes.Count -gt 0) {
  Write-Output 'Scanner notes:'
  foreach ($note in $notes) {
    Write-Output ("- {0}" -f $note)
  }
  Write-Output ''
}

if (-not $orderedFindings -or $orderedFindings.Count -eq 0) {
  Write-Output 'Apple guideline scan found no obvious hotspots in the selected files.'
  exit 0
}

Write-Output 'Apple guideline hotspots:'
foreach ($finding in $orderedFindings) {
  Write-Output ''
  Write-Output ("[{0}] [{1}] [{2}] {3}" -f $finding.Severity, $finding.EvidenceClass, $finding.Guideline, $finding.Category)
  Write-Output ("  Evidence: {0}" -f $finding.Evidence)
  Write-Output ("  Why: {0}" -f $finding.Reason)
  Write-Output ("  Fix: {0}" -f $finding.Fix)
}
