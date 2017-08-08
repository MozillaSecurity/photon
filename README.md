![Logo](https://github.com/posidron/posidron.github.io/raw/master/static/images/photon.png)


A utility for managing RAM disks.


### Basic Example

![Dharma Demo](https://people.mozilla.com/~cdiehl/screenshots/photon/example.png "")


#### Retrieve JSON output via the CLI
```bash
./photon.py -create -size 100 2>&1 >/dev/null | ack "JSON: (.*)" --output='$1' | python -m json.tool
```


### Help Menu
![Dharma Demo](https://people.mozilla.com/~cdiehl/screenshots/photon/help.png "")
