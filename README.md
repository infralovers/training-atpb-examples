# Flask Blogging Application

This is the base for building a blogging application in Flask.
It is used in a course by Commandemy.

## Setup

pip3 install -r requirements.txt

## Run
export FLASK_APP=app.py
flask run

## Prepare local virtualenv

How to prepare your local environment with virtualenv after cloning the repository

```bash
virtualenv .
source ./bin/activate
./bin/pip install -r requirements.txt
```

## How to run behave

The default behave driver is at the moment set to firefox. This can be reset by the environment variable _DRIVER_. It is coded within features/environment.py.

### Firefox

For using Firefox you must install the Firefox Geckodriver from [Github](https://github.com/mozilla/geckodriver/releases) and place it in the virtualenv _bin_ directory

```bash
version=$(curl -sX GET https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep 'tag_name' | cut -d\" -f4)
wget "https://github.com/mozilla/geckodriver/releases/download/${version}/geckodriver-${version}-macos.tar.gz" -O - | tar xz
mv geckodriver ./bin/
```

### Chrome

To enable the chrome automation you must install the Chromedriver from [Google](https://sites.google.com/a/chromium.org/chromedriver/downloads) and place it in the virtualenv _bin_ directory.

```bash
curl -O "https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_mac64.zip"
unzip chromdriver_mac64.zip
mv chromedriver ./bin/
```

To switch behave to chrome you just need to set DRIVER variable

```bash
DRIVER=chrome ./bin/behave
```

### Headless

Headless testing on your local machine just requires docker installed. You can start the container by following commandline

```bash
docker run -d -p 4444:4444 -e START_XVFB=false --shm-size 2g --name chrome-selenium selenium/standalone-chrome
```

The default configuration of chrome headless will point to the default selenium hub api. But this can also be reset by an environment variable _SELENIUM_

To run the selenium tests use following command

```bash
DRIVER=headless ./bin/behave
```

#### TODO

At the moment headless testing is broken for about_page feature. This tests always returns a Connection refused error.
