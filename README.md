# Run following command
pip install -r requirements.txt
# Crawl web dulichviet
cd DuLich
conda activate webcrawler
python get_html.py
python extract_urls.py
scrapy crawl Tour -o DuLichVietTour.json

# Crawl web vietnambooking
cd Vietnambooking
conda activate webcrawler
scrapy crawl Tour -o VietnambookingTour.json
