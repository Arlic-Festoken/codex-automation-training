$ErrorActionPreference = 'Stop'

$lessonRoot = Split-Path -Parent $PSCommandPath
$configPath = Join-Path $lessonRoot 'ssh_config_example'
$resolved = ssh.exe -F $configPath -G workbench-training

$expected = @{
    hostname = '203.0.113.10'
    user = 'devuser'
    port = '2222'
    identityfile = '~/.ssh/id_ed25519'
}

foreach ($name in $expected.Keys) {
    $line = $resolved | Where-Object { $_ -match "^$name " } | Select-Object -First 1
    if ($line -ne "$name $($expected[$name])") {
        throw "SSH config check failed for $name. Expected '$name $($expected[$name])', got '$line'."
    }
}

Write-Host 'Offline SSH config check passed.'
$resolved | Where-Object { $_ -match '^(hostname|user|port|identityfile) ' }
