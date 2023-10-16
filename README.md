# Money Tracker

This repository is python based backend for a splitwise like money/expense tracking system.
## Getting started
Get the code either down the zip file or use [git](https://git-scm.com/).
```bash
git clone https://github.com/MullaAhmed/PyEarnX.git
```
Move into the folder
```bash
cd MoneyTracker
```
Use the package manager pip to install Python dependencies.

```bash
pip install -r requirements.txt
```
Use the package manager npm to install React dependencies.

```bash
npm install
```

Building React dependencies.

```bash
npm build dev
```

## Usage
Install Redis and then start the redis server (C:\Program Files\Redis\redis-cli.exe)
and keep it running 

Start Celery in one CMD
```bash
celery -A MoneyTracker worker -l info -P eventlet
```
Start Django Server in another CMD
```bash
python manage.py runserver
```

To run it on your local server
```bash
python manage.py runserver
```
#### API Testing
Click [here](https://documenter.getpostman.com/view/21828511/2s8Z72VXUq) for the documentation of the postman collection of all the APIs.  
Access the API collection: https://elements.getpostman.com/redirect?entityId=21828511-6b276614-3566-471d-b26c-2a9828036097&entityType=collection

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
