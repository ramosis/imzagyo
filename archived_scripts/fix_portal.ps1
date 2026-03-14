
$content = Get-Content portal.html
$keep_start = $content[0..2681]
$keep_end = $content[6057..($content.Length-1)]
$new_content = $keep_start + $keep_end
$new_content | Set-Content portal.html
