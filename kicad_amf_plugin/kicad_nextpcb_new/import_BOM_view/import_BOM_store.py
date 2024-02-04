import os
import sqlite3
import logging
import json
from pathlib import Path
import contextlib

from kicad_amf_plugin.kicad_nextpcb_new.helpers import (
    natural_sort_collation,
)
from kicad_amf_plugin.kicad_nextpcb_new.board_manager import load_board_manager


class ImportBOMStore:
    def __init__(self, parent):
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.BOARD_LOADED = load_board_manager()
        self.project_path = os.path.split(self.BOARD_LOADED.GetFileName())[0]
        self.datadir = os.path.join(self.project_path, "database")
        self.dbfile = os.path.join(self.datadir, "importBOM.db")
        self.order_by = "reference"
        self.order_dir = "ASC"
        self.setup()

    def setup(self):
        """Check if folders and database exist, setup if not"""
        if not os.path.isdir(self.datadir):
            self.logger.info(
                "Data directory 'nextpcb' does not exist and will be created."
            )
            Path(self.datadir).mkdir(parents=True, exist_ok=True)
        self.create_import_db()

    def create_import_db(self):
        """Create the sqlite database tables."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS import_BOM ('reference' ,'value',\
                    'footprint','mpn', 'manufacturer', 'category', 'sku', 'supplier', 'quantity','part_detail')"
                )
                cur.commit()

    def read_all(self):
        """Read all parts from the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            con.create_collation("naturalsort", natural_sort_collation)
            with con as cur:
                return [
                    list(part)
                    for part in cur.execute(
                        f"SELECT reference, value, footprint,  mpn, manufacturer,  category, sku, supplier, 1 as quantity\
                            FROM import_BOM ORDER BY {self.order_by} COLLATE naturalsort {self.order_dir}"
                    ).fetchall()
                ]

    def read_parts_by_group_value_footprint(self):
        """read or export BOM by group value、footprint"""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            con.create_collation("naturalsort", natural_sort_collation)
            with con as cur:
                query = f"SELECT GROUP_CONCAT(reference), value, footprint, mpn, manufacturer, \
                category, sku, supplier, COUNT(*) as quantity FROM import_BOM \
                GROUP BY value, footprint, mpn, manufacturer \
                ORDER BY {self.order_by} COLLATE naturalsort {self.order_dir}"
                a = [list(part) for part in cur.execute(query).fetchall()]
                return a

    def clear_database(self):
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                cur.execute(f"DELETE FROM import_BOM")
                cur.commit()

    def import_mappings_data(self, Reference_data):
        """Insert to import data into the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                cur.execute(
                    "INSERT INTO import_BOM VALUES (?,?,?,?,?,?,?,?,?,'' )",
                    Reference_data,
                )
                cur.commit()

    def set_mpn(self, ref, value):
        """Change the BOM attribute for a part in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                cur.execute(
                    f"UPDATE import_BOM SET mpn = '{value}' WHERE reference = '{ref}'"
                )
                cur.commit()

    def set_manufacturer(self, ref, value):
        """Change the BOM attribute for a part in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                cur.execute(
                    f"UPDATE import_BOM SET manufacturer = '{value}' WHERE reference = '{ref}'"
                )
                cur.commit()

    def set_category(self, ref, value):
        """Change the BOM attribute for a part in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                cur.execute(
                    f"UPDATE import_BOM SET category = '{value}' WHERE reference = '{ref}'"
                )
                cur.commit()

    def set_sku(self, ref, value):
        """Change the BOM attribute for a part in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                cur.execute(
                    f"UPDATE import_BOM SET sku = '{value}' WHERE reference = '{ref}'"
                )
                cur.commit()

    def set_supplier(self, ref, value):
        """Change the BOM attribute for a part in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                cur.execute(
                    f"UPDATE import_BOM SET supplier = '{value}' WHERE reference = '{ref}'"
                )
                cur.commit()

    def set_multi_mpn(self, ref, value):
        """Change the BOM attribute for a part in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                references = ref.split(",")
                for reference in references:
                    cur.execute(
                        f"UPDATE import_BOM SET mpn = '{value}' WHERE reference = '{reference}'"
                    )
                cur.commit()

    def set_multi_manufacturer(self, ref, value):
        """Change the BOM attribute for a part in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                references = ref.split(",")
                for reference in references:
                    cur.execute(
                        f"UPDATE import_BOM SET manufacturer = '{value}' WHERE reference = '{reference}'"
                    )
                cur.commit()

    def set_multi_category(self, ref, value):
        """Change the BOM attribute for a part in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                references = ref.split(",")
                for reference in references:
                    cur.execute(
                        f"UPDATE import_BOM SET category = '{value}' WHERE reference = '{reference}'"
                    )
                cur.commit()

    def set_multi_sku(self, ref, value):
        """Change the BOM attribute for a part in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                references = ref.split(",")
                for reference in references:
                    cur.execute(
                        f"UPDATE import_BOM SET sku = '{value}' WHERE reference = '{reference}'"
                    )
                cur.commit()

    def set_multi_supplier(self, ref, value):
        """Change the BOM attribute for a part in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                references = ref.split(",")
                for reference in references:
                    cur.execute(
                        f"UPDATE import_BOM SET supplier = '{value}' WHERE reference = '{reference}'"
                    )
                cur.commit()

    def set_part_detail(self, ref, value):
        """Change the BOM attribute for a part in the database."""
        value = json.dumps(value)
        reference = ref.split(",")[0]
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                cur.execute(
                    "UPDATE import_BOM SET part_detail = ? WHERE reference = ?",
                    (value, reference),
                )
                cur.commit()

    def get_part_detail(self, ref):
        """Get a part from the database by its reference."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                return cur.execute(
                    f"SELECT part_detail FROM import_BOM WHERE reference = '{ref}'"
                ).fetchone()[0]
