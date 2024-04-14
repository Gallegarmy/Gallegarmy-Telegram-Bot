import requests
from datetime import datetime, date

response = requests.get(url='http://festivos.z3r3v3r.com/2024/es/gl/')
API_Data = response.json() 
earliest_date = datetime.strptime(f'{date.today().strftime("%Y")}-12-31', '%Y-%m-%d')

for key in API_Data['datos']:
    fecha = datetime.strptime(key['fecha'], '%Y-%m-%d')
    if fecha.date() >= date.today():
        if fecha <= earliest_date:
            earliest_date = fecha
            fiesta = f"O próximo festivo é {key['nombre']} o día {key['fecha']}"
    
print(fiesta)
        