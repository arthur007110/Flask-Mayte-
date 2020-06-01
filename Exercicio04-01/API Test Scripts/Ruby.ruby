require 'uri'
require 'net/http'

url = URI("http://localhost:5000/register")

http = Net::HTTP.new(url.host, url.port)

request = Net::HTTP::Get.new(url)
request["cache-control"] = 'no-cache'
request["postman-token"] = '7741d0a7-549c-2f22-8e22-a9ebd670c684'

response = http.request(request)
puts response.read_body