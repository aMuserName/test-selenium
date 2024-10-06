Prerequisites

- java 11 or higher
- python 3.6 or higher

Create the venv
```
python -m venv <any_name>
```

Install dependencies in reqs.txt
```
source <any_name>/bin/activate
pip install -r requirements.txt
```

Download selenium server (I use selenium-server-4.25.0.ja)

Run server as hub in another console
```
java -jar selenium-server-4.25.0.jar hub
```

Add node to process requests in another console
```
java -jar selenium-server-4.25.0.jar node
```

Run test
```
python selenium_unittest.py
```
