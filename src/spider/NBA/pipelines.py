# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class NbaPipeline(object):
    def open_spider(self, spider):
        self.file = open("./playerInfo.csv", "wb")
        self.exporter = CsvItemExporter(self.file, fields_to_export=["Name", "Position", "Height", "Weight",
                                                                     "Born", "Recruiting_rank", "Draft_team",
                                                                     "Experience", "Career_Length"])
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
