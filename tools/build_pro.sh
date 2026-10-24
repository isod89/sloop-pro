#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-only
# SLOOP Pro: the three SMK-37 packages (SMK-37 Pro, SMK-37 Elite, MKE-P37) into build/release/ with their SHA-256,
# the site with the installer and the editor in build/sloop-pro-site/, then the FM-1 build last (the reference the
# host tests use: tests/run_tests.sh reads build/felucca.*). Linux x86-64 or WSL, as ./build.sh.
#   tools/build_pro.sh [--release X.Y] [--no-fm1]
#   JIELI_TOOLCHAIN, AC79_SDK as for ./build.sh
set -e
cd "$(dirname "$0")/.."
REL="" FM1=1
while [ $# -gt 0 ]; do
    case "$1" in
        --release) REL="$2"; shift 2 ;;
        --no-fm1) FM1=0; shift ;;
        *) echo "tools/build_pro.sh [--release X.Y] [--no-fm1]"; exit 2 ;;
    esac
done
VER=$(sed -n 's/^#define FELUCCA_VERSION "SLOOP PRO \([^"]*\)".*/\1/p' firmware/src/felucca.c | head -1)
[ -n "$REL" ] && VER="$REL"
mkdir -p build/release
for m in pro elite mke; do
    sfx=""; [ "$m" = pro ] || sfx="-$m"
    echo "== SLOOP Pro $VER, MODEL=$m"
    if [ -n "$REL" ]; then
        BOARD=smk37 MODEL=$m FELUCCA_SLICE=0 sh build.sh --release "$REL"
        cp "build/sloop-pro$sfx-$REL.fwsc" "build/release/sloop-pro$sfx.fwsc"
    else
        BOARD=smk37 MODEL=$m FELUCCA_SLICE=0 sh build.sh
        cp "build/sloop-pro$sfx.fwsc" build/release/
    fi
done
(cd build/release && sha256sum sloop-pro.fwsc sloop-pro-elite.fwsc sloop-pro-mke.fwsc | tee SHA256SUMS.txt)
python3 web/make_site.py --pro "$VER" build/sloop-pro-site build/release/sloop-pro.fwsc build/release/sloop-pro-elite.fwsc \
    build/release/sloop-pro-mke.fwsc
if [ "$FM1" = 1 ]; then
    echo "== the FM-1 reference build (for tests/run_tests.sh)"
    FELUCCA_SLICE=0 sh build.sh
fi
echo "packages: build/release/   site: build/sloop-pro-site/ (python3 -m http.server 8767 --directory build/sloop-pro-site)"
