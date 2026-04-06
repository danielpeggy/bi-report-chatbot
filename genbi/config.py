"""
McDonald's HK GenBI Project - Shared Configuration and Reference Data
All constants and reference data used by synthetic data generators
"""

# Date range for synthetic data
DATE_START = "2023-01-01"
DATE_END = "2023-12-31"

# 200 McDonald's stores across Hong Kong
# Region distribution:
#   Hong Kong Island (50 stores): Central & Western (12), Wan Chai (12), Eastern (14), Southern (12)
#   Kowloon (80 stores): Yau Tsim Mong (20), Sham Shui Po (14), Kowloon City (16), Wong Tai Sin (14), Kwun Tong (16)
#   New Territories (70 stores): Sha Tin (12), Tai Po (6), North (6), Sai Kung (10), Yuen Long (8), Tuen Mun (8), Tsuen Wan (8), Kwai Tsing (6), Islands (6)

STORES = [
    # Hong Kong Island - Central & Western (12 stores)
    {"store_id": "S001", "store_name": "McDonald's Central Tower", "district": "Central", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 120, "open_date": "1995-03-15", "rent_monthly": 280000},
    {"store_id": "S002", "store_name": "McDonald's Des Voeux Road", "district": "Central", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 110, "open_date": "1998-07-22", "rent_monthly": 250000},
    {"store_id": "S003", "store_name": "McDonald's IFC Mall", "district": "Central", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 130, "open_date": "2003-09-10", "rent_monthly": 300000},
    {"store_id": "S004", "store_name": "McDonald's Sheung Wan", "district": "Central", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 95, "open_date": "2000-05-18", "rent_monthly": 220000},
    {"store_id": "S005", "store_name": "McDonald's Western Market", "district": "Western", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 85, "open_date": "2001-11-30", "rent_monthly": 180000},
    {"store_id": "S006", "store_name": "McDonald's Kennedy Town", "district": "Western", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 80, "open_date": "2002-01-15", "rent_monthly": 170000},
    {"store_id": "S007", "store_name": "McDonald's Sai Ying Pun", "district": "Western", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 75, "open_date": "2000-08-25", "rent_monthly": 160000},
    {"store_id": "S008", "store_name": "McDonald's Causeway Bay Plaza", "district": "Western", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 115, "open_date": "1996-02-14", "rent_monthly": 240000},
    {"store_id": "S009", "store_name": "McDonald's Possession Street", "district": "Central", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 90, "open_date": "2004-06-20", "rent_monthly": 200000},
    {"store_id": "S010", "store_name": "McDonald's Pedder Street", "district": "Central", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 100, "open_date": "1999-09-03", "rent_monthly": 230000},
    {"store_id": "S011", "store_name": "McDonald's PMQ", "district": "Central", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 88, "open_date": "2008-12-05", "rent_monthly": 210000},
    {"store_id": "S012", "store_name": "McDonald's Tai Kwun", "district": "Central", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 92, "open_date": "2018-05-12", "rent_monthly": 205000},

    # Hong Kong Island - Wan Chai (12 stores)
    {"store_id": "S013", "store_name": "McDonald's Wan Chai Tower", "district": "Wan Chai", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 118, "open_date": "1997-04-10", "rent_monthly": 260000},
    {"store_id": "S014", "store_name": "McDonald's Pacific Place", "district": "Wan Chai", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 125, "open_date": "1998-11-20", "rent_monthly": 290000},
    {"store_id": "S015", "store_name": "McDonald's Queen's Road East", "district": "Wan Chai", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 105, "open_date": "2001-03-08", "rent_monthly": 240000},
    {"store_id": "S016", "store_name": "McDonald's Lee Tung Avenue", "district": "Wan Chai", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 100, "open_date": "2014-10-25", "rent_monthly": 225000},
    {"store_id": "S017", "store_name": "McDonald's So Kongjian Centre", "district": "Wan Chai", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 112, "open_date": "2005-07-18", "rent_monthly": 255000},
    {"store_id": "S018", "store_name": "McDonald's Hennessy Road", "district": "Wan Chai", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 98, "open_date": "2002-09-12", "rent_monthly": 215000},
    {"store_id": "S019", "store_name": "McDonald's Victory House", "district": "Wan Chai", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 93, "open_date": "2003-01-30", "rent_monthly": 205000},
    {"store_id": "S020", "store_name": "McDonald's Lockhart Road", "district": "Wan Chai", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 87, "open_date": "2006-05-22", "rent_monthly": 190000},
    {"store_id": "S021", "store_name": "McDonald's Swire House", "district": "Wan Chai", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 110, "open_date": "2007-08-14", "rent_monthly": 245000},
    {"store_id": "S022", "store_name": "McDonald's Caroline Hill", "district": "Wan Chai", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 82, "open_date": "2009-02-18", "rent_monthly": 175000},
    {"store_id": "S023", "store_name": "McDonald's Immigration Tower", "district": "Wan Chai", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 96, "open_date": "2004-11-09", "rent_monthly": 220000},
    {"store_id": "S024", "store_name": "McDonald's Harbour Centre", "district": "Wan Chai", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 115, "open_date": "2010-03-25", "rent_monthly": 265000},

    # Hong Kong Island - Eastern (14 stores)
    {"store_id": "S025", "store_name": "McDonald's Causeway Bay Centre", "district": "Eastern", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 135, "open_date": "1996-06-15", "rent_monthly": 310000},
    {"store_id": "S026", "store_name": "McDonald's Times Square", "district": "Eastern", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 140, "open_date": "1997-11-20", "rent_monthly": 320000},
    {"store_id": "S027", "store_name": "McDonald's Hysan Place", "district": "Eastern", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 128, "open_date": "2007-09-28", "rent_monthly": 295000},
    {"store_id": "S028", "store_name": "McDonald's Lee Gardens", "district": "Eastern", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 125, "open_date": "2008-05-12", "rent_monthly": 285000},
    {"store_id": "S029", "store_name": "McDonald's Noonday Street", "district": "Eastern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 105, "open_date": "2001-07-15", "rent_monthly": 235000},
    {"store_id": "S030", "store_name": "McDonald's Fashion Walk", "district": "Eastern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 110, "open_date": "2002-03-10", "rent_monthly": 245000},
    {"store_id": "S031", "store_name": "McDonald's Lockhart Road East", "district": "Eastern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 100, "open_date": "2003-09-18", "rent_monthly": 225000},
    {"store_id": "S032", "store_name": "McDonald's Great Eagle Centre", "district": "Eastern", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 120, "open_date": "2005-04-22", "rent_monthly": 275000},
    {"store_id": "S033", "store_name": "McDonald's Excelsior Plaza", "district": "Eastern", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 115, "open_date": "2006-08-30", "rent_monthly": 260000},
    {"store_id": "S034", "store_name": "McDonald's Cross Harbour", "district": "Eastern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 92, "open_date": "2009-01-12", "rent_monthly": 210000},
    {"store_id": "S035", "store_name": "McDonald's Gloucester Road", "district": "Eastern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 98, "open_date": "2004-10-05", "rent_monthly": 220000},
    {"store_id": "S036", "store_name": "McDonald's Windsor House", "district": "Eastern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 104, "open_date": "2008-02-14", "rent_monthly": 235000},
    {"store_id": "S037", "store_name": "McDonald's Sugimoto", "district": "Eastern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 88, "open_date": "2010-06-20", "rent_monthly": 190000},
    {"store_id": "S038", "store_name": "McDonald's Island Beverley", "district": "Eastern", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 118, "open_date": "2011-09-15", "rent_monthly": 270000},

    # Hong Kong Island - Southern (12 stores)
    {"store_id": "S039", "store_name": "McDonald's Aberdeen Centre", "district": "Southern", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 110, "open_date": "2000-05-20", "rent_monthly": 230000},
    {"store_id": "S040", "store_name": "McDonald's Aberdeen Main Road", "district": "Southern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 95, "open_date": "2001-10-15", "rent_monthly": 195000},
    {"store_id": "S041", "store_name": "McDonald's Stanley Plaza", "district": "Southern", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 102, "open_date": "1999-08-22", "rent_monthly": 215000},
    {"store_id": "S042", "store_name": "McDonald's Repulse Bay", "district": "Southern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 85, "open_date": "2005-03-10", "rent_monthly": 180000},
    {"store_id": "S043", "store_name": "McDonald's Deep Water Bay", "district": "Southern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 78, "open_date": "2008-07-18", "rent_monthly": 160000},
    {"store_id": "S044", "store_name": "McDonald's Lei Tung Estate", "district": "Southern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 88, "open_date": "2003-02-14", "rent_monthly": 185000},
    {"store_id": "S045", "store_name": "McDonald's Wong Chuk Hang", "district": "Southern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 92, "open_date": "2006-11-25", "rent_monthly": 200000},
    {"store_id": "S046", "store_name": "McDonald's Ap Lei Chau", "district": "Southern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 82, "open_date": "2007-04-30", "rent_monthly": 175000},
    {"store_id": "S047", "store_name": "McDonald's Lamma Island", "district": "Southern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 65, "open_date": "2010-09-12", "rent_monthly": 120000},
    {"store_id": "S048", "store_name": "McDonald's Pok Fu Lam", "district": "Southern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 75, "open_date": "2009-06-08", "rent_monthly": 155000},
    {"store_id": "S049", "store_name": "McDonald's Shouson Hill", "district": "Southern", "region": "HK_Island", "store_type": "street", "avg_daily_orders": 80, "open_date": "2004-12-20", "rent_monthly": 170000},
    {"store_id": "S050", "store_name": "McDonald's Ocean Park", "district": "Southern", "region": "HK_Island", "store_type": "mall", "avg_daily_orders": 115, "open_date": "2012-08-15", "rent_monthly": 245000},

    # Kowloon - Yau Tsim Mong (20 stores)
    {"store_id": "S051", "store_name": "McDonald's Nathan Road", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 125, "open_date": "1995-02-10", "rent_monthly": 270000},
    {"store_id": "S052", "store_name": "McDonald's Langham Place", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 130, "open_date": "2004-12-18", "rent_monthly": 300000},
    {"store_id": "S053", "store_name": "McDonald's Elements", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 135, "open_date": "2008-10-02", "rent_monthly": 310000},
    {"store_id": "S054", "store_name": "McDonald's Mong Kok Centre", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 128, "open_date": "1999-07-15", "rent_monthly": 290000},
    {"store_id": "S055", "store_name": "McDonald's Argyle Street", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 115, "open_date": "2000-05-22", "rent_monthly": 240000},
    {"store_id": "S056", "store_name": "McDonald's Tai Yang Centre", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 120, "open_date": "2005-03-10", "rent_monthly": 280000},
    {"store_id": "S057", "store_name": "McDonald's Jordan MTR", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 110, "open_date": "2002-08-20", "rent_monthly": 225000},
    {"store_id": "S058", "store_name": "McDonald's Peking Road", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 105, "open_date": "2003-11-05", "rent_monthly": 220000},
    {"store_id": "S059", "store_name": "McDonald's Whampoa Centre", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 118, "open_date": "2006-01-25", "rent_monthly": 265000},
    {"store_id": "S060", "store_name": "McDonald's Hankow Road", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 98, "open_date": "2007-04-12", "rent_monthly": 210000},
    {"store_id": "S061", "store_name": "McDonald's Kowloon Hotel", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 112, "open_date": "2001-09-30", "rent_monthly": 250000},
    {"store_id": "S062", "store_name": "McDonald's Canton Road", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 108, "open_date": "2004-06-15", "rent_monthly": 235000},
    {"store_id": "S063", "store_name": "McDonald's Bubble Street", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 102, "open_date": "2009-02-20", "rent_monthly": 215000},
    {"store_id": "S064", "store_name": "McDonald's Kimberley Road", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 95, "open_date": "2010-07-10", "rent_monthly": 200000},
    {"store_id": "S065", "store_name": "McDonald's Silvercord", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 125, "open_date": "2008-05-22", "rent_monthly": 285000},
    {"store_id": "S066", "store_name": "McDonald's Hart Avenue", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 92, "open_date": "2011-03-18", "rent_monthly": 205000},
    {"store_id": "S067", "store_name": "McDonald's Tsim Sha Tsui", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 120, "open_date": "1998-04-08", "rent_monthly": 260000},
    {"store_id": "S068", "store_name": "McDonald's Star House", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 122, "open_date": "2003-07-14", "rent_monthly": 275000},
    {"store_id": "S069", "store_name": "McDonald's Chatham Road", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 100, "open_date": "2006-09-25", "rent_monthly": 225000},
    {"store_id": "S070", "store_name": "McDonald's Gateway Drive", "district": "Yau Tsim Mong", "region": "Kowloon", "store_type": "drive_thru", "avg_daily_orders": 145, "open_date": "2010-11-30", "rent_monthly": 195000},

    # Kowloon - Sham Shui Po (14 stores)
    {"store_id": "S071", "store_name": "McDonald's Sham Shui Po MTR", "district": "Sham Shui Po", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 105, "open_date": "2001-02-15", "rent_monthly": 215000},
    {"store_id": "S072", "store_name": "McDonald's Cheung Sha Wan", "district": "Sham Shui Po", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 95, "open_date": "2002-08-10", "rent_monthly": 190000},
    {"store_id": "S073", "store_name": "McDonald's Apliu Street", "district": "Sham Shui Po", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 88, "open_date": "2003-05-20", "rent_monthly": 175000},
    {"store_id": "S074", "store_name": "McDonald's Yu Chui Street", "district": "Sham Shui Po", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 82, "open_date": "2005-01-12", "rent_monthly": 165000},
    {"store_id": "S075", "store_name": "McDonald's Paper Street", "district": "Sham Shui Po", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 78, "open_date": "2006-06-25", "rent_monthly": 155000},
    {"store_id": "S076", "store_name": "McDonald's Yen Chow Street", "district": "Sham Shui Po", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 92, "open_date": "2004-03-18", "rent_monthly": 185000},
    {"store_id": "S077", "store_name": "McDonald's Tai Po Road", "district": "Sham Shui Po", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 85, "open_date": "2007-09-08", "rent_monthly": 175000},
    {"store_id": "S078", "store_name": "McDonald's Shantung Street", "district": "Sham Shui Po", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 80, "open_date": "2008-02-22", "rent_monthly": 165000},
    {"store_id": "S079", "store_name": "McDonald's Anchor Street", "district": "Sham Shui Po", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 75, "open_date": "2009-07-15", "rent_monthly": 150000},
    {"store_id": "S080", "store_name": "McDonald's Fuk Tsun Street", "district": "Sham Shui Po", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 72, "open_date": "2010-04-10", "rent_monthly": 145000},
    {"store_id": "S081", "store_name": "McDonald's Nam Cheong", "district": "Sham Shui Po", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 100, "open_date": "2005-10-30", "rent_monthly": 210000},
    {"store_id": "S082", "store_name": "McDonald's Texaco Tower", "district": "Sham Shui Po", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 87, "open_date": "2006-11-12", "rent_monthly": 180000},
    {"store_id": "S083", "store_name": "McDonald's Sham Shui Po Plaza", "district": "Sham Shui Po", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 110, "open_date": "2007-01-20", "rent_monthly": 235000},
    {"store_id": "S084", "store_name": "McDonald's Lai Tung Road", "district": "Sham Shui Po", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 83, "open_date": "2008-08-05", "rent_monthly": 170000},

    # Kowloon - Kowloon City (16 stores)
    {"store_id": "S085", "store_name": "McDonald's Kai Fuk Road", "district": "Kowloon City", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 98, "open_date": "2001-07-18", "rent_monthly": 210000},
    {"store_id": "S086", "store_name": "McDonald's King's Road", "district": "Kowloon City", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 102, "open_date": "2002-05-20", "rent_monthly": 220000},
    {"store_id": "S087", "store_name": "McDonald's Tak Long Estate", "district": "Kowloon City", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 88, "open_date": "2003-09-10", "rent_monthly": 185000},
    {"store_id": "S088", "store_name": "McDonald's Tung Tau Tsuen", "district": "Kowloon City", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 92, "open_date": "2004-02-25", "rent_monthly": 195000},
    {"store_id": "S089", "store_name": "McDonald's Beacon Estate", "district": "Kowloon City", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 85, "open_date": "2005-04-08", "rent_monthly": 175000},
    {"store_id": "S090", "store_name": "McDonald's Kowloon Tong", "district": "Kowloon City", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 115, "open_date": "2006-08-15", "rent_monthly": 260000},
    {"store_id": "S091", "store_name": "McDonald's Sung Wong Toi", "district": "Kowloon City", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 95, "open_date": "2003-11-22", "rent_monthly": 205000},
    {"store_id": "S092", "store_name": "McDonald's Kai Tak Airport", "district": "Kowloon City", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 108, "open_date": "2007-03-10", "rent_monthly": 235000},
    {"store_id": "S093", "store_name": "McDonald's Boundary Street", "district": "Kowloon City", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 100, "open_date": "2008-06-20", "rent_monthly": 215000},
    {"store_id": "S094", "store_name": "McDonald's Kuo Min Street", "district": "Kowloon City", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 82, "open_date": "2009-01-15", "rent_monthly": 170000},
    {"store_id": "S095", "store_name": "McDonald's Lyndhurst Terrace", "district": "Kowloon City", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 78, "open_date": "2010-05-25", "rent_monthly": 160000},
    {"store_id": "S096", "store_name": "McDonald's San Po Kong", "district": "Kowloon City", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 112, "open_date": "2006-10-30", "rent_monthly": 250000},
    {"store_id": "S097", "store_name": "McDonald's Cheung Sha Wan Road", "district": "Kowloon City", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 90, "open_date": "2007-07-18", "rent_monthly": 190000},
    {"store_id": "S098", "store_name": "McDonald's Lok Chun Court", "district": "Kowloon City", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 86, "open_date": "2008-09-12", "rent_monthly": 180000},
    {"store_id": "S099", "store_name": "McDonald's Mong Kok Road", "district": "Kowloon City", "region": "Kowloon", "store_type": "drive_thru", "avg_daily_orders": 140, "open_date": "2009-11-20", "rent_monthly": 185000},
    {"store_id": "S100", "store_name": "McDonald's Cheung Fai Building", "district": "Kowloon City", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 94, "open_date": "2010-08-15", "rent_monthly": 200000},

    # Kowloon - Wong Tai Sin (14 stores)
    {"store_id": "S101", "store_name": "McDonald's Chuk Yuen Estate", "district": "Wong Tai Sin", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 95, "open_date": "2002-04-15", "rent_monthly": 200000},
    {"store_id": "S102", "store_name": "McDonald's Lung Cheung Road", "district": "Wong Tai Sin", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 88, "open_date": "2003-08-22", "rent_monthly": 185000},
    {"store_id": "S103", "store_name": "McDonald's Lung Poon Street", "district": "Wong Tai Sin", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 82, "open_date": "2004-01-10", "rent_monthly": 170000},
    {"store_id": "S104", "store_name": "McDonald's Lei Tung Estate", "district": "Wong Tai Sin", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 78, "open_date": "2005-06-18", "rent_monthly": 160000},
    {"store_id": "S105", "store_name": "McDonald's Kin Cheung Terrace", "district": "Wong Tai Sin", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 75, "open_date": "2006-02-25", "rent_monthly": 155000},
    {"store_id": "S106", "store_name": "McDonald's Cheung Wah Estate", "district": "Wong Tai Sin", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 92, "open_date": "2003-12-05", "rent_monthly": 195000},
    {"store_id": "S107", "store_name": "McDonald's Fung Yat Estate", "district": "Wong Tai Sin", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 85, "open_date": "2007-05-20", "rent_monthly": 175000},
    {"store_id": "S108", "store_name": "McDonald's Hong Kong Plaza", "district": "Wong Tai Sin", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 108, "open_date": "2006-09-30", "rent_monthly": 240000},
    {"store_id": "S109", "store_name": "McDonald's Tseung Kwan O", "district": "Wong Tai Sin", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 115, "open_date": "2008-03-15", "rent_monthly": 255000},
    {"store_id": "S110", "store_name": "McDonald's Kin On Estate", "district": "Wong Tai Sin", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 80, "open_date": "2009-07-08", "rent_monthly": 165000},
    {"store_id": "S111", "store_name": "McDonald's Ling Tung Estate", "district": "Wong Tai Sin", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 77, "open_date": "2010-01-22", "rent_monthly": 160000},
    {"store_id": "S112", "store_name": "McDonald's Shatin Centre", "district": "Wong Tai Sin", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 120, "open_date": "2005-11-10", "rent_monthly": 265000},
    {"store_id": "S113", "store_name": "McDonald's Sing Tao Estate", "district": "Wong Tai Sin", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 83, "open_date": "2008-10-25", "rent_monthly": 175000},
    {"store_id": "S114", "store_name": "McDonald's Ling Shan Estate", "district": "Wong Tai Sin", "region": "Kowloon", "store_type": "drive_thru", "avg_daily_orders": 135, "open_date": "2009-04-15", "rent_monthly": 170000},

    # Kowloon - Kwun Tong (16 stores)
    {"store_id": "S115", "store_name": "McDonald's Kwun Tong MTR", "district": "Kwun Tong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 110, "open_date": "2001-03-18", "rent_monthly": 230000},
    {"store_id": "S116", "store_name": "McDonald's Kwun Tong Plaza", "district": "Kwun Tong", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 125, "open_date": "2003-06-22", "rent_monthly": 280000},
    {"store_id": "S117", "store_name": "McDonald's Aeon Mall", "district": "Kwun Tong", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 132, "open_date": "2005-09-10", "rent_monthly": 295000},
    {"store_id": "S118", "store_name": "McDonald's Kowloon Bay", "district": "Kwun Tong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 105, "open_date": "2004-01-25", "rent_monthly": 215000},
    {"store_id": "S119", "store_name": "McDonald's Lam Tin Estate", "district": "Kwun Tong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 98, "open_date": "2006-02-15", "rent_monthly": 205000},
    {"store_id": "S120", "store_name": "McDonald's Yau Tong Estate", "district": "Kwun Tong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 92, "open_date": "2007-08-20", "rent_monthly": 190000},
    {"store_id": "S121", "store_name": "McDonald's Kai Yip Street", "district": "Kwun Tong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 88, "open_date": "2008-05-10", "rent_monthly": 180000},
    {"store_id": "S122", "store_name": "McDonald's Tsui Ping Estate", "district": "Kwun Tong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 85, "open_date": "2009-02-18", "rent_monthly": 175000},
    {"store_id": "S123", "store_name": "McDonald's Concordia Plaza", "district": "Kwun Tong", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 120, "open_date": "2004-10-30", "rent_monthly": 265000},
    {"store_id": "S124", "store_name": "McDonald's Tseung Kwan O Plaza", "district": "Kwun Tong", "region": "Kowloon", "store_type": "mall", "avg_daily_orders": 128, "open_date": "2006-07-15", "rent_monthly": 285000},
    {"store_id": "S125", "store_name": "McDonald's Hang On Street", "district": "Kwun Tong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 82, "open_date": "2010-03-22", "rent_monthly": 170000},
    {"store_id": "S126", "store_name": "McDonald's Po Lam Estate", "district": "Kwun Tong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 80, "open_date": "2008-11-08", "rent_monthly": 165000},
    {"store_id": "S127", "store_name": "McDonald's Kowloon City Drive-Thru", "district": "Kwun Tong", "region": "Kowloon", "store_type": "drive_thru", "avg_daily_orders": 145, "open_date": "2010-09-15", "rent_monthly": 190000},
    {"store_id": "S128", "store_name": "McDonald's Hang Fook Estate", "district": "Kwun Tong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 76, "open_date": "2011-01-20", "rent_monthly": 155000},
    {"store_id": "S129", "store_name": "McDonald's Hing Shing Street", "district": "Kwun Tong", "region": "Kowloon", "store_type": "street", "avg_daily_orders": 95, "open_date": "2007-04-12", "rent_monthly": 200000},
    {"store_id": "S130", "store_name": "McDonald's Kwun Tong Bypass", "district": "Kwun Tong", "region": "Kowloon", "store_type": "drive_thru", "avg_daily_orders": 148, "open_date": "2011-06-18", "rent_monthly": 185000},

    # New Territories - Sha Tin (12 stores)
    {"store_id": "S131", "store_name": "McDonald's New Town Plaza", "district": "Sha Tin", "region": "NT", "store_type": "mall", "avg_daily_orders": 130, "open_date": "1998-02-20", "rent_monthly": 285000},
    {"store_id": "S132", "store_name": "McDonald's Sha Tin Centre", "district": "Sha Tin", "region": "NT", "store_type": "mall", "avg_daily_orders": 125, "open_date": "2000-08-15", "rent_monthly": 275000},
    {"store_id": "S133", "store_name": "McDonald's Sha Tin Racecourse", "district": "Sha Tin", "region": "NT", "store_type": "street", "avg_daily_orders": 105, "open_date": "2002-04-10", "rent_monthly": 215000},
    {"store_id": "S134", "store_name": "McDonald's Shui Chuen O", "district": "Sha Tin", "region": "NT", "store_type": "street", "avg_daily_orders": 98, "open_date": "2003-09-20", "rent_monthly": 200000},
    {"store_id": "S135", "store_name": "McDonald's Chuen Chung Road", "district": "Sha Tin", "region": "NT", "store_type": "street", "avg_daily_orders": 92, "open_date": "2005-01-15", "rent_monthly": 185000},
    {"store_id": "S136", "store_name": "McDonald's Tai Wai Estate", "district": "Sha Tin", "region": "NT", "store_type": "street", "avg_daily_orders": 88, "open_date": "2006-06-25", "rent_monthly": 175000},
    {"store_id": "S137", "store_name": "McDonald's Fo Tan Estate", "district": "Sha Tin", "region": "NT", "store_type": "street", "avg_daily_orders": 85, "open_date": "2007-03-10", "rent_monthly": 170000},
    {"store_id": "S138", "store_name": "McDonald's Tai Chung Kiu Estate", "district": "Sha Tin", "region": "NT", "store_type": "street", "avg_daily_orders": 82, "open_date": "2008-07-18", "rent_monthly": 165000},
    {"store_id": "S139", "store_name": "McDonald's Lung Wo Road", "district": "Sha Tin", "region": "NT", "store_type": "street", "avg_daily_orders": 80, "open_date": "2009-02-22", "rent_monthly": 160000},
    {"store_id": "S140", "store_name": "McDonald's Sha Tin Wai Estate", "district": "Sha Tin", "region": "NT", "store_type": "street", "avg_daily_orders": 75, "open_date": "2010-05-15", "rent_monthly": 150000},
    {"store_id": "S141", "store_name": "McDonald's Sha Tin Drive-Thru", "district": "Sha Tin", "region": "NT", "store_type": "drive_thru", "avg_daily_orders": 140, "open_date": "2010-10-20", "rent_monthly": 180000},
    {"store_id": "S142", "store_name": "McDonald's Shui Long Wai", "district": "Sha Tin", "region": "NT", "store_type": "mall", "avg_daily_orders": 115, "open_date": "2005-11-30", "rent_monthly": 245000},

    # New Territories - Tai Po (6 stores)
    {"store_id": "S143", "store_name": "McDonald's Tai Po Centre", "district": "Tai Po", "region": "NT", "store_type": "mall", "avg_daily_orders": 115, "open_date": "2001-05-20", "rent_monthly": 240000},
    {"store_id": "S144", "store_name": "McDonald's Tai Po Mega Mall", "district": "Tai Po", "region": "NT", "store_type": "mall", "avg_daily_orders": 120, "open_date": "2005-09-10", "rent_monthly": 260000},
    {"store_id": "S145", "store_name": "McDonald's Lik Cheng Street", "district": "Tai Po", "region": "NT", "store_type": "street", "avg_daily_orders": 92, "open_date": "2003-07-15", "rent_monthly": 185000},
    {"store_id": "S146", "store_name": "McDonald's Pui To Road", "district": "Tai Po", "region": "NT", "store_type": "street", "avg_daily_orders": 85, "open_date": "2007-02-18", "rent_monthly": 170000},
    {"store_id": "S147", "store_name": "McDonald's Tai Po Industrial Estate", "district": "Tai Po", "region": "NT", "store_type": "street", "avg_daily_orders": 80, "open_date": "2008-04-22", "rent_monthly": 160000},
    {"store_id": "S148", "store_name": "McDonald's Tai Po Gateway", "district": "Tai Po", "region": "NT", "store_type": "street", "avg_daily_orders": 88, "open_date": "2006-08-30", "rent_monthly": 175000},

    # New Territories - North (6 stores)
    {"store_id": "S149", "store_name": "McDonald's Sheung Shui Centre", "district": "North", "region": "NT", "store_type": "mall", "avg_daily_orders": 110, "open_date": "2002-06-15", "rent_monthly": 225000},
    {"store_id": "S150", "store_name": "McDonald's Fanling Centre", "district": "North", "region": "NT", "store_type": "mall", "avg_daily_orders": 105, "open_date": "2004-03-20", "rent_monthly": 215000},
    {"store_id": "S151", "store_name": "McDonald's Luen Wo Market", "district": "North", "region": "NT", "store_type": "street", "avg_daily_orders": 85, "open_date": "2006-10-10", "rent_monthly": 170000},
    {"store_id": "S152", "store_name": "McDonald's Sha Tin Pass Road", "district": "North", "region": "NT", "store_type": "street", "avg_daily_orders": 80, "open_date": "2008-01-25", "rent_monthly": 160000},
    {"store_id": "S153", "store_name": "McDonald's Yuen Long Highway", "district": "North", "region": "NT", "store_type": "drive_thru", "avg_daily_orders": 135, "open_date": "2009-05-15", "rent_monthly": 165000},
    {"store_id": "S154", "store_name": "McDonald's Tai Fu Road", "district": "North", "region": "NT", "store_type": "street", "avg_daily_orders": 78, "open_date": "2010-02-20", "rent_monthly": 155000},

    # New Territories - Sai Kung (10 stores)
    {"store_id": "S155", "store_name": "McDonald's Sai Kung Town Centre", "district": "Sai Kung", "region": "NT", "store_type": "mall", "avg_daily_orders": 105, "open_date": "2002-08-20", "rent_monthly": 220000},
    {"store_id": "S156", "store_name": "McDonald's Clear Water Bay Road", "district": "Sai Kung", "region": "NT", "store_type": "street", "avg_daily_orders": 92, "open_date": "2005-02-15", "rent_monthly": 185000},
    {"store_id": "S157", "store_name": "McDonald's Tseung Kwan O Waterfront", "district": "Sai Kung", "region": "NT", "store_type": "street", "avg_daily_orders": 98, "open_date": "2006-05-18", "rent_monthly": 195000},
    {"store_id": "S158", "store_name": "McDonald's Mun Tung Road", "district": "Sai Kung", "region": "NT", "store_type": "street", "avg_daily_orders": 85, "open_date": "2007-09-22", "rent_monthly": 170000},
    {"store_id": "S159", "store_name": "McDonald's Po Lam Estate", "district": "Sai Kung", "region": "NT", "store_type": "street", "avg_daily_orders": 82, "open_date": "2008-03-10", "rent_monthly": 165000},
    {"store_id": "S160", "store_name": "McDonald's Tseung Kwan O Civic Centre", "district": "Sai Kung", "region": "NT", "store_type": "mall", "avg_daily_orders": 118, "open_date": "2003-11-25", "rent_monthly": 250000},
    {"store_id": "S161", "store_name": "McDonald's Hang Hau Estate", "district": "Sai Kung", "region": "NT", "store_type": "street", "avg_daily_orders": 80, "open_date": "2009-06-15", "rent_monthly": 160000},
    {"store_id": "S162", "store_name": "McDonald's Sai Kung Harbour", "district": "Sai Kung", "region": "NT", "store_type": "street", "avg_daily_orders": 75, "open_date": "2010-01-30", "rent_monthly": 150000},
    {"store_id": "S163", "store_name": "McDonald's Silverstrand", "district": "Sai Kung", "region": "NT", "store_type": "drive_thru", "avg_daily_orders": 130, "open_date": "2010-07-18", "rent_monthly": 175000},
    {"store_id": "S164", "store_name": "McDonald's Sai Kung Hiram's Highway", "district": "Sai Kung", "region": "NT", "store_type": "street", "avg_daily_orders": 78, "open_date": "2011-03-12", "rent_monthly": 155000},

    # New Territories - Yuen Long (8 stores)
    {"store_id": "S165", "store_name": "McDonald's Yuen Long Plaza", "district": "Yuen Long", "region": "NT", "store_type": "mall", "avg_daily_orders": 120, "open_date": "2000-10-15", "rent_monthly": 255000},
    {"store_id": "S166", "store_name": "McDonald's Yuen Long Town", "district": "Yuen Long", "region": "NT", "store_type": "street", "avg_daily_orders": 105, "open_date": "2002-12-20", "rent_monthly": 215000},
    {"store_id": "S167", "store_name": "McDonald's Long Ping Estate", "district": "Yuen Long", "region": "NT", "store_type": "street", "avg_daily_orders": 95, "open_date": "2004-06-10", "rent_monthly": 190000},
    {"store_id": "S168", "store_name": "McDonald's Tin Shui Wai", "district": "Yuen Long", "region": "NT", "store_type": "mall", "avg_daily_orders": 115, "open_date": "2003-04-25", "rent_monthly": 245000},
    {"store_id": "S169", "store_name": "McDonald's Wang Chuk Shan", "district": "Yuen Long", "region": "NT", "store_type": "street", "avg_daily_orders": 88, "open_date": "2006-01-15", "rent_monthly": 175000},
    {"store_id": "S170", "store_name": "McDonald's Lun Chuen Estate", "district": "Yuen Long", "region": "NT", "store_type": "street", "avg_daily_orders": 82, "open_date": "2007-08-20", "rent_monthly": 165000},
    {"store_id": "S171", "store_name": "McDonald's Yuen Long Highway", "district": "Yuen Long", "region": "NT", "store_type": "drive_thru", "avg_daily_orders": 138, "open_date": "2008-11-10", "rent_monthly": 180000},
    {"store_id": "S172", "store_name": "McDonald's Yuen Long Sports Centre", "district": "Yuen Long", "region": "NT", "store_type": "street", "avg_daily_orders": 92, "open_date": "2009-09-15", "rent_monthly": 185000},

    # New Territories - Tuen Mun (8 stores)
    {"store_id": "S173", "store_name": "McDonald's Tuen Mun Town Centre", "district": "Tuen Mun", "region": "NT", "store_type": "mall", "avg_daily_orders": 125, "open_date": "1999-05-15", "rent_monthly": 270000},
    {"store_id": "S174", "store_name": "McDonald's Tuen Mun Plaza", "district": "Tuen Mun", "region": "NT", "store_type": "mall", "avg_daily_orders": 120, "open_date": "2003-07-20", "rent_monthly": 260000},
    {"store_id": "S175", "store_name": "McDonald's Tuen Mun Civic Centre", "district": "Tuen Mun", "region": "NT", "store_type": "street", "avg_daily_orders": 105, "open_date": "2005-02-10", "rent_monthly": 215000},
    {"store_id": "S176", "store_name": "McDonald's Lung Mun Road", "district": "Tuen Mun", "region": "NT", "store_type": "street", "avg_daily_orders": 95, "open_date": "2006-09-18", "rent_monthly": 190000},
    {"store_id": "S177", "store_name": "McDonald's Butterfly Estate", "district": "Tuen Mun", "region": "NT", "store_type": "street", "avg_daily_orders": 88, "open_date": "2007-03-25", "rent_monthly": 175000},
    {"store_id": "S178", "store_name": "McDonald's Tuen Mun Drive-Thru", "district": "Tuen Mun", "region": "NT", "store_type": "drive_thru", "avg_daily_orders": 142, "open_date": "2009-06-20", "rent_monthly": 185000},
    {"store_id": "S179", "store_name": "McDonald's Ho Koon Estate", "district": "Tuen Mun", "region": "NT", "store_type": "street", "avg_daily_orders": 82, "open_date": "2010-01-15", "rent_monthly": 165000},
    {"store_id": "S180", "store_name": "McDonald's Tuen Mun Estate", "district": "Tuen Mun", "region": "NT", "store_type": "street", "avg_daily_orders": 78, "open_date": "2010-10-25", "rent_monthly": 155000},

    # New Territories - Tsuen Wan (8 stores)
    {"store_id": "S181", "store_name": "McDonald's Tsuen Wan Plaza", "district": "Tsuen Wan", "region": "NT", "store_type": "mall", "avg_daily_orders": 125, "open_date": "2000-03-20", "rent_monthly": 275000},
    {"store_id": "S182", "store_name": "McDonald's Tsuen Wan Town Centre", "district": "Tsuen Wan", "region": "NT", "store_type": "mall", "avg_daily_orders": 122, "open_date": "2004-08-15", "rent_monthly": 270000},
    {"store_id": "S183", "store_name": "McDonald's Shun Tak Centre", "district": "Tsuen Wan", "region": "NT", "store_type": "street", "avg_daily_orders": 108, "open_date": "2005-01-10", "rent_monthly": 220000},
    {"store_id": "S184", "store_name": "McDonald's Yeung Uk Road", "district": "Tsuen Wan", "region": "NT", "store_type": "street", "avg_daily_orders": 100, "open_date": "2006-06-20", "rent_monthly": 205000},
    {"store_id": "S185", "store_name": "McDonald's Lek Yuen Estate", "district": "Tsuen Wan", "region": "NT", "store_type": "street", "avg_daily_orders": 92, "open_date": "2007-04-18", "rent_monthly": 185000},
    {"store_id": "S186", "store_name": "McDonald's Tsuen Wan Drive-Thru", "district": "Tsuen Wan", "region": "NT", "store_type": "drive_thru", "avg_daily_orders": 140, "open_date": "2008-10-22", "rent_monthly": 180000},
    {"store_id": "S187", "store_name": "McDonald's Tsuen Wan West", "district": "Tsuen Wan", "region": "NT", "store_type": "street", "avg_daily_orders": 85, "open_date": "2009-05-15", "rent_monthly": 170000},
    {"store_id": "S188", "store_name": "McDonald's Hong Lok Estate", "district": "Tsuen Wan", "region": "NT", "store_type": "street", "avg_daily_orders": 80, "open_date": "2010-11-20", "rent_monthly": 160000},

    # New Territories - Kwai Tsing (6 stores)
    {"store_id": "S189", "store_name": "McDonald's Kwai Fong Estate", "district": "Kwai Tsing", "region": "NT", "store_type": "street", "avg_daily_orders": 95, "open_date": "2002-07-15", "rent_monthly": 200000},
    {"store_id": "S190", "store_name": "McDonald's Kwai Chung Plaza", "district": "Kwai Tsing", "region": "NT", "store_type": "mall", "avg_daily_orders": 115, "open_date": "2005-04-20", "rent_monthly": 245000},
    {"store_id": "S191", "store_name": "McDonald's Oceana Bay", "district": "Kwai Tsing", "region": "NT", "store_type": "street", "avg_daily_orders": 100, "open_date": "2008-02-10", "rent_monthly": 205000},
    {"store_id": "S192", "store_name": "McDonald's Kwai Tsing Highway", "district": "Kwai Tsing", "region": "NT", "store_type": "drive_thru", "avg_daily_orders": 135, "open_date": "2009-08-25", "rent_monthly": 175000},
    {"store_id": "S193", "store_name": "McDonald's Lai King Estate", "district": "Kwai Tsing", "region": "NT", "store_type": "street", "avg_daily_orders": 88, "open_date": "2006-09-18", "rent_monthly": 180000},
    {"store_id": "S194", "store_name": "McDonald's Ling Tong Street", "district": "Kwai Tsing", "region": "NT", "store_type": "street", "avg_daily_orders": 82, "open_date": "2010-03-22", "rent_monthly": 165000},

    # New Territories - Islands (6 stores)
    {"store_id": "S195", "store_name": "McDonald's Lantau Island", "district": "Islands", "region": "NT", "store_type": "street", "avg_daily_orders": 90, "open_date": "2007-05-15", "rent_monthly": 185000},
    {"store_id": "S196", "store_name": "McDonald's Hong Kong Disneyland", "district": "Islands", "region": "NT", "store_type": "mall", "avg_daily_orders": 125, "open_date": "2005-09-12", "rent_monthly": 280000},
    {"store_id": "S197", "store_name": "McDonald's Cheung Chau", "district": "Islands", "region": "NT", "store_type": "street", "avg_daily_orders": 70, "open_date": "2008-06-20", "rent_monthly": 140000},
    {"store_id": "S198", "store_name": "McDonald's Peng Chau", "district": "Islands", "region": "NT", "store_type": "street", "avg_daily_orders": 62, "open_date": "2009-01-15", "rent_monthly": 120000},
    {"store_id": "S199", "store_name": "McDonald's Discovery Bay", "district": "Islands", "region": "NT", "store_type": "street", "avg_daily_orders": 85, "open_date": "2006-10-30", "rent_monthly": 175000},
    {"store_id": "S200", "store_name": "McDonald's Mui Wo", "district": "Islands", "region": "NT", "store_type": "street", "avg_daily_orders": 68, "open_date": "2010-08-25", "rent_monthly": 135000},
]

# 30 menu items across 8 categories
CATEGORIES = [
    {"category_id": 1, "category_name": "Burgers"},
    {"category_id": 2, "category_name": "Chicken"},
    {"category_id": 3, "category_name": "Fries"},
    {"category_id": 4, "category_name": "Drinks"},
    {"category_id": 5, "category_name": "Breakfast"},
    {"category_id": 6, "category_name": "Desserts"},
    {"category_id": 7, "category_name": "Sides"},
    {"category_id": 8, "category_name": "Wraps"},
]

MENU_ITEMS = [
    # Burgers (5 items)
    {"item_id": 1, "item_name": "Big Mac", "category_id": 1, "unit_price": 39.90, "cogs": 17.95, "is_lto": False},
    {"item_id": 2, "item_name": "Quarter Pounder", "category_id": 1, "unit_price": 34.90, "cogs": 15.71, "is_lto": False},
    {"item_id": 3, "item_name": "McChicken Burger", "category_id": 1, "unit_price": 27.50, "cogs": 12.38, "is_lto": False},
    {"item_id": 4, "item_name": "Filet-O-Fish", "category_id": 1, "unit_price": 28.90, "cogs": 13.01, "is_lto": False},
    {"item_id": 5, "item_name": "Spicy Korean Beef Burger", "category_id": 1, "unit_price": 35.90, "cogs": 16.16, "is_lto": True},

    # Chicken (5 items)
    {"item_id": 6, "item_name": "Chicken McNuggets (6pc)", "category_id": 2, "unit_price": 25.90, "cogs": 11.66, "is_lto": False},
    {"item_id": 7, "item_name": "Chicken McNuggets (9pc)", "category_id": 2, "unit_price": 32.90, "cogs": 14.81, "is_lto": False},
    {"item_id": 8, "item_name": "Crispy Chicken Sandwich", "category_id": 2, "unit_price": 29.90, "cogs": 13.46, "is_lto": False},
    {"item_id": 9, "item_name": "Grilled Chicken Sandwich", "category_id": 2, "unit_price": 28.50, "cogs": 12.83, "is_lto": False},
    {"item_id": 10, "item_name": "Thai Chili Chicken Wrap", "category_id": 2, "unit_price": 32.50, "cogs": 14.63, "is_lto": True},

    # Fries (3 items)
    {"item_id": 11, "item_name": "Small Fries", "category_id": 3, "unit_price": 15.90, "cogs": 7.16, "is_lto": False},
    {"item_id": 12, "item_name": "Medium Fries", "category_id": 3, "unit_price": 18.90, "cogs": 8.51, "is_lto": False},
    {"item_id": 13, "item_name": "Large Fries", "category_id": 3, "unit_price": 21.90, "cogs": 9.86, "is_lto": False},

    # Drinks (4 items)
    {"item_id": 14, "item_name": "Coca-Cola Small", "category_id": 4, "unit_price": 14.50, "cogs": 4.35, "is_lto": False},
    {"item_id": 15, "item_name": "Coca-Cola Large", "category_id": 4, "unit_price": 18.50, "cogs": 5.55, "is_lto": False},
    {"item_id": 16, "item_name": "Iced Tea", "category_id": 4, "unit_price": 16.90, "cogs": 5.07, "is_lto": False},
    {"item_id": 17, "item_name": "McCafe Coffee", "category_id": 4, "unit_price": 19.90, "cogs": 5.97, "is_lto": False},

    # Breakfast (4 items)
    {"item_id": 18, "item_name": "Breakfast Burrito", "category_id": 5, "unit_price": 24.90, "cogs": 11.21, "is_lto": False},
    {"item_id": 19, "item_name": "Egg McMuffin", "category_id": 5, "unit_price": 22.50, "cogs": 10.13, "is_lto": False},
    {"item_id": 20, "item_name": "Sausage McGriddles", "category_id": 5, "unit_price": 23.90, "cogs": 10.76, "is_lto": False},
    {"item_id": 21, "item_name": "Seasonal Dim Sum Breakfast", "category_id": 5, "unit_price": 28.50, "cogs": 12.83, "is_lto": True},

    # Desserts (3 items)
    {"item_id": 22, "item_name": "Apple Pie", "category_id": 6, "unit_price": 12.90, "cogs": 5.81, "is_lto": False},
    {"item_id": 23, "item_name": "Chocolate Chip Cookie", "category_id": 6, "unit_price": 11.50, "cogs": 5.18, "is_lto": False},
    {"item_id": 24, "item_name": "McFlurry Vanilla", "category_id": 6, "unit_price": 18.90, "cogs": 8.51, "is_lto": False},

    # Sides (3 items)
    {"item_id": 25, "item_name": "Garden Salad", "category_id": 7, "unit_price": 26.50, "cogs": 11.93, "is_lto": False},
    {"item_id": 26, "item_name": "Corn Soup", "category_id": 7, "unit_price": 18.90, "cogs": 8.51, "is_lto": False},
    {"item_id": 27, "item_name": "Macaroni Salad", "category_id": 7, "unit_price": 19.90, "cogs": 8.96, "is_lto": False},

    # Wraps (3 items + LTO)
    {"item_id": 28, "item_name": "Grilled Chicken Wrap", "category_id": 8, "unit_price": 31.90, "cogs": 14.36, "is_lto": False},
    {"item_id": 29, "item_name": "Crispy Chicken Wrap", "category_id": 8, "unit_price": 32.90, "cogs": 14.81, "is_lto": False},
    {"item_id": 30, "item_name": "Asian Fusion Wrap", "category_id": 8, "unit_price": 34.50, "cogs": 15.53, "is_lto": True},
]

# Sales channels (HK-specific)
CHANNELS = [
    {"channel_id": 1, "channel_name": "counter"},
    {"channel_id": 2, "channel_name": "kiosk"},
    {"channel_id": 3, "channel_name": "mobile_app"},
    {"channel_id": 4, "channel_name": "delivery"},
    {"channel_id": 5, "channel_name": "drive_thru"},
]

# Payment methods (HK-specific: octopus is dominant, plus mainland payment apps)
PAYMENT_METHODS = [
    {"payment_id": 1, "payment_name": "cash"},
    {"payment_id": 2, "payment_name": "octopus"},
    {"payment_id": 3, "payment_name": "visa"},
    {"payment_id": 4, "payment_name": "mastercard"},
    {"payment_id": 5, "payment_name": "apple_pay"},
    {"payment_id": 6, "payment_name": "alipay"},
    {"payment_id": 7, "payment_name": "wechat_pay"},
]

# 12 Promotions across the year
PROMOTIONS = [
    {"promo_id": 1, "promo_name": "New Year Special", "promo_type": "discount", "discount_pct": 15, "start_date": "2023-01-01", "end_date": "2023-01-31", "applicable_items": "1,2,3,4,6,7,8,9"},
    {"promo_id": 2, "promo_name": "Chinese New Year Combo", "promo_type": "combo", "discount_pct": 20, "start_date": "2023-01-20", "end_date": "2023-02-05", "applicable_items": "1,2,11,12,14,15"},
    {"promo_id": 3, "promo_name": "Spring Salad Bundle", "promo_type": "combo", "discount_pct": 12, "start_date": "2023-03-01", "end_date": "2023-04-15", "applicable_items": "25,26,27"},
    {"promo_id": 4, "promo_name": "Easter Dessert BOGO", "promo_type": "bogo", "discount_pct": 50, "start_date": "2023-04-01", "end_date": "2023-04-09", "applicable_items": "22,23,24"},
    {"promo_id": 5, "promo_name": "Dragon Boat Festival Meal", "promo_type": "combo", "discount_pct": 18, "start_date": "2023-06-10", "end_date": "2023-06-25", "applicable_items": "1,2,6,7,11,12"},
    {"promo_id": 6, "promo_name": "Summer Cool Drinks", "promo_type": "discount", "discount_pct": 20, "start_date": "2023-06-01", "end_date": "2023-08-31", "applicable_items": "14,15,16"},
    {"promo_id": 7, "promo_name": "Back to School Combo", "promo_type": "combo", "discount_pct": 15, "start_date": "2023-08-15", "end_date": "2023-09-15", "applicable_items": "6,7,11,12,22,23"},
    {"promo_id": 8, "promo_name": "Mid-Autumn Festival Bundle", "promo_type": "combo", "discount_pct": 22, "start_date": "2023-09-20", "end_date": "2023-10-05", "applicable_items": "1,2,3,4,14,15"},
    {"promo_id": 9, "promo_name": "Breakfast Deal", "promo_type": "combo", "discount_pct": 25, "start_date": "2023-07-01", "end_date": "2023-09-30", "applicable_items": "18,19,20,14"},
    {"promo_id": 10, "promo_name": "Halloween Special", "promo_type": "discount", "discount_pct": 16, "start_date": "2023-10-15", "end_date": "2023-10-31", "applicable_items": "22,23,24"},
    {"promo_id": 11, "promo_name": "Thanksgiving Value Meal", "promo_type": "combo", "discount_pct": 18, "start_date": "2023-11-15", "end_date": "2023-11-30", "applicable_items": "1,2,11,12,18,19"},
    {"promo_id": 12, "promo_name": "Year-End Christmas Feast", "promo_type": "combo", "discount_pct": 25, "start_date": "2023-12-01", "end_date": "2023-12-31", "applicable_items": "1,2,3,4,6,7,11,12,22,23,24"},
]

# Hour weights for order distribution across day (7am-11pm)
HOUR_WEIGHTS = {
    7: 1,
    8: 3,
    9: 2,
    10: 4,
    11: 6,
    12: 10,
    13: 10,
    14: 8,
    15: 4,
    16: 4,
    17: 5,
    18: 9,
    19: 9,
    20: 8,
    21: 4,
    22: 3,
    23: 2,
}

# Day of week multipliers
DAY_WEIGHTS = {
    "Monday": 0.9,
    "Tuesday": 0.9,
    "Wednesday": 0.95,
    "Thursday": 1.0,
    "Friday": 1.2,
    "Saturday": 1.35,
    "Sunday": 1.3,
}

# Seasonal multipliers by month (1-12)
MONTH_WEIGHTS = {
    1: 0.9,
    2: 0.85,
    3: 1.0,
    4: 1.05,
    5: 1.1,
    6: 1.15,
    7: 1.2,
    8: 1.2,
    9: 1.1,
    10: 1.05,
    11: 1.0,
    12: 1.15,
}
