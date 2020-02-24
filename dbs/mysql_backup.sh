#!/bin/bash
DB_HOST="127.0.0.1"
DB_PORT="3306"
DB_USER=""
DB_PASS=""
DB_NAMES=""
#
BKP_DIR="/var/backup"
COPY_COUNT="2"
#
EXP=".sql.gz"
DATE=$(date '+%d-%m-%Y')
MYSQL_OPT="-R -e --single-transaction -h${DB_HOST} -P${DB_PORT} -u${DB_USER} -p${DB_PASS}"
#
#
function backup_db() {
	cd "${BKP_DIR}" && {
		#
		for DB in ${DB_NAMES}; do
			#
			FNAME="${DB}_${DATE}${EXP}"
			[[ -e "${FNAME}" ]] || {
				mysqldump ${MYSQL_OPT} ${DB} | gzip > "${FNAME}"
			}
		done
	}
}
#
function clear_old() {
	cd "${BKP_DIR}" && {
		for DB in ${DB_NAMES}; do
			#
			COUNT="$(ls ${DB}* | wc -w)"
			for I in $(ls -tr ${DB}*); do
				#
				[[ ${COUNT} -gt ${COPY_COUNT} ]] && rm -f ${I}
				let "COUNT=COUNT-1"
			done
		done
	}
}
#
#
#set -x
backup_db && clear_old
#set +x

