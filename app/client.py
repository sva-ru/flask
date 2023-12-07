import requests

# response = requests.post("http://127.0.0.1:5000/ads",
#                         json={"title": "advertisement3", "description": "I sell mountain air", "owner": "Vasily S."},
#                         )
# print(response.status_code)
# print(response.text)



# response = requests.patch("http://127.0.0.1:5000/ads/1", json={"description": "not description"},)
# print(response.status_code)
# print(response.text)

response = requests.delete(
    "http://127.0.0.1:5000/ads/5",
)
print(response.status_code)
print(response.text)
#
#
# response = requests.get(
#     "http://127.0.0.1:5000/ads/1",
# )
# print(response.status_code)
# print(response.text)
