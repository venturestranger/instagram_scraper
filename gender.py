import requests 

gender_list = {"male": "M", "female": "F"}

def gender_predict(name):
	resp = requests.get(f"https://api.genderize.io?name={name}&country_id=KZ")
	try:
		return gender_list[resp.json()["name"]]
	except:
		return "N"
