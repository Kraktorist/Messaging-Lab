# based on https://github.com/RamblingCookieMonster/PSRabbitMq
# https://github.com/RamblingCookieMonster/PSRabbitMq/issues/26
Import-Module PSRabbitMq -ErrorAction Stop
#$cred = Get-Credential
$prms =@{
    ComputerName = 'localhost'
    Exchange = 'message'
    key = 'example.text'
    QueueName = 'text'
    AutoDelete = $false
    Durable = $false
    Credential = $cred
    RequireACK = $true
}
Start-RabbitMqListener @prms | ForEach-Object {
    $req = $_
    Start-Sleep -Seconds 1
    Write-Warning $req
    }