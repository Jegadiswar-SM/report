#!/usr/bin/env bash
set -u
PKG="$(cd "$(dirname "$0")/.." && pwd)"
ROOT="$(cd "$PKG/../.." && pwd)"
printf 'PULSAR-4X Review 02 launcher\nProject: %s\n' "$ROOT"
if [[ -z "${DISPLAY:-}" ]]; then
  echo 'GUI unavailable: DISPLAY is unset.'
  GUI_OK=0
elif command -v xdpyinfo >/dev/null 2>&1 && xdpyinfo >/dev/null 2>&1; then
  echo "GUI display reachable: ${DISPLAY}"
  GUI_OK=1
else
  echo "GUI unavailable: cannot connect to DISPLAY ${DISPLAY}. No GUI will be launched."
  GUI_OK=0
fi
VIRTUOSO="$(command -v virtuoso 2>/dev/null || true)"
SIMVISION="$(command -v simvision 2>/dev/null || true)"
GENUS="$(command -v genus 2>/dev/null || true)"
[[ -x "$VIRTUOSO" ]] || VIRTUOSO="/home/install/IC618/tools.lnx86/dfII/bin/virtuoso"
[[ -x "$SIMVISION" ]] || SIMVISION="/home/install/SSV221/tools.lnx86/simvision/bin/simvision"
[[ -x "$GENUS" ]] || GENUS="/home/install/DDI221/GENUS221/bin/genus"
for pair in "virtuoso:$VIRTUOSO" "simvision:$SIMVISION" "genus:$GENUS"; do
  name="${pair%%:*}"; path="${pair#*:}"
  if [[ -x "$path" ]]; then printf '%s: %s\n' "$name" "$path"; else printf '%s: executable unavailable\n' "$name"; fi
done
if [[ -n "${CDS_LIC_FILE:-${LM_LICENSE_FILE:-}}" ]]; then
  echo 'Cadence license variable is configured (value hidden).'
else
  echo 'Cadence license variable is not configured in this shell; GUI licensing may fail.'
fi
printf '\nOffline evidence:\n'
printf '  %s\n' "$PKG/report/PULSAR4X_REVIEW_02.md" "$PKG/index.html" "$PKG/slides/review_slides.html"
printf '  Saved Genus reports: %s\n' "$ROOT/results/digital/channel_wrapper_20261013/timing.rpt"
printf '  Saved AMS logs: %s\n' "$ROOT/results/raw/first_integrated_adc_capture/cases"
if [[ "$GUI_OK" != 1 ]]; then
  echo 'No GUI launch attempted. Use the package README manual procedure on an authorized desktop.'
  exit 0
fi
if [[ -x "$VIRTUOSO" ]]; then
  if pgrep -u "$(id -u)" -x virtuoso >/dev/null 2>&1; then
    echo 'Virtuoso already runs under this user; leaving it untouched. Open the cells through Library Manager.'
  elif [[ "${PULSAR_LAUNCH_VIRTUOSO:-0}" == 1 ]]; then
    echo 'Launching Virtuoso with the existing project cds.lib; no design files will be edited by this launcher.'
    (cd "$ROOT" && "$VIRTUOSO" -log "$PKG/evidence/virtuoso_review.log")
  else
    echo 'Virtuoso is available. To launch it now set PULSAR_LAUNCH_VIRTUOSO=1 and rerun this script.'
  fi
fi
if [[ -x "$SIMVISION" ]]; then
  if [[ -d "$ROOT/results/raw/first_integrated_adc_capture/xcelium.d" ]]; then
    echo 'Xcelium run directory exists, but no verified SimVision database path was packaged; inspect logs and PSF with the saved setup.'
  else
    echo 'No packaged SimVision database found; use saved data-derived plots and logs.'
  fi
fi
if [[ -x "$GENUS" ]]; then echo 'Genus executable is installed; no GUI checkpoint launch command is inferred.'; else echo 'Genus executable unavailable; text reports are preserved.'; fi
