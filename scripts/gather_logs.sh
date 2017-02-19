set -e

service=$1

[ -z "$service" ] && echo "Empty"

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
if [ ! -z "${service}" ]; then
  echo "Copying logs for: ${service}"
  GATHER_DIR=${service}-logs_${TIMESTAMP}
else
  GATHER_DIR=tq-celery-logs_${TIMESTAMP}
fi
OUTPUT=tq-celery-logs-${TIMESTAMP}.log

mkdir ${GATHER_DIR}
echo "Created dir: ${GATHER_DIR}"

for instance in $(cat /etc/appscale/taskqueue_nodes | tail -n +2)
#for instance in $(cat /etc/appscale/masters /etc/appscale/slaves)
do
  mkdir ${GATHER_DIR}/${instance}
  if [ ! -z "${service}" ]; then
    echo "Copying ${instance}:/var/log/appscale/${service}-*.log*"
    scp -r ${instance}:/var/log/appscale/*${service}* ${GATHER_DIR}/${instance}
  else
    scp -r ${instance}:/var/log/appscale/taskqueue-*.log* ${GATHER_DIR}/${instance}
    scp -r ${instance}:/var/log/appscale/celery_workers/h-script-*.log ${GATHER_DIR}/${instance}
  fi
done

