# Bash Boilerplate: https://github.com/alphabetum/bash-boilerplate
#   ${some_array[@]:-}              # blank default value
#   ${some_array[*]:-}              # blank default value
#   ${some_array[0]:-}              # blank default value
#   ${some_array[0]:-default_value} # default value: the string 'default_value'

#   ${1:-alternative}         # default value: the string 'alternative'
#   ${2:-}                    # blank default value
#   ${1:?'error message'}     # exit with 'error message' if variable is unbound
set -u
set -o nounset
set -o errexit
set -o pipefail

DEFAULT_IFS="${IFS}"
SAFER_IFS=$'\n\t'
IFS="${SAFER_IFS}"
DEFAULT_COMMAND="${DEFAULT_COMMAND:-help}"

_LOG_LEVEL="${_LOG_LEVEL:-6}" # 7 = debug -> 0 = emergency
_NO_COLOR="${NO_COLOR:-}"

function _push_log () {
  local _log_level="${1}"
  shift

  local color_debug="\x1b[35m"
  local color_info="\x1b[34m"
  local color_success="\x1b[32m"
  local color_warning="\x1b[33m"
  local color_error="\x1b[31m"
  local color_abort="\x1b[1;31m"

  local msg_debug="DBG"
  local msg_info="INFO"
  local msg_success="SUCCESS"
  local msg_warning="WARN"
  local msg_error="ERROR"
  local msg_abort="ABORT"

  local colorvar="color_${_log_level}"

  local color="${!colorvar:-${color_error}}"
  local color_reset="\x1b[0m"

  local levelvar="msg_${_log_level}"
  local levelname="$(printf "%8s" "${!levelvar:-${msg_error}}")"
  local funcname="\x1b[35m$(printf "%-15s" "${FUNCNAME[2]}")"

  if [[ "${_NO_COLOR:-}" = "true" ]] || [[ "${TERM:-}" != "xterm"* ]] || [[ ! -t 2 ]]; then
    if [[ "${_NO_COLOR:-}" != "false" ]]; then
      # Don't use colors on pipes or non-recognized terminals
      color=""; color_reset=""
    fi
  fi

  # all remaining arguments are to be printed
  local log_line=""

  while IFS=$'\n' read -r log_line; do
    echo -e "${color}${levelname}${color_reset} ${funcname}${color_reset} ${log_line}" 1>&2
  done <<< "${@:-}"
}
function _abort ()   {                                   _push_log abort   "${@}"; exit 1; }
function _error ()   { [[ "${_LOG_LEVEL:-0}" -ge 3 ]] && _push_log error   "${@}"; true; }
function _success () { [[ "${_LOG_LEVEL:-0}" -ge 3 ]] && _push_log success "${@}"; true; }
function _warn ()    { [[ "${_LOG_LEVEL:-0}" -ge 4 ]] && _push_log warning "${@}"; true; }
function _info ()    { [[ "${_LOG_LEVEL:-0}" -ge 6 ]] && _push_log info    "${@}"; true; }
function _debug ()   { [[ "${_LOG_LEVEL:-0}" -ge 7 ]] && _push_log debug   "${@}"; true; }

# Options
# Get raw options for any commands that expect them.
_RAW_OPTIONS="${*:-}"

# Steps:
# 1. set expected short options in `optstring` at beginning of the "Normalize
#    Options" section,
# 2. parse options in while loop in the "Parse Options" section.
# Normalize Options ###########################################################

optstring=h

# Normalize -------------------------------------------------------------------
# iterate over options, breaking -ab into -a -b and --foo=bar into --foo bar
unset options
# while the number of arguments is greater than 0
while ((${#}))
do
  case ${1} in
    # if option is of type -ab
    -[!-]?*)
      # loop over each character starting with the second
      for ((i=1; i<${#1}; i++))
      do
        # extract 1 character from position 'i'
        c=${1:i:1}
        # add current char to options
        options+=("-${c}")

        # if option takes a required argument, and it's not the last char
        # make the rest of the string its argument
        if [[ ${optstring} = *"${c}:"* && ${1:i+1} ]]
        then
          options+=("${1:i+1}")
          break
        fi
      done
      ;;
    # if option is of type --foo=bar, split on first '='
    --?*=*)
      options+=("${1%%=*}" "${1#*=}")
      ;;
    # end of options, stop breaking them up
    --)
      options+=(--endopts)
      shift
      options+=("${@}")
      break
      ;;
    # otherwise, nothing special
    *)
      options+=("${1}")
      ;;
  esac

  shift
done
# set new positional parameters to altered options. Set default to blank.
set -- "${options[@]:-}"
unset options

# Parse Options ###############################################################

# $_COMMAND_ARGV contains all of the arguments that get passed along
_COMMAND_ARGV=("${0}")
_CMD=""
_USE_DEBUG=0

while [[ ${#} -gt 0 ]]; do
  __opt="${1}"
  shift
  case "${__opt}" in
    -h|--help)
      _CMD="help"
      ;;
    --version)
      _CMD="version"
      ;;
    --debug)
      _USE_DEBUG=1
      ;;
    *)
      # The first non-option argument is assumed to be the command name.
      # All subsequent arguments are added to $_COMMAND_ARGV.
      if [[ -n "${_CMD}" ]]; then
        _COMMAND_ARGV+=("${__opt}")
      else
        _CMD="${__opt}"
      fi
      ;;
  esac
done

# Set $_COMMAND_PARAMETERS to $_COMMAND_ARGV, minus the initial element, $0. This
# provides an array that is equivalent to $* and $@ within each command
# function, though the array is zero-indexed, which could lead to confusion.
_COMMAND_PARAMETERS=(${_COMMAND_ARGV[*]})
unset "_COMMAND_PARAMETERS[0]"

# Initialize $_DEFINED_COMMANDS array.
_DEFINED_COMMANDS=()

_load_commands() {
  # declare when called with '-F' displays all of the functions with the format
  # `declare -f function_name`
  local _function_list=($(declare -F))

  for __name in "${_function_list[@]}"; do
    # Each element has the format `declare -f function_name`, so set the name
    # to only the 'function_name' part of the string.
    local _function_name
    _function_name=$(printf "%s" "${__name}" | awk '{ print $3 }')

    # Add the function name to the $_DEFINED_COMMANDS array unless it starts
    # with an underscore or is desc
    if ! ( [[ "${_function_name}" =~ ^_(.*)  ]] || \
           [[ "${_function_name}" == "desc"  ]] ) then
      _DEFINED_COMMANDS+=("${_function_name}")
    fi
  done
}

_main() {
  # If $_CMD is blank, then set to `$DEFAULT_COMMAND`
  if [[ -z "${_CMD}" ]]
  then
    _CMD="${DEFAULT_COMMAND}"
  fi

  # Load all of the commands.
  _load_commands

  # If the command is defined, run it, otherwise return an error.
  if _contains "${_CMD}" "${_DEFINED_COMMANDS[*]:-}"
  then
    # Pass all comment arguments to the program except for the first ($0).
    ${_CMD} "${_COMMAND_PARAMETERS[@]:-}"
  else
    _abort "Unknown command:" "${_CMD}"
  fi
}

# Utility Functions
_function_exists () {
  # Returns 0 if a function with the given name is defined in the current environment.
  [ "$(type -t "${1}")" == 'function' ]
}
_command_exists () {
  # Returns 0 if a command with the given name is defined in the current environment.
  # http://stackoverflow.com/a/677212
  hash "${1}" 2>/dev/null
}
_contains () {
  # Usage: _contains "$item" "${list[*]}"
  # Returns 0 if item is included in list
  local _test_list=(${*:2})
  for __test_element in "${_test_list[@]:-}"
  do
    if [[ "${__test_element}" == "${1}" ]]
    then
      return 0
    fi
  done
  return 1
}
_join () {
  # Usage:
  #   _join "," a b c
  #   _join "${an_array[@]}"
  local _separator
  local _target_array
  local _dirty
  local _clean
  _separator="${1}"
  _target_array=(${@:2})
  _dirty="$(printf "${_separator}%s"  "${_target_array[@]}")"
  _clean="${_dirty:${#_separator}}"
  printf "%s" "${_clean}"
}
_command_argv_includes () {
  # This is a shortcut for simple cases where a command wants to check for the
  # presence of options quickly without parsing the options again.
  # Usage: _command_argv_includes "an_argument"
  # Returns 0 if the argument is included in `$_COMMAND_ARGV`
  _contains "${1}" "${_COMMAND_ARGV[*]}"
}
_blank () {
  # Usage: _blank "$an_argument"
  # Returns 0 if the argument is not present or null.
  [[ -z "${1:-}" ]]
}
_present() {
  # Usage: _present "$an_argument"
  # Returns 0 if the argument is present and not null.
  [[ -n "${1:-}" ]]
}
_interactive_input() {
  # Returns 0 if the current input is interactive (eg, a shell).
  # 1 if the current input is stdin / piped input.
  [[ -t 0 ]]
}
_piped_input() {
  ! _interactive_input
}

desc () {
  # Usage:
  #   desc <name> <description>
  #   desc --get <name>
  #
  # Options:
  #   --get  Print the description for <name> if one has been set.
  #
  # Set or print a description for a specified command or function <name>. The
  # <description> text can be passed as the second argument or as standard input.

  # To make the <description> text available to other functions, `desc()` assigns
  # the text to a variable with the format `$___desc_<name>`.

  set +e
  [[ -z "${1:-}" ]] && _abort "desc(): No command name specified."

  if [[ "${1}" == "--get" ]]
  then # get ------------------------------------------------------------------
    [[ -z "${2:-}" ]] && _abort "desc(): No command name specified."

    local _name="${2:-}"
    local _desc_var="___desc_${_name//:}"

    if [[ -n "${!_desc_var:-}" ]]
    then
      printf "%s\n" "${!_desc_var}"
    else
      printf "No additional information for \`%s\`\n" "${_name}"
    fi
  else # set ------------------------------------------------------------------
    if [[ -n "${2:-}" ]]
    then # argument is present
      read -r -d '' "___desc_${1//:}" <<HEREDOC
${2}
HEREDOC
    else # no argument is present, so assume piped input
      read -r -d '' "___desc_${1//:}"
    fi
  fi
  set -e
}

#================================================

desc 'version' <<HEREDOC
Usage:
  ${_ME} ( version | --version )

Description:
  Display the current program version.

  To save you the trouble, the current version is ${_VERSION}
HEREDOC
version () {
  printf "%s\n" "${_VERSION}"
}

#================================================

desc 'commands' <<HEREDOC
Usage:
  ${_ME} commands [--raw]

Options:
  --raw  Display the command list without formatting.

Description:
  Display the list of available commands.
HEREDOC
commands () {
  if _command_argv_includes "--raw"
  then
    printf "%s\n" "${_DEFINED_COMMANDS[@]}"
  else
    printf "Available commands:\n"
    printf "  %s\n" "${_DEFINED_COMMANDS[@]}"
  fi
}

#================================================

desc 'help' <<HEREDOC
Usage:
  ${_ME} help [<command>]

Description:
  Display help information for ${_ME} or a specified command.
HEREDOC
help () {
  if [[ ${#_COMMAND_ARGV[@]} = 1 ]]
  then
    printf "%s\n\n" "${BANNER}"
    commands
  else
    desc --get "${1}"
  fi
}
