from os import path
from driver_class import DataDriver
import csv


class CSVDataDriver(DataDriver):
    def load(self):
        # If the "file_path" property is not defined, return.
        file_path = self.config.get("file_path")

        if file_path is None:
            self.logger.fatal(
                "File path is not specified."
                + " Please specify the file path under the key 'file_path' in configuration."
            )
            return
        else:
            normalized_path = path.join("config", *path.split(file_path))
            self.logger.info(f"Reading data from {normalized_path}")
            with open(normalized_path, "r") as file:
                data = list(csv.DictReader(file))
                self.logger.info("Fetched data from file")
                return data
