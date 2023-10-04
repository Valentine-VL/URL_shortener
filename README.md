# Test Python CLI app (URL shortener)

### Task:

- Transform a long URL to a short URL.
- Expand a shortened URL to its original form.
- Store and retrieve URLs in a MongoDB database.
- Automatic expiration of shortened URLs after a configurable time.

### Installation:
Run following commands in directory of your choice:

1.       git clone https://github.com/Valentine-VL/URL_shortener.git
2.       cd URL_shortener
3.       docker-compose up --build -d

### Execute script
1. Shorten given url then expand it back:
   -     docker exec url_app python app.py --minify=https://www.example.com/path\?q=search
      NOTE: Please do not forget escape "?" symbol with "\\" or wrap whole url in brackets like: 
      >--minify="https://www.example.com/path?q=search"
   - copy output url result
   -     docker exec url_app python app.py --expand=output_result_here
2. Run tests: 
   -     docker exec url_app python -m pytest tests_app.py

##### Initial URL expiry time is set to 10 sec
