import requests

url_generate_webhook = 'https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON'
data = {
    "name": "Abhinav Gupta",
    "regNo": "0827CS221011",
    "email": "abhinavgupta220045@acropolis.in"
}

response = requests.post(url_generate_webhook, json=data)
response.raise_for_status()
response_data = response.json()

webhook_url = response_data.get("webhook")
access_token = response_data.get("accessToken")

if not webhook_url or not access_token:
    print("Error: Webhook URL or Access Token missing.")
    exit(1)

print("Webhook URL:", webhook_url)
print("Access Token:", access_token)

sql_query = """SELECT 
    p.AMOUNT AS SALARY,
    CONCAT(e.FIRST_NAME, ' ', e.LAST_NAME) AS NAME,
    FLOOR(DATEDIFF(CURDATE(), e.DOB) / 365) AS AGE,
    d.DEPARTMENT_NAME
FROM 
    PAYMENTS p
JOIN 
    EMPLOYEE e ON p.EMP_ID = e.EMP_ID
JOIN 
    DEPARTMENT d ON e.DEPARTMENT = d.DEPARTMENT_ID
WHERE 
    DAY(p.PAYMENT_TIME) != 1
ORDER BY 
    p.AMOUNT DESC
LIMIT 1;"""  

url_submit_query = 'https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON'
headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}

submission_data = {
    "finalQuery": sql_query
}

response_submit = requests.post(url_submit_query, headers=headers, json=submission_data)
response_submit.raise_for_status()  
print("Response:", response_submit.text)
