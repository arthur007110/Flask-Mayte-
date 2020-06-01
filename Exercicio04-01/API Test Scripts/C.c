CURL *hnd = curl_easy_init();

curl_easy_setopt(hnd, CURLOPT_CUSTOMREQUEST, "GET");
curl_easy_setopt(hnd, CURLOPT_URL, "http://localhost:5000/register");

struct curl_slist *headers = NULL;
headers = curl_slist_append(headers, "postman-token: 9e4f1db0-4ddd-64a7-8f74-289ddaa84768");
headers = curl_slist_append(headers, "cache-control: no-cache");
curl_easy_setopt(hnd, CURLOPT_HTTPHEADER, headers);

CURLcode ret = curl_easy_perform(hnd);