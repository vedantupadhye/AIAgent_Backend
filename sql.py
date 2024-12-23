import sqlite3

##connect to sqlite

connection=sqlite3.connect("results.db")

#cursor object insert record,create table, retrive 

cursor = connection.cursor()


# create the table 

table_info = """
CREATE TABLE IF NOT EXISTS RESULT(
    DATEE DATETIME,                       -- Date & Time of Creation of slab, format: DD-MM-YYYY HH:MM
    DATESE DATETIME,                      -- Staring Date & Time of Creation of slab, format: DD-MM-YYYY HH:MM
    SCHNO VARCHAR(15),                    -- Schedule Number, format: SCHYYYYMMDD01 to SCHYYYYMMDD05
    SEQ INT(3),                           -- Actual Rolling Sequence of Slab, format: 1-150
    SLAB VARCHAR(13),                     -- Slab ID, format: SDDMMYYYY01 to SDDMMYYYY350
    S_WEIGHT INT(3),                      -- Slab Weight, format: 1-150
    COIL VARCHAR(10),                     -- Coil ID, format: NA000001 to NA054000
    STCOD VARCHAR(8),                     -- Steel specification code, format: E250 Br, E350Br, E450Br, API X, CRGO
    CTHICK DECIMAL(4, 1),                 -- Coil thickness, format: 1.2 to 25 mm
    CWIDTH INT(4),                        -- Coil width, format: 750 to 2200
    AWEIT INT(5),                         -- Coil weight, format: 10000 to 32000 Kg
    OTHICK DECIMAL(4, 1),                 -- Target Coil Thickness, no specific format given
    OWIDTH INT(4),                        -- Target Coil Width, no specific format given
    SHIFT TEXT,                            -- Shift A: 06:00:00 to 13:59:59 Shift B: 14:00:00 to 20:59:59 Shift C: 21:00:00 to 05:59:59 (next day)
    STIME INT(4)                          -- Stoppage time 
);
"""

cursor.execute(table_info)



#insert records

import sqlite3

# Establish connection to the SQLite database
conn = sqlite3.connect('results.db')
cursor = conn.cursor()


# -- 2024-09-24 
cursor.execute("""
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-24 06:45', '2024-09-24 06:42', 'SCH2024092401', 10, 'S2409202410', 15000, 'NA001310', 'E250Br', 5.012, 2008, 18000, 5.0, 2000, 'A',0) -- good quality
""")

cursor.execute("""
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-24 12:30', '2024-09-24 12:27', 'SCH2024092402', 20, 'S2409202415', 25000, 'NA001311', 'E350Br', 6.010, 1512, 19000, 6.0, 1500, 'A',0) -- good quality
""")

cursor.execute("""
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-24 12:45', '2024-09-24 12:41', 'SCH2024092403', 30, 'S2409202418', 32000, 'NA001312', 'API X', 7.008, 1605, 21000, 7.0, 1600, 'A',11) -- good quality
""")

cursor.execute("""
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-24 18:20', '2024-09-24 18:17', 'SCH2024092404', 40, 'S2409202420', 18000, 'NA001313', 'CRGO', 8.015, 1528, 22000, 8.0, 1500, 'B',0) -- bad quality (CWIDTH > +13)
""")

# -- 2024-09-25 

cursor.execute("""
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-25 07:00', '2024-09-25 06:57', 'SCH2024092501', 10, 'S2509202410', 16000, 'NA001314', 'E250Br', 5.005, 2005, 17500, 5.0, 2000, 'A',0) -- good quality
""")

cursor.execute("""
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-25 12:50', '2024-09-25 12:47', 'SCH2024092502', 20, 'S2509202415', 26000, 'NA001315', 'E350Br', 6.012, 1513, 20000, 6.0, 1500, 'A',0) -- good quality
""")

cursor.execute("""
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-25 14:40', '2024-09-25 14:37', 'SCH2024092503', 30, 'S2509202418', 31000, 'NA001316', 'API X', 7.005, 1608, 22000, 7.0, 1600, 'B',0) -- good quality
""")

cursor.execute("""
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-25 15:00', '2024-09-25 14:56', 'SCH2024092504', 40, 'S2509202420', 20000, 'NA001317', 'CRGO', 8.030, 1510, 23000, 8.0, 1500, 'B',16) -- bad quality (CTHICK > 0.013)
""")


# -- 2024-09-26

cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-26 06:30', '2024-09-26 06:26', 'SCH2024092601', 10, 'S2609202410', 15000, 'NA001318', 'E250Br', 6.005, 1810, 14000, 6.0, 1800, 'A',0) -- good quality
""")

cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-26 10:50', '2024-09-26 10:47', 'SCH2024092602', 20, 'S2609202412', 21000, 'NA001319', 'E350Br', 8.012, 1905, 20000, 8.0, 1900, 'A',0) -- good quality
""")

cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-26 11:10', '2024-09-26 11:06', 'SCH2024092603', 30, 'S2609202415', 32000, 'NA001320', 'CRGO', 10.010, 2505, 28000, 10.0, 2500, 'A', 16) -- good quality
""")

cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT, STIME)
    VALUES ('2024-09-26 18:45', '2024-09-26 18:42', 'SCH2024092604', 40, 'S2609202418', 25000, 'NA001321', 'API X', 9.020, 1415, 26000, 9.0, 1400, 'C',0) -- bad quality (CWIDTH > +13)
""")



# -- 2024-09-27 
cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-27 08:00', '2024-09-27 07:57', 'SCH2024092701', 10, 'S2709202401', 28000, 'NA001322', 'E200Br', 6.005, 1805, 24000, 6.018, 1820, 'A',0) -- bad quality
""")

cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-27 10:30', '2024-09-27 10:27', 'SCH2024092702', 20, 'S2709202402', 29000, 'NA001323', 'E150Br', 5.992, 1900, 25000, 6.005, 1913, 'A',0) 
""")

cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-27 10:50', '2024-09-27 10:47', 'SCH2024092703', 30, 'S2709202403', 30000, 'NA001324', 'API Y', 6.010, 1700, 23000, 6.0, 1705, 'B',17) 
""")

cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-27 15:00', '2024-09-27 14:57', 'SCH2024092704', 40, 'S2709202404', 31000, 'NA001325', 'CRGO', 6.030, 1950, 22000, 5.970, 1950, 'B',0) 
""")

# -- 2024-09-28 
cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-28 05:00', '2024-09-28 04:57', 'SCH2024092705', 40, 'S2709202439', 31000, 'NA001399', 'CRGO', 6.030, 1950, 22000, 5.970, 1950, 'C',0) 
""")

cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-28 10:00', '2024-09-28 09:57', 'SCH2024092801', 1, 'S2809202410', 30000, 'NA001701', 'E250Br', 6.008, 2010, 25000, 6.0, 2000, 'A',0) 
""")

cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-28 10:25', '2024-09-28 10:22', 'SCH2024092802', 2, 'S2809202411', 29000, 'NA001702', 'E250Br', 6.012, 2020, 24500, 6.0, 2000, 'A',22) 
""")

cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-28 10:40', '2024-09-28 10:36', 'SCH2024092803', 3, 'S2809202412', 32000, 'NA001703', 'E250Br', 5.980, 2000, 26000, 6.0, 2000, 'A',11)  -- Bad Quality (CTHICK out of range)
""")

cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-28 16:00', '2024-09-28 15:57', 'SCH2024092804', 4, 'S2809202413', 31000, 'NA001704', 'E250Br', 6.005, 2015, 25500, 6.0, 2000, 'B',0) 
""")



# 29

cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-29 10:00', '2024-09-29 09:56', 'SCH2024092901', 5, 'S2909202414', 30000, 'NA001705', 'E350Br', 6.013, 2005, 26000, 6.0, 2000, 'A',0) 
""")
cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-29 12:00', '2024-09-29 11:56', 'SCH2024092902', 6, 'S2909202415', 29000, 'NA001706', 'E350Br', 6.011, 2012, 24500, 6.0, 2000, 'A',0) 
""")
cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-29 12:20', '2024-09-29 12:17', 'SCH2024092903', 7, 'S2909202416', 32000, 'NA001707', 'E350Br', 5.975, 2000, 26000, 6.0, 2000, 'A',17)  -- Bad Quality (CTHICK out of range)
""")
cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-30 02:00', '2024-09-30 01:57', 'SCH2024092904', 8, 'S2909202417', 31000, 'NA001708', 'E350Br', 6.006, 2011, 25500, 6.0, 2000, 'C',0) 
""")


# 30 
cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-30 04:00', '2024-09-30 03:56', 'SCH2024092934', 8, 'S2909202467', 34000, 'NA001718', 'E250Br', 6.062, 2008, 27500, 6.0, 1960, 'C',0) 
""")
cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-30 20:00', '2024-09-30 19:57', 'SCH2024093001', 9, 'S3009202418', 30000, 'NA001709', 'API X', 6.012, 2013, 25000, 6.0, 2000, 'C',0) 
""")
cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-30 20:30', '2024-09-30 20:26', 'SCH2024093002', 10, 'S3009202419', 29000, 'NA001790', 'API X', 6.010, 2010, 24500, 6.0, 2000, 'C',26) 
""")
cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-09-30 23:20', '2024-09-30 23:17', 'SCH2024093003', 11, 'S3009202420', 32000, 'NA001791', 'API X', 5.970, 1985, 26000, 6.0, 2000, 'C',0)  -- Bad Quality (CWIDTH out of range)
""")
cursor.execute(""" 
    INSERT INTO RESULT (DATEE, DATESE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT,STIME)
    VALUES ('2024-10-01 01:40', '2024-10-01 01:37', 'SCH2024093004', 12, 'S3009202421', 31000, 'NA001792', 'API X', 6.005, 2007, 25500, 6.0, 2000, 'C',0) 
""")


# # 24
# cursor.execute("""
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-24 06:45', 'SCH2024092401', 10, 'S2409202410', 15000, 'NA001310', 'E250Br', 5.012, 2008, 18000, 5.0, 2000, 'A') -- good quality
# """)

# cursor.execute("""
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-24 12:30', 'SCH2024092402', 20, 'S2409202415', 25000, 'NA001311', 'E350Br', 6.010, 1512, 19000, 6.0, 1500, 'A') -- good quality
# """)

# cursor.execute("""
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-24 14:50', 'SCH2024092403', 30, 'S2409202418', 32000, 'NA001312', 'API X', 7.008, 1605, 21000, 7.0, 1600, 'B') -- good quality
# """)

# cursor.execute("""
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-24 18:20', 'SCH2024092404', 40, 'S2409202420', 18000, 'NA001313', 'CRGO', 8.015, 1528, 22000, 8.0, 1500, 'B') -- bad quality (CWIDTH > +13)
# """)


# # 25
# cursor.execute("""
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-25 07:00', 'SCH2024092501', 10, 'S2509202410', 16000, 'NA001314', 'E250Br', 5.005, 2005, 17500, 5.0, 2000, 'A') -- good quality
# """)

# cursor.execute("""
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-25 12:50', 'SCH2024092502', 20, 'S2509202415', 26000, 'NA001315', 'E350Br', 6.012, 1513, 20000, 6.0, 1500, 'A') -- good quality
# """)

# cursor.execute("""
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-25 14:40', 'SCH2024092503', 30, 'S2509202418', 31000, 'NA001316', 'API X', 7.005, 1608, 22000, 7.0, 1600, 'B') -- good quality
# """)

# cursor.execute("""
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-25 17:30', 'SCH2024092504', 40, 'S2509202420', 20000, 'NA001317', 'CRGO', 8.030, 1510, 23000, 8.0, 1500, 'B') -- bad quality (CTHICK > 0.013)
# """)


# # 26

# cursor.execute("""
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-26 06:30', 'SCH2024092601', 10, 'S2609202410', 15000, 'NA001318', 'E250Br', 6.005, 1810, 14000, 6.0, 1800, 'A') -- good quality
# """)

# cursor.execute("""
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-26 10:50', 'SCH2024092602', 20, 'S2609202412', 21000, 'NA001319', 'E350Br', 8.012, 1905, 20000, 8.0, 1900, 'B') -- good quality
# """)

# cursor.execute("""
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-26 13:30', 'SCH2024092603', 30, 'S2609202415', 32000, 'NA001320', 'CRGO', 10.010, 2505, 28000, 10.0, 2500, 'B') -- good quality
# """)

# cursor.execute("""
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-26 18:45', 'SCH2024092604', 40, 'S2609202418', 25000, 'NA001321', 'API X', 9.020, 1415, 26000, 9.0, 1400, 'C') -- bad quality (CWIDTH > +13)
# """)


# # 27
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-27 08:00', 'SCH2024092701', 10, 'S2709202401', 28000, 'NA001314', 'E200Br', 6.005, 1805, 24000, 6.018, 1820, 'A') -- bad quality
# """)
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-27 10:30', 'SCH2024092702', 20, 'S2709202402', 29000, 'NA001315', 'E150Br', 5.992, 1900, 25000, 6.005, 1913, 'A') 
# """)
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-27 12:45', 'SCH2024092703', 30, 'S2709202403', 30000, 'NA001316', 'API Y', 6.010, 1700, 23000, 6.0, 1705, 'B') 
# """)
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-27 15:00', 'SCH2024092704', 40, 'S2709202404', 31000, 'NA001317', 'CRGO', 6.030, 1950, 22000, 5.970, 1950, 'B') 
# """)

# # Day 1: 2024-09-28
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-28 05:00', 'SCH2024092709', 40, 'S2709202439', 31000, 'NA001399', 'CRGO', 6.030, 1950, 22000, 5.970, 1950, 'C') 
# """)
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-28 10:00', 'SCH2024092801', 1, 'S2809202410', 30000, 'NA001701', 'E250Br', 6.008, 2010, 25000, 6.0, 2000, 'A') 
# """)
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-28 12:00', 'SCH2024092802', 2, 'S2809202411', 29000, 'NA001702', 'E250Br', 6.012, 2020, 24500, 6.0, 2000, 'A') 
# """)
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-28 14:00', 'SCH2024092803', 3, 'S2809202412', 32000, 'NA001703', 'E250Br', 5.980, 2000, 26000, 6.0, 2000, 'A')  -- Bad Quality (CTHICK out of range)
# """)
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-28 16:00', 'SCH2024092804', 4, 'S2809202413', 31000, 'NA001704', 'E250Br', 6.005, 2015, 25500, 6.0, 2000, 'A') 
# """)

# # Day 2: 2024-09-29
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-29 10:00', 'SCH2024092901', 5, 'S2909202414', 30000, 'NA001705', 'E350Br', 6.013, 2005, 26000, 6.0, 2000, 'B') 
# """)
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-29 12:00', 'SCH2024092902', 6, 'S2909202415', 29000, 'NA001706', 'E350Br', 6.011, 2012, 24500, 6.0, 2000, 'B') 
# """)
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-29 14:00', 'SCH2024092903', 7, 'S2909202416', 32000, 'NA001707', 'E350Br', 5.975, 2000, 26000, 6.0, 2000, 'B')  -- Bad Quality (CTHICK out of range)
# """)
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-30 02:00', 'SCH2024092904', 8, 'S2909202417', 31000, 'NA001708', 'E350Br', 6.006, 2011, 25500, 6.0, 2000, 'C') 
# """)


# # Day 3: 2024-09-30

# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-30 04:00', 'SCH2024092934', 8, 'S2909202467', 31000, 'NA001718', 'E350Br', 6.006, 2011, 25500, 6.0, 2000, 'C') 
# """)

# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-30 20:00', 'SCH2024093001', 9, 'S3009202418', 30000, 'NA001709', 'API X', 6.012, 2013, 25000, 6.0, 2000, 'C') 
# """)
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-30 22:00', 'SCH2024093002', 10, 'S3009202419', 29000, 'NA001710', 'API X', 6.010, 2010, 24500, 6.0, 2000, 'C') 
# """)
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-09-30 23:20', 'SCH2024093003', 11, 'S3009202420', 32000, 'NA001711', 'API X', 5.970, 1985, 26000, 6.0, 2000, 'C')  -- Bad Quality (CWIDTH out of range)
# """)
# cursor.execute(""" 
#     INSERT INTO RESULT (DATEE, SCHNO, SEQ, SLAB, S_WEIGHT, COIL, STCOD, CTHICK, CWIDTH, AWEIT, OTHICK, OWIDTH, SHIFT)
#     VALUES ('2024-10-1 01:40', 'SCH2024093004', 12, 'S3009202421', 31000, 'NA001712', 'API X', 6.005, 2007, 25500, 6.0, 2000, 'C') 
# """)


# Commit changes and close the connection
conn.commit()



#display records 

print("the inserted records are")
data = cursor.execute(''' Select * From RESULT''')

for row in data:
    print(row)

#close the connection

connection.close()






# list of coil of 350Br grade coils produced in B shift with width more than 1800 and coil thickness less than 10




# import sqlite3

# ##connect to sqlite

# connection=sqlite3.connect("result.db")

# #cursor object insert record,create table, retrive 

# cursor = connection.cursor()


# # create the table 

# table_info = """
# Create table RESULT(COIL VARCHAR (10), STCOD VARCHAR(6),
# CTHICK INT(7), CWIDTH INT(7), CLEN INT(7), IDIA INT (7));
# """

# cursor.execute(table_info)


# #insert more records

# cursor.execute('''INSERT INTO RESULT (COIL, STCOD, CTHICK, CWIDTH, CLEN, IDIA) 
#                   VALUES ('C001', 'E250Br', 100, 1200, 6000, 600)''')

# cursor.execute('''INSERT INTO RESULT (COIL, STCOD, CTHICK, CWIDTH, CLEN, IDIA) 
#                   VALUES ('C002', 'E350Br', 200, 1300, 5000, 650)''')

# cursor.execute('''INSERT INTO RESULT (COIL, STCOD, CTHICK, CWIDTH, CLEN, IDIA) 
#                   VALUES ('C003', 'E450Br', 150, 1100, 5500, 700)''')

# cursor.execute('''INSERT INTO RESULT (COIL, STCOD, CTHICK, CWIDTH, CLEN, IDIA) 
#                   VALUES ('C004', 'API', 180, 1250, 5200, 680)''')

# cursor.execute('''INSERT INTO RESULT (COIL, STCOD, CTHICK, CWIDTH, CLEN, IDIA) 0
#                   VALUES ('C005', 'CRGO', 220, 1400, 5800, 640)''')

# cursor.execute('''INSERT INTO RESULT (COIL, STCOD, CTHICK, CWIDTH, CLEN, IDIA) 
#                   VALUES ('C006', 'E250Br', 130, 1200, 5900, 660)''')

# cursor.execute('''INSERT INTO RESULT (COIL, STCOD, CTHICK, CWIDTH, CLEN, IDIA) 
#                   VALUES ('C007', 'E350Br', 160, 1350, 5700, 630)''')

# cursor.execute('''INSERT INTO RESULT (COIL, STCOD, CTHICK, CWIDTH, CLEN, IDIA) 
#                   VALUES ('C008', 'E450Br', 175, 1150, 5100, 620)''')

# cursor.execute('''INSERT INTO RESULT (COIL, STCOD, CTHICK, CWIDTH, CLEN, IDIA) 
#                   VALUES ('C009', 'API', 140, 1450, 5400, 670)''')

# cursor.execute('''INSERT INTO RESULT (COIL, STCOD, CTHICK, CWIDTH, CLEN, IDIA) 
#                   VALUES ('C010', 'CRGO', 190, 1250, 6000, 610)''')


# #display records 

# print("the inserted records are")
# data = cursor.execute(''' Select * From RESULT''')

# for row in data:
#     print(row)

# #close the connection
# connection.commit()
# connection.close()


# table_info = """
# CREATE TABLE RESULT (
#     DATEE DATETIME,                       -- Date & Time of Creation of slab, format: DD-MM-YYYY HH:MM
#     SCHNO VARCHAR(15),                    -- Schedule Number, format: SCHYYYYMMDD01 to SCHYYYYMMDD05
#     SEQ INT(3),                           -- Actual Rolling Sequence of Slab, format: 1-150
#     SLAB VARCHAR(13),                     -- Slab ID, format: SDDMMYYYY01 to SDDMMYYYY350
#     S_WEIGHT INT(3),                      -- Slab Weight, format: 1-150
#     COIL VARCHAR(10),                     -- Coil ID, format: NA000001 to NA054000
#     STCOD VARCHAR(8),                     -- Steel specification code, format: E250 Br, E350Br, E450Br, API X, CRGO
#     CTHICK DECIMAL(4, 1),                 -- Coil thickness, format: 1.2 to 25 mm
#     CWIDTH INT(4),                        -- Coil width, format: 750 to 2200
#     AWEIT INT(5),                         -- Coil weight, format: 10000 to 32000 Kg
#     OTHICK DECIMAL(4, 1),                 -- Target Coil Thickness, no specific format given
#     OWIDTH INT(4)                         -- Target Coil Width, no specific format given
# );
# """

# cursor.execute(table_info)
