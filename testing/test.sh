#!/usr/bin/env bash
sleep 10

error=0
echo "-- response code test --"
echo "Testing response code, looking for a 200 code"
if $(curl -s -I localhost | head -n 1 | grep 200 >/dev/null);
then
  echo "Response code test passed"
else
  echo "Response code test failed"
  error=1
fi

echo "-- Articles list response test --"
echo "Testing article list response, looking for a valid json list"
json_string=$(curl -s localhost/articles)
if jq -e . >/dev/null 2>&1 <<<"$json_string"; then
    echo "Articles list response test passed"
else
    echo "Articles list response test failed"
    error=1
fi


echo "-- Single article query test --"
echo "Testing single article query , looking for a valid json list"
json_string=$(curl -s localhost/article/1)
if jq -e . >/dev/null 2>&1 <<<"$json_string"; then
    echo "Single article query test passed"
else
    echo "Single article query test failed"
    error=1
fi

echo "-- Article creation test --"
echo "Testing article creation ,looking for a valid json list"
curl -s -d '{"Id": "3", "Title": "My new product", "Desc": "New Article Description", "Content": "New Article Content"}' -H "Content-Type: application/json" -X POST localhost/article
json_string=$(curl -s localhost/article/3)
id=$(echo "$json_string" |  jq -r '.Id')
if [[ $id -eq 3 ]]; then
    echo "Article creation test passed"
else
    echo "Article creation test failed"
    error=1
fi

echo "-- Article deletion test --"
echo "Testing article deletion ,looking for a not valid json list"
curl -s -X DELETE localhost/article/3
json_string=$(curl -s localhost/article/3)
id=$(echo "$json_string" |  jq -r '.Id')
if [[ $id -eq 3 ]]; then
    echo "Article deletion test failed"
    error=1
else
    echo "Article deletion test passed"
fi

if [[ $error -eq 1 ]]; then
  docker-compose -f "testing/docker-compose.yml" down
  exit 1
else
  exit 0
fi
