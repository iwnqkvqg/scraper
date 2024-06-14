This repo is for illustrative purposes, most of the forums would block the bots.

# Scraper

Get new posts for a list of selected topics.


## Usage

```bash
python -m src.main [OPTIONS]
```


## Options

- `config` &mdash; Configuration file. Default: `config/settings.yaml`
- `verbose` &mdash; Print debug messages


## Config file

Configuration file is a YAML file with the following structure:

- `base_url` &mdash; Base URL of the forum
- `history` &mdash; File containing the list of previously visited pages
- `proxy` &mdash; (Optional). Proxy in "http://{ip}:{port}" format
- `reporter` &mdash; Reporter type. Currently, only "csv" is supported
- `top` &mdash; Number of pages to scrape for each topic. Set to `0` to scrape all pages
- `topics` &mdash; List of topics to monitor

Topics contain the following fields:

- `label` &mdash; Topic label, e.g. "movies-2024". This is included in the report file
- `url` &mdash; Topic URL. _Note: URLs are relative_
- `disabled` &mdash; (Optional) Skip topic

Example:

```yaml
base_url: https://example.com
history: config/history.gz
proxy: http://1.1.1.1:1234
reporter: csv
top: 10
topics:
    -
      disabled: false
      label: topic-label
      url: /path/to/topic
```
