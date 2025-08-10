# Sumaq API

## Pasos para lograr la conexión SSH desde Windows con el servidor EC2 y poder aprovisionarlo

Primero asegurar la privacidad de la llave privada:

```bash
icacls "key-pair-sumaq-server.pem" /inheritance:r
icacls "key-pair-sumaq-server.pem" /remove:g "BUILTIN\Administradores" "NT AUTHORITY\SYSTEM" "NT AUTHORITY\Usuarios autentificados" "BUILTIN\Usuarios"
icacls "key-pair-sumaq-server.pem" /grant:r "$($env:USERNAME):(R)"
icacls "key-pair-sumaq-server.pem"
```

Y ya se puede establecer la conexión usando OpenSSH:

```bash
ssh -i "key-pair-sumaq-server.pem" ec2-user@ec2-35-153-170-195.compute-1.amazonaws.com
```

## Aprovisionar EC2

En una consola SSH:

```bash
sudo yum install -y git docker python
```
