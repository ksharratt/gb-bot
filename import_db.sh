cd db
find . -type f -printf '%f\n' | xargs -I@ sh -c 'curl $REPLIT_DB_URL --data-urlencode "@=$(cat "@")"'

