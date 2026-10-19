#!/usr/bin/env bash

# TEJ Linux Mint Cinnamon appearance lab
# Changes a small set of current-user Cinnamon settings. It never uses sudo.

set -u

BACKUP_ROOT="${HOME}/.config/tej-cinnamon-style-backups"
LATEST_FILE="${BACKUP_ROOT}/latest"

fail() {
  printf '%s\n' "Error: $*" >&2
  exit 1
}

has_schema() {
  gsettings list-schemas | grep -Fxq "$1"
}

has_key() {
  gsettings list-keys "$1" 2>/dev/null | grep -Fxq "$2"
}

get_setting() {
  gsettings get "$1" "$2"
}

save_setting() {
  schema="$1"
  key="$2"
  filename="$3"
  if has_schema "${schema}" && has_key "${schema}" "${key}"; then
    get_setting "${schema}" "${key}" > "${ACTIVE_BACKUP}/${filename}"
  fi
}

restore_setting() {
  backup_dir="$1"
  schema="$2"
  key="$3"
  filename="$4"
  if [ -f "${backup_dir}/${filename}" ]; then
    value="$(cat "${backup_dir}/${filename}")"
    gsettings set "${schema}" "${key}" "${value}" || return 1
  fi
}

show_setting() {
  label="$1"
  schema="$2"
  key="$3"
  if has_schema "${schema}" && has_key "${schema}" "${key}"; then
    printf '  %-22s %s\n' "${label}:" "$(get_setting "${schema}" "${key}")"
  else
    printf '  %-22s %s\n' "${label}:" "not available"
  fi
}

panel_record() {
  get_setting org.cinnamon panels-enabled \
    | grep -oE '[0-9]+:[0-9]+:(top|bottom)' \
    | head -n 1
}

check_single_panel() {
  records="$(get_setting org.cinnamon panels-enabled | grep -oE '[0-9]+:[0-9]+:(top|bottom)' || true)"
  count="$(printf '%s\n' "${records}" | sed '/^$/d' | wc -l | tr -d ' ')"
  if [ "${count}" != "1" ]; then
    fail "This safe classroom version requires exactly one Cinnamon panel. Use System Settings > Panel instead."
  fi
}

show_current_settings() {
  printf '%s\n' "Current Cinnamon settings:"
  show_setting "Panel position" org.cinnamon panels-enabled
  show_setting "Panel height" org.cinnamon panels-height
  show_setting "Panel auto-hide" org.cinnamon panels-autohide
  show_setting "Window buttons" org.cinnamon.desktop.wm.preferences button-layout
  show_setting "Window theme" org.cinnamon.desktop.wm.preferences theme
  show_setting "Application theme" org.cinnamon.desktop.interface gtk-theme
  show_setting "Icon theme" org.cinnamon.desktop.interface icon-theme
  show_setting "Cinnamon theme" org.cinnamon.theme name
}

create_backup() {
  stamp="$(date +%Y%m%d-%H%M%S)"
  ACTIVE_BACKUP="${BACKUP_ROOT}/${stamp}"
  mkdir -p "${ACTIVE_BACKUP}"

  save_setting org.cinnamon panels-enabled panels-enabled.txt
  save_setting org.cinnamon panels-height panels-height.txt
  save_setting org.cinnamon panels-autohide panels-autohide.txt
  save_setting org.cinnamon.desktop.wm.preferences button-layout button-layout.txt
  save_setting org.cinnamon.desktop.wm.preferences theme window-theme.txt
  save_setting org.cinnamon.desktop.interface gtk-theme gtk-theme.txt
  save_setting org.cinnamon.desktop.interface icon-theme icon-theme.txt
  save_setting org.cinnamon.theme name cinnamon-theme.txt

  printf '%s\n' "${ACTIVE_BACKUP}" > "${LATEST_FILE}"
  printf '%s\n' "Backup saved in ${ACTIVE_BACKUP}"
}

restore_from_dir() {
  backup_dir="$1"
  [ -d "${backup_dir}" ] || fail "Backup folder not found: ${backup_dir}"

  restore_setting "${backup_dir}" org.cinnamon panels-enabled panels-enabled.txt || return 1
  restore_setting "${backup_dir}" org.cinnamon panels-height panels-height.txt || return 1
  restore_setting "${backup_dir}" org.cinnamon panels-autohide panels-autohide.txt || return 1
  restore_setting "${backup_dir}" org.cinnamon.desktop.wm.preferences button-layout button-layout.txt || return 1
  restore_setting "${backup_dir}" org.cinnamon.desktop.wm.preferences theme window-theme.txt || return 1
  restore_setting "${backup_dir}" org.cinnamon.desktop.interface gtk-theme gtk-theme.txt || return 1
  restore_setting "${backup_dir}" org.cinnamon.desktop.interface icon-theme icon-theme.txt || return 1
  restore_setting "${backup_dir}" org.cinnamon.theme name cinnamon-theme.txt || return 1

  printf '%s\n' "Settings restored. Log out and back in if every visual change does not appear immediately."
}

theme_exists() {
  theme_name="$1"
  [ -d "/usr/share/themes/${theme_name}" ] || [ -d "${HOME}/.themes/${theme_name}" ]
}

icon_theme_exists() {
  theme_name="$1"
  [ -d "/usr/share/icons/${theme_name}" ] || [ -d "${HOME}/.icons/${theme_name}" ]
}

apply_setting() {
  schema="$1"
  key="$2"
  value="$3"
  if ! gsettings writable "${schema}" "${key}" >/dev/null 2>&1; then
    printf '%s\n' "Cannot write ${schema} ${key}." >&2
    return 1
  fi
  gsettings set "${schema}" "${key}" "${value}"
}

preview_preset() {
  preset="$1"
  panel_position="$2"
  panel_height="$3"
  panel_autohide="$4"
  button_layout="$5"
  theme_name="$6"

  record="$(panel_record)"
  panel_id="${record%%:*}"
  remainder="${record#*:}"
  monitor_id="${remainder%%:*}"

  printf '%s\n' ""
  printf '%s\n' "Preview only. No settings have changed yet."
  printf '  Preset:             %s\n' "${preset}"
  printf '  Panel position:     %s\n' "${panel_position}"
  printf '  Panel height:       %s pixels\n' "${panel_height}"
  printf '  Panel auto-hide:    %s\n' "${panel_autohide}"
  printf '  Window buttons:     %s\n' "${button_layout}"
  printf '  Built-in theme:     %s, if installed\n' "${theme_name}"
  printf '%s\n' "A restore point will be created before these changes are applied."
  printf 'Type APPLY to continue, or press Enter to cancel: '
  read -r confirmation
  [ "${confirmation}" = "APPLY" ] || {
    printf '%s\n' "Cancelled. Nothing changed."
    return 0
  }

  create_backup
  failed=0
  apply_setting org.cinnamon panels-enabled "['${panel_id}:${monitor_id}:${panel_position}']" || failed=1
  apply_setting org.cinnamon panels-height "['${panel_id}:${panel_height}']" || failed=1
  apply_setting org.cinnamon panels-autohide "['${panel_id}:${panel_autohide}']" || failed=1
  apply_setting org.cinnamon.desktop.wm.preferences button-layout "'${button_layout}'" || failed=1

  if theme_exists "${theme_name}"; then
    apply_setting org.cinnamon.desktop.wm.preferences theme "'${theme_name}'" || failed=1
    apply_setting org.cinnamon.desktop.interface gtk-theme "'${theme_name}'" || failed=1
    apply_setting org.cinnamon.theme name "'${theme_name}'" || failed=1
  else
    printf '%s\n' "Theme ${theme_name} is not installed, so the current theme was kept."
  fi

  if icon_theme_exists Mint-Y; then
    apply_setting org.cinnamon.desktop.interface icon-theme "'Mint-Y'" || failed=1
  fi

  if [ "${failed}" -ne 0 ]; then
    printf '%s\n' "A setting failed. Restoring the backup now."
    restore_from_dir "${ACTIVE_BACKUP}" || fail "Automatic restore also failed. Open System Settings and ask for help."
    exit 1
  fi

  printf '%s\n' "Applied ${preset}. Check the menu, network, sound, and clock before continuing."
  printf '%s\n' "Choose Restore from the menu if you want to undo the preset."
}

restore_latest() {
  [ -f "${LATEST_FILE}" ] || fail "No course-script backup was found."
  backup_dir="$(cat "${LATEST_FILE}")"
  case "${backup_dir}" in
    "${BACKUP_ROOT}"/*) ;;
    *) fail "The saved backup path is invalid." ;;
  esac
  printf '%s\n' "The following backup will be restored:"
  printf '  %s\n' "${backup_dir}"
  printf 'Type RESTORE to continue, or press Enter to cancel: '
  read -r confirmation
  [ "${confirmation}" = "RESTORE" ] || {
    printf '%s\n' "Cancelled. Nothing changed."
    return 0
  }
  restore_from_dir "${backup_dir}" || fail "Restore failed. Open System Settings and ask for help."
}

command -v gsettings >/dev/null 2>&1 || fail "The gsettings command is unavailable."

desktop_name="${XDG_CURRENT_DESKTOP:-}"
case "${desktop_name}" in
  *Cinnamon*|*cinnamon*) ;;
  *) fail "Cinnamon was not detected. Use the Xfce script only on Linux Mint Xfce." ;;
esac

for required_schema in \
  org.cinnamon \
  org.cinnamon.desktop.interface \
  org.cinnamon.desktop.wm.preferences \
  org.cinnamon.theme
do
  has_schema "${required_schema}" || fail "Required Cinnamon schema is missing: ${required_schema}"
done

for required_key in panels-enabled panels-height panels-autohide
do
  has_key org.cinnamon "${required_key}" || fail "Required Cinnamon setting is missing: ${required_key}"
done

mkdir -p "${BACKUP_ROOT}"
check_single_panel

printf '%s\n' "TEJ Linux Mint Cinnamon appearance lab"
printf '%s\n' "Desktop: ${desktop_name}"
if command -v cinnamon >/dev/null 2>&1; then
  printf '%s\n' "Version: $(cinnamon --version 2>/dev/null || printf 'unknown')"
fi
printf '%s\n' ""
printf '%s\n' "1. Preview Windows-style: larger bottom panel and right-side window buttons"
printf '%s\n' "2. Preview Mac-inspired: top panel, left-side window buttons, and dark styling"
printf '%s\n' "3. Show current Cinnamon settings"
printf '%s\n' "4. Restore the most recent course-script backup"
printf '%s\n' "5. Quit"
printf 'Choose 1, 2, 3, 4, or 5: '
read -r choice

case "${choice}" in
  1) preview_preset "Windows-style" bottom 48 false 'menu:minimize,maximize,close' Mint-Y ;;
  2) preview_preset "Mac-inspired" top 44 false 'close,minimize,maximize:menu' Mint-Y-Dark ;;
  3) show_current_settings ;;
  4) restore_latest ;;
  5) exit 0 ;;
  *) fail "That was not one of the choices. Nothing changed." ;;
esac
