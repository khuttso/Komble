# Sends exactly ONE tiny request to the selected FREE model. No retries, files, or saved answers.
# Run in the same PowerShell terminal where the app's environment variables were set.
$ErrorActionPreference = 'Stop'

function Format-SafeDiagnosticText([object]$Value) {
    $text = [string]$Value
    if (-not [string]::IsNullOrWhiteSpace($env:OPENROUTER_API_KEY)) {
        $text = $text.Replace($env:OPENROUTER_API_KEY.Trim(), '[KEY REDACTED]')
    }
    $text = [regex]::Replace($text, 'sk-[A-Za-z0-9_-]+', '[KEY REDACTED]')
    $text = [regex]::Replace($text, '[\x00-\x1F\x7F]', ' ')
    if ($text.Length -gt 1200) { $text = $text.Substring(0, 1200) + ' [truncated]' }
    return $text
}

if ([string]::IsNullOrWhiteSpace($env:OPENROUTER_API_KEY) -or [string]::IsNullOrWhiteSpace($env:OPENROUTER_MODEL)) {
    Write-Output 'Missing OPENROUTER_API_KEY or OPENROUTER_MODEL in this terminal. Configure them first; do not paste the key into chat.'
    exit 1
}
if (-not $env:OPENROUTER_MODEL.Trim().EndsWith(':free')) {
    Write-Output 'This diagnostic only calls a model whose ID ends in :free. No request was sent.'
    exit 1
}

Add-Type -AssemblyName System.Net.Http
$handler = [System.Net.Http.HttpClientHandler]::new()
$handler.AllowAutoRedirect = $false
$client = [System.Net.Http.HttpClient]::new($handler)
$client.Timeout = [TimeSpan]::FromSeconds(20)
$request = [System.Net.Http.HttpRequestMessage]::new([System.Net.Http.HttpMethod]::Post, 'https://openrouter.ai/api/v1/chat/completions')
$request.Headers.Authorization = [System.Net.Http.Headers.AuthenticationHeaderValue]::new('Bearer', $env:OPENROUTER_API_KEY.Trim())
$payload = @{
    model = $env:OPENROUTER_MODEL.Trim()
    messages = @(@{ role = 'user'; content = 'Reply with the JSON object {"ok":true} only.' })
    response_format = @{ type = 'json_object' }
    max_tokens = 32
    stream = $false
    provider = @{ allow_fallbacks = $false; require_parameters = $true }
} | ConvertTo-Json -Depth 6 -Compress
$request.Content = [System.Net.Http.StringContent]::new($payload, [System.Text.Encoding]::UTF8, 'application/json')
$response = $null

try {
    Write-Output ('Selected model: ' + (Format-SafeDiagnosticText $env:OPENROUTER_MODEL))
    Write-Output 'Sending one tiny diagnostic request. No interview answer is sent.'
    $response = $client.SendAsync($request).GetAwaiter().GetResult()
    Write-Output ('HTTP status: ' + [int]$response.StatusCode)
    foreach ($name in @('Retry-After', 'X-RateLimit-Limit', 'X-RateLimit-Remaining', 'X-RateLimit-Reset')) {
        if ($response.Headers.Contains($name)) {
            Write-Output ($name + ': ' + (Format-SafeDiagnosticText ($response.Headers.GetValues($name) -join ', ')))
        }
    }
    $body = $response.Content.ReadAsStringAsync().GetAwaiter().GetResult()
    try { $data = $body | ConvertFrom-Json } catch {
        Write-Output 'Response was not JSON. Raw response omitted.'
        exit 1
    }
    if ($null -ne $data.error) {
        Write-Output ('Error code: ' + (Format-SafeDiagnosticText $data.error.code))
        Write-Output ('Error message: ' + (Format-SafeDiagnosticText $data.error.message))
        foreach ($field in @('provider_name', 'provider_code', 'error_type', 'limit_source', 'reason')) {
            $value = $data.error.metadata.$field
            if ($null -ne $value) { Write-Output ($field + ': ' + (Format-SafeDiagnosticText $value)) }
        }
        # Inspect only an error message from nested provider JSON, never dump metadata or bodies.
        if ($data.error.metadata.raw -is [string]) {
            try {
                $providerData = $data.error.metadata.raw | ConvertFrom-Json
                $providerMessage = $providerData.error.message
                if ($null -eq $providerMessage) { $providerMessage = $providerData.message }
                if ($null -ne $providerMessage) { Write-Output ('Provider message: ' + (Format-SafeDiagnosticText $providerMessage)) }
            } catch { Write-Output 'Provider supplied non-JSON details; raw details omitted.' }
        }
    } elseif ($response.IsSuccessStatusCode) {
        Write-Output 'The provider accepted this tiny request. This does not verify interview feedback quality.'
        Write-Output ('Finish reason: ' + (Format-SafeDiagnosticText $data.choices[0].finish_reason))
    }
} catch {
    Write-Output ('Diagnostic transport error: ' + (Format-SafeDiagnosticText $_.Exception.Message))
} finally {
    if ($null -ne $response) { $response.Dispose() }
    $request.Dispose()
    $client.Dispose()
}
