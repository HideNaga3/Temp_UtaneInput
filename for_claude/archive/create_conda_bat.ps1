$enc = [System.Text.Encoding]::GetEncoding(932)
$content = [System.IO.File]::ReadAllText('temp_base.bat', $enc)
$content = $content -replace 'pdfが入る', 'input_imgが入る'
$content = $content -replace 'var3にはpdf', 'var3にはinput_img'
$outputPath = 'BA_venvでパッケージ化conda__給与計算検定入力アプリ__試作V1__input_img__ddd.bat'
[System.IO.File]::WriteAllText($outputPath, $content, $enc)
Write-Host "Created: $outputPath"
