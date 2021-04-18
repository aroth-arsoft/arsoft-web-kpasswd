#!/bin/sh
script_file=`readlink -f "$0"`
script_dir=`dirname "$script_file"`
gunicorn_user='app'
gunicorn_num_workers=${GUNICORN_NUM_WORKERS:-2}
gunicorn_num_threads=${GUNICORN_NUM_THREADS:-2}
gunicorn_debug=${GUNICORN_DEBUG:-0}
gunicorn_opts=''

if [ $gunicorn_debug -ne 0 ]; then
    gunicorn_opts="$gunicorn_opts -R --capture-output --log-level=DEBUG"
fi

exec gunicorn --workers=${gunicorn_num_workers} --threads=${gunicorn_num_threads} $gunicorn_opts -b 0.0.0.0:8000 --user "$gunicorn_user" --group "nogroup" --chdir "$script_dir" app:application
exit $?

