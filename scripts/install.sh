#!/bin/sh
set -eu

REPO="tacosandtypescript-debug/SpaceFlow"
APP_DIR="${SPACEFLOW_HOME:-$HOME/.local/share/spaceflow}"

if [ -n "${TERMUX_VERSION:-}" ] || echo "${PREFIX:-}" | grep -q 'com.termux'; then
    PLATFORM="termux"
    pkg install -y python ffmpeg curl
    BIN_DIR="$HOME/.local/bin"
elif [ -d "$HOME/Documents" ]; then
    PLATFORM="ashell"
    pkg install ffmpeg
    BIN_DIR="$HOME/Documents/bin"
    APP_DIR="${SPACEFLOW_HOME:-$HOME/Documents/.spaceflow/app}"
else
    PLATFORM="unix"
    BIN_DIR="$HOME/.local/bin"
fi

PYTHON="$(command -v python3 || command -v python || true)"
if [ -z "$PYTHON" ]; then
    echo "No se encontró Python 3." >&2
    exit 1
fi

"$PYTHON" -m pip install --user --upgrade yt-dlp
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
echo "Ejecuta: spaceflow auth import /ruta/cookies.txt"
