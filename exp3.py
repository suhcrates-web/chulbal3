from datetime import datetime
day_name =datetime.today().strftime("%A")[:3]
month_name = datetime.today().strftime("%B")[:3]
print(datetime.today().strftime(f"%d-{month_name}-%Y %H:%M:%S GMT"))