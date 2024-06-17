import contextlib
import csv
import logging
import os
import sqlite3
from pathlib import Path
import json
import wx
import tempfile

from .helpers import (
    get_exclude_from_bom,
    get_exclude_from_pos,
    get_pcb_value,
    get_valid_footprints,
    natural_sort_collation,
)

THRESHOLD = 6

PART_REFERENCE = 0
PART_VALUE = 1
PART_FOOTPRINT = 2
PART_MPN = 3
PART_BOMCHECK = 4
PART_POSCHECK = 5


class Store:
    """A storage class to get data from a sqlite database and write it back"""

    def __init__(self, parent, file_path, board):
        self.logger = logging.getLogger(__name__)
        self.parent = parent
        self.file_path = file_path


        self.datadir = os.path.join(self.file_path, "database")    
        self.dbfile = os.path.join(self.datadir, "project.db") 
        self.order_by = "reference"
        self.order_dir = "ASC"
        self.board = board
        
        try:
            self.setup()
        except sqlite3.Error as e:
            wx.MessageBox(
                "Do not have write permission, please run kicad as administrator\r\n",
                "Error",
                style=wx.ICON_ERROR,
            )
        # Call create_db function here,if database build false
        try:
            self.update_from_board()
        except sqlite3.Error as e:
            wx.MessageBox(
                "database create error,delete the project cache folder : datebase\r\n",
                "Error",
                style=wx.ICON_ERROR,
            )

    def setup(self):
        """Check if folders and database exist, setup if not"""
        if not os.path.isdir(self.datadir):
            self.logger.info(
                "Data directory 'nextpcb' does not exist and will be created."
            )
            Path(self.datadir).mkdir(parents=True, exist_ok=True)
        self.create_db()

    def set_order_by(self, n):
        """Set which value we want to order by when getting data from the database"""
        if n > THRESHOLD:
            return
        # The following two cases are just a temporary hack and will eventually be replaced by
        # direct sorting via DataViewListCtrl rather than via SQL query
        n = n - 1
        order_by = [
            "reference",
            "value",
            "footprint",
            "mpn",
            "manufacturer",
            "quantity",
        ]
        if self.order_by == order_by[n] and self.order_dir == "ASC":
            self.order_dir = "DESC"
        else:
            self.order_by = order_by[n]
            self.order_dir = "ASC"

    def create_db(self):
        """Create the sqlite database tables."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS part_info ("
                    "reference NOT NULL PRIMARY KEY,"
                    "value TEXT NOT NULL,"
                    "footprint TEXT NOT NULL,"
                    "mpn TEXT,"
                    "manufacturer TEXT,"
                    "category TEXT,"
                    "sku TEXT,"
                    "quantity INT DEFAULT 1,"
                    "bomcheck INT DEFAULT 1,"
                    "poscheck INT DEFAULT 1,"
                    "side TEXT,"
                    "part_detail TEXT,"
                    "image BLOB"
                    ")",
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
                        f"SELECT reference, value, footprint,  mpn, manufacturer, category, sku, 1 as quantity,\
                            bomcheck, poscheck, side FROM part_info ORDER BY {self.order_by} COLLATE naturalsort {self.order_dir}"
                    ).fetchall()
                ]

    def read_parts_by_group_value_footprint(self):
        """"""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            con.create_collation("naturalsort", natural_sort_collation)
            with con as cur:
                query = f"SELECT GROUP_CONCAT(reference), value, footprint, mpn, manufacturer, \
                category, sku,  COUNT(*) as quantity, GROUP_CONCAT(bomcheck), GROUP_CONCAT(poscheck), \
                 GROUP_CONCAT(side) FROM part_info GROUP BY value, footprint, mpn, manufacturer \
                ORDER BY {self.order_by} COLLATE naturalsort {self.order_dir}"
                a = [list(part) for part in cur.execute(query).fetchall()]
                return a

    def export_parts_by_group(self):
        """export BOM by group value、footprint"""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            con.create_collation("naturalsort", natural_sort_collation)
            with con as cur:
                query = f"SELECT GROUP_CONCAT(reference), value, footprint, mpn, manufacturer, \
                category, sku, COUNT(*) as quantity FROM part_info \
                GROUP BY value, footprint, mpn, manufacturer \
                ORDER BY reference COLLATE naturalsort ASC "
                a = [list(part) for part in cur.execute(query).fetchall()]
                return a



    def read_bom_parts(self):
        """Read all parts that should be included in the BOM."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            con.create_collation("naturalsort", natural_sort_collation)
            with con as cur:
                # Query all parts that are supposed to be in the BOM an have an mpn number, group the references together
                query = f"SELECT mpn, COUNT(*) as quantity, GROUP_CONCAT(reference), value, manufacturer, category, sku \
                FROM part_info GROUP BY footprint, mpn\
                ORDER BY reference COLLATE naturalsort ASC"
                a = [list(part) for part in cur.execute(query).fetchall()]
                return a


    def read_pos_parts(self):
        """Read all parts that should be included in the POS."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            con.create_collation("naturalsort", natural_sort_collation)
            with con as cur:
                # Query all parts that are supposed to be in the POS
                query = "SELECT reference, value, footprint FROM part_info WHERE poscheck = 1 ORDER BY reference COLLATE naturalsort ASC"
                return [list(part) for part in cur.execute(query).fetchall()]

    def create_part(self, part):
        """Create a part in the database."""
        try:
            with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO part_info VALUES (?,?,?,?,'','','','',?,?,?,'','' )",
                    part, 
                )
                con.commit()
        except sqlite3.Error as e:
            # 打印异常信息，可以根据需要进行其他异常处理
            print(f"An error occurred: {e}")
            # 可以选择重新抛出异常，或者处理它
            raise


    def update_part(self, part):
        """Update a part in the database, overwrite mpn if supplied."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                if len(part) == 7:
                    cur.execute(
                        "UPDATE part_info set value = ?, footprint = ?,  mpn = '', manufacturer = '', \
                        category = '',sku = '',  quantity = '', bomcheck = ?, poscheck = ?, side = ?, part_detail = '',image = '' WHERE reference = ?",
                        part[PART_VALUE:PART_MPN]
                        + part[PART_BOMCHECK:]
                        + part[PART_REFERENCE:PART_VALUE],
                    )
                else:
                    cur.execute(
                        "UPDATE part_info set value = ?, footprint = ?,quantity = '', bomcheck = ?, poscheck = ?, side = ? WHERE reference = ?",
                        part[PART_VALUE:] + part[PART_REFERENCE:PART_VALUE],
                    )
                cur.commit()
    
    def set_batch_bom_match(self, values):
        """Change the BOM attribute for a parts in the database."""
        update_statement = """
        UPDATE part_info SET 
            mpn = ?, 
            manufacturer = ?, 
            category = ?, 
            sku = ?, 
            part_detail = ?
        WHERE reference = ?
        """
        try:
            with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
                for value in values:
                    detail_data = json.dumps(value[5])
                    update_params = (
                        value[1],  # mpn
                        value[2],  # manufacturer
                        value[3],  # category
                        value[4],  # sku
                        detail_data,  # part_detail as JSON
                    )
                    for reference in value[0].split(","):
                        # 为每个 reference 添加到参数列表
                        con.execute(update_statement, update_params + (reference,))
                con.commit() 
        except sqlite3.Error as e:
            con.rollback()  # 发生错误时回滚事务
            print(f"Database error: {e}")
        except Exception as e:
            con.rollback()  
            print(f"An error occurred: {e}")

    def set_bom_match_ref(self,references, value):
        """Change the BOM attribute for a part in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            if isinstance(value[4], str) and value[4]:
                 value[4] = json.loads( value[4] )
            
            detail_data = json.dumps(value[4])
            update_params = (value[0], value[1], value[2], value[3], detail_data)
            try:
                for reference in references.split(","):
                    
                    with con as cur:
                        cur.execute(
                            f"UPDATE part_info SET  mpn = ?, manufacturer = ?, \
                                category = ?,sku = ?,part_detail = ? WHERE reference = '{reference}'",
                                update_params,
                        )
                        cur.commit()
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")


    def set_batch_cache_image(self, values):
        """Cache image binary data in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            for value in values:
                image_params = (value[6] )
                try:
                    for reference in value[0].split(","):
                        with con as cur:
                            cur.execute(
                                f"UPDATE part_info SET  image = ?  WHERE reference = '{reference}'",
                                    (image_params,)
                            )
                            cur.commit()    
                except sqlite3.Error as e:
                    print(f"Database error: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")
                    

    def set_cache_image(self, refs, image_params):
        """Cache image binary data in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            try:
                for reference in refs.split(","):
                    with con as cur:
                        cur.execute(
                            f"UPDATE part_info SET  image = ?  WHERE reference = '{reference}'",
                                (image_params,)
                        )
                        cur.commit()    
                print(f"cache image to database")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

    def get_part(self, ref):
        """Get a part from the database by its reference."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                return cur.execute(
                    "SELECT * FROM part_info WHERE reference=?", (ref,)
                ).fetchone()

    def get_reference_mpn_footprint(self):
        """Get reference, mpn, and footprint for a part from the database by its reference."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            con.create_collation("naturalsort", natural_sort_collation)
            with con as cur:
                result = cur.execute(
                    "SELECT reference, mpn, footprint FROM part_info \
                        ORDER BY reference COLLATE naturalsort ASC"
                ).fetchall()
                return result

    def get_unique_value_fp_count(self):
        """Get the count of unique mpn values from the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con:
                cur = con.cursor()
                # 使用 DISTINCT 来获取不同的 mpn 值，并计数
                cur.execute(
                    "SELECT value, footprint FROM part_info GROUP BY value, footprint;"
                )
                all_results = cur.fetchall()   
                total_count = len(all_results)  # 计算总数
                return total_count   
            
    def delete_part(self, ref):
        """Delete a part from the database by its reference."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                cur.execute("DELETE FROM part_info WHERE reference=?", (ref,))
                cur.commit()

    def set_bom(self, refs, state):
        """Change the BOM attribute for a part in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            for ref in refs.split(","):
                with con as cur:
                    cur.execute(
                        f"UPDATE part_info SET bomcheck = {int(state)} WHERE reference = '{ref}'"
                    )
                    cur.commit()

    def set_pos(self, refs, state):
        """Change the BOM attribute for a part in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            for ref in refs.split(","):
                with con as cur:
                    cur.execute(
                        f"UPDATE part_info SET poscheck = {int(state)} WHERE reference = '{ref}'"
                    )
                    cur.commit()

    def set_part_side(self, ref, value):
        """Change the BOM attribute for a part in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                cur.execute(
                    f"UPDATE part_info SET side = '{value}' WHERE reference = '{ref}'"
                )
                cur.commit()


    def print_part_info(self, ref):
        """Print the information for a part in the database."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            cur = con.cursor()  # Create a cursor here
            cur.execute(f"SELECT * FROM part_info WHERE reference = '{ref}'")
            rows = cur.fetchall()

            if not rows:
                print(f"No data found for reference: {ref}")
            else:
                # Assuming the columns in your part_info table are, for example, reference, SKU, and category
                print("  MPN   | Manufacturer   | Category  |  SKU  | details")
                print("--------------------------------")
                for row in rows:
                    print(
                        f"{row[3]:<10} | {row[4]:<10} | {row[5]:<10} | {row[6]:<10} | {row[12]} "
                    )

    def get_part_detail(self, ref):
        """Get a part from the database by its reference."""
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                result = cur.execute(
                    f"SELECT part_detail, image FROM part_info WHERE reference = '{ref}'"
                ).fetchone()
                return result


    def update_from_board(self):
        """Read all footprints from the board and insert them into the database if they do not exist."""
        board = self.board
        for fp in get_valid_footprints(board):
            part = [
                fp.GetReference(),
                fp.GetValue(),
                str(fp.GetFPID().GetLibItemName()),
                get_pcb_value(fp),
                int(not get_exclude_from_bom(fp)),
                int(not get_exclude_from_pos(fp)),
                fp.GetLayer(),
            ]
            dbpart = self.get_part(part[PART_REFERENCE])
            # if part is not in the database yet, create it
            if not dbpart:
                self.logger.debug(
                    f"Part {part[PART_REFERENCE]} does not exist in the database and will be created from the board."
                )
                self.create_part(part)
            else:
                # if the board part matches the dbpart except for the and the stock value,
                if part[PART_REFERENCE:PART_FOOTPRINT] == list(dbpart[PART_REFERENCE:PART_FOOTPRINT]) and part[PART_BOMCHECK:PART_POSCHECK ] == [bool(x) for x in dbpart[8:9] ]:
                    # if part in the database, has no mpn value the board part has a mpn value, update including mpn
                    # if dbpart and not dbpart[PART_MPN]:
                    #     self.logger.debug(
                    #         f"Part {part[PART_REFERENCE]} is already in the database but without mpn value, so the value supplied from the board will be set."
                    #     )
                        # self.update_part(part)
                    # if part in the database, has a mpn value
                    if dbpart and dbpart[PART_MPN]:
                        # update mpn value as well if setting is accordingly
                        part.pop(PART_MPN)
                        # self.logger.debug(
                        #     f"Part {part[PART_REFERENCE]} is already in the database and has a mpn value, the value supplied from the board will be ignored."
                        # )
                        # self.update_part(part)
                else:
                    # If something changed, we overwrite the part and dump the mpn value or use the one supplied by the board
                    # self.logger.debug(
                    #     f"Part {part[PART_REFERENCE]} is already in the database but value, footprint, bom or pos values changed in the board file, part will be updated, mpn overwritten/cleared."
                    # )
                    self.update_part(part)
        self.clean_database()

    def clean_database(self):
        """Delete all parts from the database that are no longer present on the board."""
        refs = [f"'{fp.GetReference()}'" for fp in get_valid_footprints(self.board)]
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                cur.execute(
                    f"DELETE FROM part_info WHERE reference NOT IN ({','.join(refs)})"
                )
                cur.commit()

    def clear_database(self):
        with contextlib.closing(sqlite3.connect(self.dbfile)) as con:
            with con as cur:
                cur.execute(f"DELETE FROM part_info")
                cur.commit()
