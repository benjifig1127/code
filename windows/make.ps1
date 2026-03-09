# Compile all .cpp files in the current directory

$gpp = "C:\msys64\mingw64\bin\g++.exe"

if (-not (Test-Path $gpp)) {
    Write-Error "g++ not found at $gpp. Update the path in the script."
    exit 1
}

$cppFiles = Get-ChildItem -Path . -Filter *.cpp

if ($cppFiles.Count -eq 0) {
    Write-Host "No .cpp files found in the current folder."
    exit 0
}

foreach ($file in $cppFiles) {
    $exeName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name) + ".exe"

    Write-Host "Compiling $($file.Name) -> $exeName ..."
    & $gpp -O3 -Wall -Wextra -Wpedantic -Werror $file.FullName -o $exeName

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Compilation failed for $($file.Name)."
    }
}