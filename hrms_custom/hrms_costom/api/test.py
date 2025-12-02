
import frappe
import requests

url = "https://sandbox.posindonesia.co.id:8245"

@frappe.whitelist(['POST'])
def getToken(username, password):
    payload = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(f"{url}/token", auth=(username, password), data=payload)
    return response.json()

@frappe.whitelist(['POST'])
def sendData(username, password, x_pos_key):
    request_token = getToken(username, password)
    if 'access_token' not in request_token:
        return {'error': 'Failed to obtain access token', 'details': ""}

    token = request_token['access_token']

    headers = { 
        'Content-Type': 'application/json', 
        'X-POS-Key': x_pos_key,
        'Authorization': f"Bearer {token}"
    }
    nippos = frappe.db.get_value("Employee",{"first_name": "supratman"}, "custom_nippos")
    if not nippos:
        frappe.throw("NIPPOS is not set in Pos Indonesia Settings")
    # nippos = "995491616"
    payload = {
        "nippos": nippos
    }
    response = requests.post(f"{url}/SDMEXT/1.1.0/masternew/pegawainew1", json=payload, headers=headers)
    return response.json()
