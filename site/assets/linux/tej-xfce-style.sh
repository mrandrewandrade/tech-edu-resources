#!/usr/bin/env bash

# TEJ Linux Mint Xfce appearance lab
# Changes only the current user's Xfce settings. It never uses sudo.

set -u

CONFIG_DIR="${HOME}/.config"
CONFIG_FILE="${CONFIG_DIR}/tej-xfce-style.conf"
BACKUP_ROOT="${CONFIG_DIR}/tej-xfce-backups"

if ! command -v xfconf-query >/dev/null 2>&1; then
  printf '%s\n' "This activity requires an Xfce desktop, such as Linux Mint Xfce."
  exit 1
fi

desktop_name="${XDG_CURRENT_DESKTOP:-}"
case "${desktop_name}" in
  *XFCE*|*Xfce*|*xfce*) ;;
  *)
    printf '%s\n' "Xfce was not detected. Open this script from a Linux Mint Xfce desktop."
    exit 1
    ;;
esac

mkdir -p "${CONFIG_DIR}" "${BACKUP_ROOT}"

write_config() {
  preset_name="$1"
  panel_position="$2"
  panel_length="$3"
  panel_size="$4"
  panel_icon_size="$5"
  desktop_icon_size="$6"
  autohide_behavior="$7"
  window_button_layout="$8"

  cat > "${CONFIG_FILE}" <<EOF
# TEJ Xfce appearance values
# Edit the numbers, save the file, rerun the script, and choose option 3.
# Safe ranges: panel length 40-100, panel size 24-80,
# panel icon size 16-64, and desktop icon size 24-128.
# AUTOHIDE_BEHAVIOR: 0 = never, 1 = intelligently, 2 = always.
STYLE_NAME=${preset_name}
PANEL_POSITION=${panel_position}
PANEL_LENGTH=${panel_length}
PANEL_SIZE=${panel_size}
PANEL_ICON_SIZE=${panel_icon_size}
DESKTOP_ICON_SIZE=${desktop_icon_size}
AUTOHIDE_BEHAVIOR=${autohide_behavior}
WINDOW_BUTTON_LAYOUT=${window_button_layout}
EOF
}

get_panel_id() {
  xfconf-query -c xfce4-panel -p /panels 2>/dev/null | awk '/^[0-9]+$/ { print; exit }'
}

read_setting() {
  channel="$1"
  property="$2"
  fallback="$3"
  value="$(xfconf-query -c "${channel}" -p "${property}" 2>/dev/null || true)"
  if [ -n "${value}" ]; then
    printf '%s' "${value}"
  else
    printf '%s' "${fallback}"
  fi
}

show_current_settings() {
  panel_id="$(get_panel_id)"
  if [ -z "${panel_id}" ]; then
    printf '%s\n' "No Xfce panel was found. Ask your teacher for help."
    exit 1
  fi

  panel_path="/panels/panel-${panel_id}"
  printf '%s\n' "Current Xfce values for panel ${panel_id}:"
  printf '  PANEL_LENGTH=%s (percentage of screen)\n' "$(read_setting xfce4-panel "${panel_path}/length" "not set")"
  printf '  PANEL_SIZE=%s (pixels)\n' "$(read_setting xfce4-panel "${panel_path}/size" "not set")"
  printf '  PANEL_ICON_SIZE=%s (pixels)\n' "$(read_setting xfce4-panel "${panel_path}/icon-size" "automatic")"
  printf '  DESKTOP_ICON_SIZE=%s (pixels)\n' "$(read_setting xfce4-desktop /desktop-icons/icon-size "not set")"
  printf '  AUTOHIDE_BEHAVIOR=%s (0 never, 1 intelligently, 2 always)\n' "$(read_setting xfce4-panel "${panel_path}/autohide-behavior" "not set")"
  printf '  WINDOW_BUTTON_LAYOUT=%s\n' "$(read_setting xfwm4 /general/button_layout "not set")"
  printf '%s\n' ""
  printf '%s\n' "Investigation command:"
  printf '%s\n' "  xfconf-query -c xfce4-panel -p ${panel_path} -l -v"
}

load_config() {
  STYLE_NAME="custom"
  PANEL_POSITION="bottom"
  PANEL_LENGTH="100"
  PANEL_SIZE="48"
  PANEL_ICON_SIZE="30"
  DESKTOP_ICON_SIZE="56"
  AUTOHIDE_BEHAVIOR="0"
  WINDOW_BUTTON_LAYOUT="O|HMC"

  while IFS='=' read -r key value; do
    case "${key}" in
      STYLE_NAME) STYLE_NAME="${value}" ;;
      PANEL_POSITION) PANEL_POSITION="${value}" ;;
      PANEL_LENGTH) PANEL_LENGTH="${value}" ;;
      PANEL_SIZE) PANEL_SIZE="${value}" ;;
      PANEL_ICON_SIZE) PANEL_ICON_SIZE="${value}" ;;
      DESKTOP_ICON_SIZE) DESKTOP_ICON_SIZE="${value}" ;;
      AUTOHIDE_BEHAVIOR) AUTOHIDE_BEHAVIOR="${value}" ;;
      WINDOW_BUTTON_LAYOUT) WINDOW_BUTTON_LAYOUT="${value}" ;;
    esac
  done < "${CONFIG_FILE}"
}

require_number() {
  label="$1"
  value="$2"
  minimum="$3"
  maximum="$4"
  case "${value}" in
    ''|*[!0-9]*)
      printf '%s\n' "${label} must be a whole number."
      exit 1
      ;;
  esac
  if [ "${value}" -lt "${minimum}" ] || [ "${value}" -gt "${maximum}" ]; then
    printf '%s\n' "${label} must be from ${minimum} to ${maximum}."
    exit 1
  fi
}

set_value() {
  channel="$1"
  property="$2"
  value_type="$3"
  value="$4"
  if xfconf-query -c "${channel}" -p "${property}" >/dev/null 2>&1; then
    xfconf-query -c "${channel}" -p "${property}" -s "${value}"
  else
    xfconf-query -c "${channel}" -p "${property}" --create -t "${value_type}" -s "${value}"
  fi
}

backup_settings() {
  stamp="$(date +%Y%m%d-%H%M%S)"
  backup_dir="${BACKUP_ROOT}/${stamp}"
  mkdir -p "${backup_dir}"
  for file_name in xfce4-panel.xml xfce4-desktop.xml xfwm4.xml; do
    source_file="${CONFIG_DIR}/xfce4/xfconf/xfce-perchannel-xml/${file_name}"
    if [ -f "${source_file}" ]; then
      cp "${source_file}" "${backup_dir}/${file_name}"
    fi
  done
  printf '%s\n' "Backup saved in ${backup_dir}"
}

apply_config() {
  load_config
  require_number "PANEL_LENGTH" "${PANEL_LENGTH}" 40 100
  require_number "PANEL_SIZE" "${PANEL_SIZE}" 24 80
  require_number "PANEL_ICON_SIZE" "${PANEL_ICON_SIZE}" 16 64
  require_number "DESKTOP_ICON_SIZE" "${DESKTOP_ICON_SIZE}" 24 128
  require_number "AUTOHIDE_BEHAVIOR" "${AUTOHIDE_BEHAVIOR}" 0 2

  case "${PANEL_POSITION}" in
    top) position_value="p=9;x=0;y=0" ;;
    bottom) position_value="p=10;x=0;y=0" ;;
    *)
      printf '%s\n' "PANEL_POSITION must be top or bottom."
      exit 1
      ;;
  esac

  panel_id="$(get_panel_id)"
  if [ -z "${panel_id}" ]; then
    printf '%s\n' "No Xfce panel was found. Ask your teacher for help."
    exit 1
  fi

  backup_settings
  panel_path="/panels/panel-${panel_id}"
  set_value xfce4-panel "${panel_path}/position" string "${position_value}"
  set_value xfce4-panel "${panel_path}/length" uint "${PANEL_LENGTH}"
  set_value xfce4-panel "${panel_path}/length-adjust" bool false
  set_value xfce4-panel "${panel_path}/size" uint "${PANEL_SIZE}"
  set_value xfce4-panel "${panel_path}/icon-size" uint "${PANEL_ICON_SIZE}"
  set_value xfce4-panel "${panel_path}/autohide-behavior" uint "${AUTOHIDE_BEHAVIOR}"
  set_value xfce4-panel "${panel_path}/position-locked" bool true
  set_value xfce4-desktop /desktop-icons/icon-size uint "${DESKTOP_ICON_SIZE}"
  set_value xfwm4 /general/button_layout string "${WINDOW_BUTTON_LAYOUT}"

  xfce4-panel -r >/dev/null 2>&1 || true
  printf '%s\n' "Applied ${STYLE_NAME}."
  printf '%s\n' "Edit ${CONFIG_FILE} in a text editor, rerun this script, and choose option 3 to experiment."
}

printf '%s\n' "TEJ Linux Mint Xfce appearance lab"
printf '%s\n' "1. Windows-style: full bottom panel and larger icons"
printf '%s\n' "2. Mac-inspired: centred auto-hiding dock and left window buttons"
printf '%s\n' "3. Apply values from ${CONFIG_FILE}"
printf '%s\n' "4. Show current Xfce values"
printf '%s\n' "5. Quit"
printf 'Choose 1, 2, 3, 4, or 5: '
read -r choice

case "${choice}" in
  1)
    write_config "windows-style" bottom 100 48 30 56 0 'O|HMC'
    apply_config
    ;;
  2)
    write_config "mac-inspired" bottom 78 56 36 64 1 'CHM|O'
    apply_config
    ;;
  3)
    if [ ! -f "${CONFIG_FILE}" ]; then
      write_config "custom" bottom 100 48 30 56 0 'O|HMC'
      printf '%s\n' "Created ${CONFIG_FILE}. Edit it, then run this script again."
      exit 0
    fi
    apply_config
    ;;
  4) show_current_settings ;;
  5) exit 0 ;;
  *)
    printf '%s\n' "That was not one of the choices. Nothing changed."
    exit 1
    ;;
esac
