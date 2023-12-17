# Run following command
`pip install -r requirements.txt`
# Crawl web dulichviet
```python
cd DuLich
python extract_urls.py
scrapy crawl Tour -o DuLichVietTour.json
```

# Crawl web vietnambooking
```python
cd Vietnambooking
scrapy crawl Tour -o VietnambookingTour.json
```

# Add data to MonogoDB
```python
python json_to_mongo.py
```