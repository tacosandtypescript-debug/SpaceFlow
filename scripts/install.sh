#!/bin/sh
set -eu

REPO="tacosandtypescript-debug/SpaceFlow"
APP_DIR="${SPACEFLOW_HOME:-$HOME/.local/share/spaceflow}"
PYTHON=""

if command -v apk >/dev/null 2>&1 && [ -f /etc/alpine-release ]; then
    PLATFORM="ish"
    apk add --no-cache python3 py3-pip py3-virtualenv ffmpeg curl ca-certificates
    if [ "$(id -u)" = "0" ]; then
        BIN_DIR="/usr/local/bin"
    else
        BIN_DIR="$HOME/.local/bin"
    fi
    mkdir -p "$APP_DIR" "$BIN_DIR"
    VENV_DIR="$APP_DIR/venv"
    python3 -m virtualenv "$VENV_DIR"
    PYTHON="$VENV_DIR/bin/python"
    "$PYTHON" -m pip install --upgrade pip yt-dlp
elif [ -n "${TERMUX_VERSION:-}" ] || echo "${PREFIX:-}" | grep -q 'com.termux'; then
    PLATFORM="termux"
    pkg install -y python ffmpeg curl
    BIN_DIR="$HOME/.local/bin"
elif { [ -n "${APPNAME:-}" ] && echo "$APPNAME" | grep -qi 'a-shell'; } || \
     { command -v pkg >/dev/null 2>&1 && [ -d "$HOME/Documents" ]; }; then
    PLATFORM="ashell"
    pkg install ffmpeg
    BIN_DIR="$HOME/Documents/bin"
    APP_DIR="${SPACEFLOW_HOME:-$HOME/Documents/.spaceflow/app}"
else
    PLATFORM="unix"
    BIN_DIR="$HOME/.local/bin"
fi

if [ -z "$PYTHON" ]; then
    PYTHON="$(command -v python3 || command -v python || true)"
fi
if [ -z "$PYTHON" ]; then
    echo "No se encontró Python 3." >&2
    exit 1
fi

if [ "$PLATFORM" != "ish" ]; then
    "$PYTHON" -m pip install --user --upgrade yt-dlp
fi
mkdir -p "$APP_DIR" "$BIN_DIR"

LATEST="https://github.com/$REPO/releases/latest/download/spaceflow.pyz"
CHECKSUMS="https://github.com/$REPO/releases/latest/download/SHA256SUMS"
curl -fL "$LATEST" -o "$APP_DIR/spaceflow.pyz.new"
curl -fL "$CHECKSUMS" -o "$APP_DIR/SHA256SUMS"

EXPECTED="$(grep 'spaceflow.pyz$' "$APP_DIR/SHA256SUMS" | awk '{print $1}')"
ACTUAL="$($PYTHON -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$APP_DIR/spaceflow.pyz.new")"
if [ -z "$EXPECTED" ] || [ "$EXPECTED" != "$ACTUAL" ]; then
    rm -f "$APP_DIR/spaceflow.pyz.new"
    echo "El checksum de SpaceFlow no coincide." >&2
    exit 1
fi
mv "$APP_DIR/spaceflow.pyz.new" "$APP_DIR/spaceflow.pyz"

cat > "$BIN_DIR/spaceflow" <<EOF
#!/bin/sh
exec "$PYTHON" "$APP_DIR/spaceflow.pyz" "\$@"
EOF
chmod +x "$BIN_DIR/spaceflow"

case ":${PATH}:" in
    *":$BIN_DIR:"*) ;;
    *)
        PROFILE="$HOME/.profile"
        echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$PROFILE"
        export PATH="$BIN_DIR:$PATH"
        ;;
esac

echo "SpaceFlow instalado para $PLATFORM."
echo "Ejecuta: spaceflow"
echo "Las cookies son opcionales y solo hacen falta si X exige iniciar sesión."
