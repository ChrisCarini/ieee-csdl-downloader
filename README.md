# IEEE Computer Society Digital Library Downloader

## 🛠️ Setup

1. Visit [https://www.computer.org/csdl/home](https://www.computer.org/csdl/home) and login
2. Find a request with the `CSDL_AUTH_COOKIE` cookie, and copy it's value into `auth.py`
3. Run the download:
   ```shell
   source venv/bin/activate && \
   python3 -m ieee_csdl_downloader.download
   ```

## 🤓 Hacking

### Getting Setup

```shell
./init.sh
```

### Saving Dependencies

```shell
source activate
pip-chill > requirements.txt
```

### Running linting and tests

```shell
./lint.sh && pytest test/
```