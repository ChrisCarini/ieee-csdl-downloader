# IEEE Computer Society Digital Library Downloader

## 🛠️ Setup

1. Visit [https://www.computer.org/csdl/home](https://www.computer.org/csdl/home) and login
2. Run the below JavaScript in the console, and copy it's value into the respective configuration value in
   `config.yaml`.
   ```javascript
   `; ${document.cookie}`.split('; CSDL_AUTH_COOKIE=').pop().split(';').shift()
   ```
4. Run the download:
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