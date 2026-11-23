#!/usr/bin/env bash
# Collect read-only system evidence for teacher review.
# This script does not prove that any expansion-header pin is safe or correctly mapped.

set -u

timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
evidence_dir="${1:-beaglebone-evidence-${timestamp}}"
mkdir -p -- "$evidence_dir"

section() {
  printf '\n## %s\n' "$1"
}

{
  section "Collection time"
  date -u '+%Y-%m-%dT%H:%M:%SZ'

  section "Board model reported by device tree"
  if [ -r /proc/device-tree/model ]; then
    tr -d '\000' < /proc/device-tree/model
    printf '\n'
  else
    printf 'unavailable\n'
  fi

  section "Kernel"
  uname -a

  section "Operating system"
  if [ -r /etc/os-release ]; then
    cat /etc/os-release
  else
    printf 'unavailable\n'
  fi

  section "Python"
  if command -v python3 >/dev/null 2>&1; then
    command -v python3
    python3 --version 2>&1
  else
    printf 'python3 not found\n'
  fi

  section "Beagle version utility"
  if command -v beagle-version >/dev/null 2>&1; then
    beagle-version 2>&1
  else
    printf 'beagle-version not found\n'
  fi
} > "$evidence_dir/system.txt" 2>&1

{
  section "Mounted storage"
  df -hT 2>&1

  section "Block devices"
  if command -v lsblk >/dev/null 2>&1; then
    lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,RO 2>&1
  else
    printf 'lsblk not found\n'
  fi
} > "$evidence_dir/storage.txt" 2>&1

{
  section "libgpiod command-line tools"
  if command -v gpiodetect >/dev/null 2>&1; then
    gpiodetect --version 2>&1 || true
    gpiodetect 2>&1 || true
  else
    printf 'gpiodetect not found\n'
  fi

  section "GPIO line information"
  if command -v gpioinfo >/dev/null 2>&1; then
    gpioinfo 2>&1 || true
  else
    printf 'gpioinfo not found\n'
  fi

  section "Python gpiod binding"
  if command -v python3 >/dev/null 2>&1; then
    python3 -c 'import gpiod; print("module:", gpiod.__file__); print("version:", getattr(gpiod, "__version__", "not reported")); print("request_lines:", hasattr(gpiod, "request_lines"))' 2>&1 || true
  fi
} > "$evidence_dir/gpio.txt" 2>&1

{
  section "Network interface state"
  for interface_path in /sys/class/net/*; do
    [ -e "$interface_path" ] || continue
    interface_name="$(basename "$interface_path")"
    state="unknown"
    if [ -r "$interface_path/operstate" ]; then
      state="$(cat "$interface_path/operstate")"
    fi
    printf '%s,%s\n' "$interface_name" "$state"
  done
  printf '\nAddresses, MAC addresses, Wi-Fi names, and credentials are intentionally not collected.\n'
} > "$evidence_dir/network.txt" 2>&1

{
  section "Linux LED devices"
  if [ -d /sys/class/leds ]; then
    for led_path in /sys/class/leds/*; do
      [ -e "$led_path" ] || continue
      basename "$led_path"
    done
  else
    printf 'no /sys/class/leds directory\n'
  fi

  section "Power-supply class devices"
  if [ -d /sys/class/power_supply ]; then
    for supply_path in /sys/class/power_supply/*; do
      [ -e "$supply_path" ] || continue
      basename "$supply_path"
    done
  else
    printf 'no /sys/class/power_supply directory\n'
  fi
} > "$evidence_dir/devices.txt" 2>&1

cat > "$evidence_dir/READ-ME-FIRST.txt" <<'EOF'
TEACHER REVIEW REQUIRED

This folder contains read-only software evidence. It does not verify:
- the printed board revision or physical condition;
- the power adapter's measured voltage, polarity, or current rating;
- any header pin's physical identity, pinmux, voltage, or safe current;
- external wiring;
- operation of a relay, lamp, horn, LED, button, or sensor.

Do not publish this folder. Review it with the inventory and verified-header-pin
worksheets, then record only approved configuration values in the class files.
EOF

printf 'Evidence written to %s\n' "$evidence_dir"
printf 'No GPIO lines, packages, network settings, or system files were changed.\n'
