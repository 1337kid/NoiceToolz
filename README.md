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
