# NoiceToolz
Self-hosted pastebin and url shortner
## Installation & Setup
Provide your PostgreSQL credentials and a secret key in config.yml<br>
secret kay can be generated using the below code
```python
import secrets
secrets.token_hex(16)
```
## Running
```bash
pip3 install -r requirements.txt
gunicorn app:app
```
## Admin Panel
By default username is "admin" and the password is also "admin". These can be changed in the admin panel
## Some screenshots
![img](https://raw.githubusercontent.com/1337kid/NoiceToolz/main/sc/1.png)
![img](https://raw.githubusercontent.com/1337kid/NoiceToolz/main/sc/4.png)
![img](https://raw.githubusercontent.com/1337kid/NoiceToolz/main/sc/2.png)
![img](https://raw.githubusercontent.com/1337kid/NoiceToolz/main/sc/3.png)
