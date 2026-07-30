#!/usr/bin/env bash
#
# install-docker.sh
# Instala Docker Engine + docker-compose-plugin desde el repositorio oficial
# de Docker en Ubuntu, removiendo antes cualquier instalación previa vía
# docker.io (repos de Ubuntu) que pueda generar conflictos.
#
# Uso: chmod +x install-docker.sh && ./install-docker.sh

set -euo pipefail

echo "==> Removiendo instalaciones previas de Docker (docker.io, si existen)..."
sudo apt remove -y docker.io docker-compose docker-doc podman-docker containerd runc 2>/dev/null || true

echo "==> Actualizando índice de paquetes..."
sudo apt update

echo "==> Instalando dependencias (ca-certificates, curl, gnupg)..."
sudo apt install -y ca-certificates curl gnupg

echo "==> Agregando la clave GPG oficial de Docker..."
sudo install -m 0755 -d /etc/apt/keyrings
if [ ! -f /etc/apt/keyrings/docker.gpg ]; then
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  sudo chmod a+r /etc/apt/keyrings/docker.gpg
else
  echo "    (ya existe, se omite)"
fi

echo "==> Agregando el repositorio de Docker a las fuentes de apt..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "==> Actualizando índice de paquetes (con el nuevo repo)..."
sudo apt update

echo "==> Instalando Docker Engine, CLI, containerd, buildx y compose plugin..."
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "==> Agregando tu usuario al grupo 'docker' (para no necesitar sudo)..."
sudo usermod -aG docker "$USER"

echo ""
echo "==> Verificación:"
docker --version
docker compose version

echo ""
echo "Listo. Cerrá sesión y volvé a entrar (o corré 'newgrp docker') para poder"
echo "usar 'docker' sin sudo."