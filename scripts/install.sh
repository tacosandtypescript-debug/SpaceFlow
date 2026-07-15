#!/bin/sh
set -eu

REPO="tacosandtypescript-debug/SpaceFlow"
APP_DIR="${SPACEFLOW_HOME:-$HOME/.local/share/spaceflow}"
PYTHON=""

if command -v apk >/dev/null 2>&1 && [ -f /etc/alpine-release ]; then
    PLATFORM="ish"
    MISSING_PACKAGES=""
    for package in python3 py3-pip py3-virtualenv ffmpeg curl ca-certificates; do
        if ! apk info -e "$package" >/dev/null 2>&1; then
            MISSING_PACKAGES="$MISSING_PACKAGES $package"
        fi
    done
    if [ -n "$MISSING_PACKAGES" ]; then
        apk add --no-cache $MISSING_PACKAGES
    else
        echo "Dependencias de iSH ya instaladas; se omite apk."
    fi
    if [ "$(id -u)" = "0" ]; then
        BIN_DIR="/usr/local/bin"
    else
        BIN_DIR="$HOME/.local/bin"
    fi
    mkdir -p "$APP_DIR" "$BIN_DIR"
    VENV_DIR="$APP_DIR/venv"
    if [ ! -x "$VENV_DIR/bin/python" ]; then
        python3 -m virtualenv "$VENV_DIR"
    else
        echo "Entorno Python de SpaceFlow ya instalado."
    fi
    PYTHON="$VENV_DIR/bin/python"
elif [ -n "${TERMUX_VERSION:-}" ] || echo "${PREFIX:-}" | grep -q 'com.termux'; then
    PLATFORM="termux"
    MISSING_PACKAGES=""
    command -v python >/dev/null 2>&1 || MISSING_PACKAGES="$MISSING_PACKAGES python"
    command -v ffmpeg >/dev/null 2>&1 || MISSING_PACKAGES="$MISSING_PACKAGES ffmpeg"
    command -v curl >/dev/null 2>&1 || MISSING_PACKAGES="$MISSING_PACKAGES curl"
    command -v mpv >/dev/null 2>&1 || MISSING_PACKAGES="$MISSING_PACKAGES mpv"
    if [ -n "$MISSING_PACKAGES" ]; then
        pkg install -y $MISSING_PACKAGES
    else
        echo "Dependencias de Termux ya instaladas; se omite pkg."
    fi
    # PREFIX/bin forma parte del PATH de Termux desde la sesión actual.
    # Usar ~/.local/bin aquí obligaba a reiniciar la terminal después de curl | sh.
    BIN_DIR="$PREFIX/bin"
elif { [ -n "${APPNAME:-}" ] && echo "$APPNAME" | grep -qi 'a-shell'; } || \
     { command -v pkg >/dev/null 2>&1 && [ -d "$HOME/Documents" ]; }; then
    PLATFORM="ashell"
    if ! command -v ffmpeg >/dev/null 2>&1; then
        pkg install ffmpeg
    else
        echo "FFmpeg ya está instalado; se omite pkg."
    fi
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

if [ "${SPACEFLOW_UPDATE_DEPS:-0}" = "1" ] || \
   ! "$PYTHON" -c 'import yt_dlp' >/dev/null 2>&1; then
    if [ "$PLATFORM" = "ish" ]; then
        "$PYTHON" -m pip install --upgrade pip yt-dlp
    else
        "$PYTHON" -m pip install --user --upgrade yt-dlp
    fi
else
    echo "yt-dlp ya está instalado; se omite pip."
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
