#!/usr/bin/env bash

#Debugging
set -x

#Exit Immediately if child job is failed 
set -eo pipefail


main(){

set_env
validate_env

while read user_to_reset
do
echo "tabcmd reset_openid_sub --target-username ${user_to_reset} -s ${TABLEAU_HOSTNAME} -u ${TABLEAU_USERNAME} -u ${TABLEAU_USERNAME} -p ${TABLEAU_PASSWORD}"
tabcmd reset_openid_sub --target-username ${user_to_reset} \
  -s "${TABLEAU_HOSTNAME}" \
  -u ${TABLEAU_USERNAME} \
  -p ${TABLEAU_PASSWORD} \
  || echo "User ${user_to_reset} is not found, continue to the next user..."
done < ${FILE_LIST}
}


set_env(){
if [[ -e "/etc/profile.d/tabcmd.sh" ]]; then
  source /etc/profile.d/tabcmd.sh
fi

DIR_SANDBOX=$(cd $(dirname $0); pwd)

TABLEAU_HOSTNAME="${TABLEAU_HOSTNAME:-10.200.108.147}"
TABLEAU_USERNAME="${TABLEAU_USERNAME:-bi-dev}" 
TABLEAU_PASSWORD="${TABLEAU_PASSWORD:-}" #Mandatory
FILE_LIST="${FILE_LIST:-$DIR_SANDBOX/list_username.csv}"
}

validate_env(){
if [[ -z "${TABLEAU_HOSTNAME}" ]]; then 
  die 1 "Variable \$TABLEAU_HOSTNAME is not set."
fi

if [[ -z "${TABLEAU_USERNAME}" ]]; then
  die 1 "Variable \$TABLEAU_USERNAME is not set."
fi
if [[ -z "${TABLEAU_PASSWORD}" ]]; then
  die 1 "Variable \$TABLEAU_PASSWORD is not set."
fi
}

die() {
  error_signal=${1:-1}   ## exits with 1 if error number not given
  shift
  (>&2 echo "$*")
  exit "$error_signal"
}

main ${@}

