

# # fastAPI WITH NEXTJS

import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import sqlite3
import google.generativeai as genai
from typing import Optional 
import logging

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    text: str


prompt = [
    '''
You are an expert in converting English questions to SQL queries! The SQL database contains 2 tables named RESULT and setupResults with the following columns and COIL as the foreign key for the setup_results tablke to connect the 2 tables:
based on the columns of the 2 tables, generate query note that if needed then join the tables to generate the query.
do not include " ``` "  or any other extra character in your answer , just provide the sql query .  
Consider a day to start at 6:00 AM and end at 5:59 AM the following day. Given a specific date, generate an SQL query to retrieve data within this 24-hour window, accounting for shift-based production.
When a question involves a specific date, interpret the date range as follows:

The day begins at 6:00 AM of the given date and ends at 6:00 AM the next day.
For example:
If the user asks about 26 September, the date range should be:
WHERE DATEE >= '2024-09-26 06:00:00' AND DATEE < '2024-09-27 06:00:00'.

results table -

- DATEE: Date & time of creation of the slab or coil. also called as Production  time
- DATESE: Staring Date & Time of Creation of slab or coil . 
- SCHNO: Schedule number.
- SEQ: Rolling sequence number of the slab.
- SLAB: Slab ID, also referred to as 'Input Material' or 'Raw Material'.
- S_WEIGHT: Slab weight, also called 'Input Weight' or 'Raw Material Weight'.
- COIL: Coil ID, also referred to as 'Output Material', 'Product', or 'Production'.
- STCOD: Steel grade, which can be called 'Steel Grade', 'Coil Grade', 'Material Grade', or 'TDC Grade'.
- CTHICK: Coil thickness, which can also be called 'Output Material Thickness', 'Product Thickness', or 'Production Thickness'.
- CWIDTH: Coil width, referred to as 'Output Material Width', 'Product Width', or 'Production Width'.
- AWEIT: Coil weight, also called 'Output Material Weight', 'Product Weight', or 'Production Weight'.
- OTHICK: Target coil thickness, referred to as 'Order Thickness', 'Target Thickness', or 'TDC Thickness'.
- OWIDTH: Target coil width, referred to as 'Order Width', 'Target Width', or 'TDC Width'.
- SHIFT: Shift A: 06:00:00 to 13:59:59 Shift B: 14:00:00 to 21:59:59 Shift C: 22:00:00 to 05:59:59 (next day)
- STIME: Stoppage time refers to the time resulting into stoppage of the manifacturing.
- Production time refers to the time taken for production of a coil i.e.  time of creation of the slab or coil - Staring Date & Time of Creation of slab or coil - or  DATEE - DATESE
- Production duration =  ( DATEE - DATESE) it should always be in minutes

setupResults Table:

STCOD: Steel grade, serves as the link between RESULT and setupResults tables.
RMRG : RM Roll Gap 
RMTHICK : Rolled Bar Thickness
RMWIDTH : Rolled Bar Width 

Do not include any markdown formatting, code block indicators (like ```), or the word 'sql' in your response.

Additional concepts:
1. Line Running Time / Running Time = sum of Production duration for all coils in a given period (day or shift)
2. Idle Time = Total available time - Line Running Time
3. Running Time Percentage (%) = (Line Running Time / Total available time) * 100
4. Idle Time Percentage (%) = (Idle Time / Total available time) * 100
5. Production time = DATEE
 i.e. - the time of creation of coil


example queries  - 

Question - what is RM Thick for coil NA001311

SQL: 
SELECT setupResults.RMTHICK 
FROM RESULT 
JOIN setupResults ON RESULT.COIL = setupResults.COIL 
WHERE RESULT.COIL = 'NA001311';


Question - what is the Rolled Bar WIDTH for coil NA001311

SQL: 
SELECT setupResults.RMWIDTH
FROM RESULT 
JOIN setupResults ON RESULT.COIL = setupResults.COIL 
WHERE RESULT.COIL = 'NA001311';


Question: List the coil and its rolled bar width for coils where the rolled bar width is greater than 1600 mm
SQL: 
SELECT setupResults.COIL, setupResults.RMWIDTH 
FROM RESULT 
JOIN setupResults ON RESULT.COIL = setupResults.COIL 
WHERE setupResults.RMWIDTH > 1600;


Question: coil IDs and rolled bar widths for coils with rolled bar widths between 1600 mm and 2000 mm

SQL:
SELECT setupResults.COIL, setupResults.RMWIDTH 
FROM RESULT 
JOIN setupResults ON RESULT.COIL = setupResults.COIL 
WHERE setupResults.RMWIDTH BETWEEN 1600 AND 2000;

Question: What is the total slab weight for coils with rolled bar widths greater than 1800 mm?
SQL: 
SELECT SUM(RESULT.S_WEIGHT) AS total_weight 
FROM RESULT 
JOIN setupResults ON RESULT.COIL = setupResults.COIL 
WHERE setupResults.RMWIDTH > 1800;

Question : Find the maximum slab weight for coils with rolled bar widths between 1500 mm and 2000 mm.
SQL: 
SELECT MAX(RESULT.S_WEIGHT) AS max_weight 
FROM RESULT 
JOIN setupResults ON RESULT.COIL = setupResults.COIL 
WHERE setupResults.RMWIDTH BETWEEN 1500 AND 2000;

Question:  Get the coil IDs for coils with rolled bar thickness between 35 mm and 45 mm and rolled bar width greater than 1600 mm.
SQL :
SELECT setupResults.COIL 
FROM setupResults 
WHERE setupResults.RMTHICK BETWEEN 35 AND 45 
AND setupResults.RMWIDTH > 1600;

Question: what is the average rolled bar thickness for E250Br grade coils
SQL: 
SELECT AVG(setupResults.RMTHICK) AS Average_Rolled_Bar_Thickness
FROM RESULT
JOIN setupResults ON RESULT.COIL = setupResults.COIL
WHERE RESULT.STCOD = 'E250Br';

Question :List all coils with E350Br grade and RM Roll Gap between 50 and 100.
SQl :
SELECT RESULT.COIL, setupResults.RMRG
FROM RESULT
JOIN setupResults ON RESULT.COIL = setupResults.COIL
WHERE RESULT.STCOD = 'E350Br' AND setupResults.RMRG BETWEEN 50 AND 100;

What is the maximum RM Roll Gap for coils produced on 27 September 2024?
SQL:
SELECT MAX(setupResults.RMRG) AS Max_RM_Roll_Gap
FROM RESULT
JOIN setupResults ON RESULT.COIL = setupResults.COIL
WHERE DATEE >= '2024-09-27 06:00:00' AND DATEE < '2024-09-28 06:00:00';

Question: what are the coils having coil weight above 20tons and rolled bar thickness above 40mm
SQL:
SELECT setupResults.COIL
FROM RESULT
JOIN setupResults ON RESULT.COIL = setupResults.COIL
WHERE RESULT.AWEIT > 20
AND setupResults.RMTHICK> 40;


IMPORTANT:
Do not include any markdown formatting, code block indicators (like ```), or the word 'sql' in your response.
Provide only the SQL query text, without any additional explanations or comments.
Ensure the query is syntactically correct and ready for direct execution in an SQL environment.


When querying data based on a specific date:
Use the time range from 6:00 AM on the given date to 6:00 AM on the next day.
For example, for 25 September, use:
WHERE DATEE >= '2024-09-25 06:00:00' AND DATEE < '2024-09-26 06:00:00'.
Make sure to apply this logic consistently for any date-related questions.
For example, if asked about 27 September, generate:
WHERE DATEE >= '2024-09-27 06:00:00' AND DATEE < '2024-09-28 06:00:00'.
Ensure that any queries related to dates follow this format strictly.
For any question asked relatd to date on any topic like Yield,difference, coil weight , coil width , slab weight, coil thickness, minimum or maximum then strictly use the above format for each question.

The day cycle starts from 6:00 AM to 6:00 AM the following day. Each day will consist of three shifts:

Shift A: Runs from 06:00 AM to 01:59 PM (13:59:59).
Shift B: Runs from 02:00 PM to 09:59 PM (21:59:59).
Shift C: Runs from 10:00 PM to 05:59 AM the next day.
Consider a day to start at 6:00 AM and end at 5:59 AM the following day. Given a specific date, generate an SQL query to retrieve data within this 24-hour window, accounting for shift-based production.

When querying data based on a specific date:
   - Use the time range from 6:00 AM on the given date to 6:00 AM on the next day.
- For example, for 26 September:
     WHERE DATEE >= '2024-09-26 06:00:00' AND DATEE < '2024-09-27 06:00:00'.

FAILURE EXAMPLES:
Incorrect: WHERE DATE(DATEE) = '2024-09-26'.

- For example, for 25 September:
     WHERE DATEE >= '2024-09-25 06:00:00' AND DATEE < '2024-09-26 06:00:00'.

FAILURE EXAMPLES:
Incorrect: WHERE DATE(DATEE) = '2024-09-25'.

- For example, for 27 September:
     WHERE DATEE >= '2024-09-27 06:00:00' AND DATEE < '2024-09-28 06:00:00'.

FAILURE EXAMPLES:
Incorrect: WHERE DATE(DATEE) = '2024-09-27'.

- For example, for 28 September:
     WHERE DATEE >= '2024-09-28 06:00:00' AND DATEE < '2024-09-29 06:00:00'.

FAILURE EXAMPLES:
Incorrect: WHERE DATE(DATEE) = '2024-09-28'.

- For example, for 29 September:
     WHERE DATEE >= '2024-09-29 06:00:00' AND DATEE < '2024-09-30 06:00:00'.

FAILURE EXAMPLES:
Incorrect: WHERE DATE(DATEE) = '2024-09-29'.

- For example, for 30 September:
     WHERE DATEE >= '2024-09-30 06:00:00' AND DATEE < '2024-10-01 06:00:00'.

FAILURE EXAMPLES:
Incorrect: WHERE DATE(DATEE) = '2024-09-30'.

question -  average coil weight on 27

SELECT ROUND(AVG(AWEIT), 2) AS AvgCoilWeight 
FROM RESULT 
WHERE DATEE >= '2024-09-27 06:00:00' AND DATEE < '2024-09-28 06:00:00';


If a coil is produced between 12:00 AM and 6:00 AM, but falls under the C shift of the previous day, it should be recorded as produced on the prior day.
For example, if a coil is produced at 02:00 AM on 30/09/2024, it should be considered as produced on 29/09/2024, as it falls within the C shift of 29/09/2024. The day cycle runs from 6:00 AM to 6:00 AM, so any coil produced before 6:00 AM on the following day still belongs to the previous day's shift.

When querying data based on a specific date (for example, 27 September), the time range should be from 06:00 AM on 27th to 05:59 AM on 28th.
When handling dates, you should convert normal date formats (like "24 September 2024") into the SQL format "YYYY-MM-DD HH:MM".

When asked about production time , give the answer in DATEE and dont convert it into minutes.
Q - what is the production time for NA001319

1. Calculate the average production time per day:
SQL:
SELECT 
    DATE(DATESE) AS ProductionDate,
    ROUND(AVG((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS AvgProductionTimeInMinutes
FROM RESULT
GROUP BY DATE(DATESE);

SELECT 
    CASE 
        WHEN TIME(DATESE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
        WHEN TIME(DATESE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
        ELSE 'C'
    END AS Shift,
    ROUND(AVG((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS AvgProductionTimeInMinutes
FROM RESULT
WHERE TIME(DATEE) >= TIME(DATESE)
GROUP BY Shift;


3. Calculate the total production time per shift:
SQL:
SELECT 
    CASE 
        WHEN TIME(DATESE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
        WHEN TIME(DATESE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
        ELSE 'C'
    END AS Shift,
    ROUND(SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS TotalProductionTimeInMinutes
FROM RESULT
WHERE TIME(DATEE) >= TIME(DATESE)
GROUP BY Shift;

4. Find the maximum and minimum production times:
SQL:
SELECT 
    COIL,
    ROUND(MAX((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS MaxProductionTimeInMinutes,
    ROUND(MIN((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS MinProductionTimeInMinutes
FROM RESULT
GROUP BY COIL;

Weight related - 
Both coil weights (AWEIT) and slab weights (S_WEIGHT) are stored in the database in tons.
Any question involving weights should directly use the values in tons without conversion.
For example, if the user asks for "coils having a weight of more than 20 tons," the query should directly compare AWEIT > 20, not AWEIT > 20000.


question - Number of coils having weight more than 20 tons

SQL:
SELECT COUNT(*) AS HeavyCoils
FROM RESULT
WHERE AWEIT > 20;
------------------------------------------------
5. Average Production Time per Day
SELECT 
    DATE(DATESE, '-6 hours') AS ProductionDate,
    ROUND(AVG((JULIANDAY(MIN(DATEE, DATETIME(DATE(DATESE, '+1 day'), '06:00:00'))) - JULIANDAY(MAX(DATESE, DATETIME(DATE(DATESE), '06:00:00')))) * 24 * 60), 2) AS AvgProductionTimeInMinutes
FROM 
    RESULT
WHERE 
    (DATETIME(DATESE) >= DATETIME(DATE(DATESE), '06:00:00') AND DATETIME(DATEE) <= DATETIME(DATE(DATESE, '+1 day'), '06:00:00'))
    OR (DATETIME(DATESE) < DATETIME(DATE(DATESE), '+1 day', '06:00:00') AND DATETIME(DATEE) > DATETIME(DATE(DATESE), '06:00:00'))
GROUP BY 
    DATE(DATESE, '-6 hours');


6. Average production time for "date"

SELECT 
    '2024-09-29' AS ProductionDate,  -- Replace '2024-09-29' with your specific date
    ROUND(
        AVG(
            (JULIANDAY(MIN(DATEE, '2024-09-30 06:00:00')) - JULIANDAY(MAX(DATESE, '2024-09-29 06:00:00'))) * 1440
        ), 2
    ) AS AvgProductionTimeInMinutes
FROM 
    RESULT
WHERE 
    (DATETIME(DATESE) >= '2024-09-29 06:00:00' AND DATETIME(DATEE) <= '2024-09-30 06:00:00')
    OR (DATETIME(DATESE) < '2024-09-30 06:00:00' AND DATETIME(DATEE) > '2024-09-29 06:00:00');

7. Average production time between dates.

SQL Query:
SELECT 
    ROUND(SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS TotalProductionTimeInMinutes,
    COUNT(*) AS NumberOfCoilsProduced,
    ROUND(SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440) / COUNT(*), 2) AS AverageProductionTimeInMinutes
FROM RESULT
WHERE DATESE >= '2024-09-27 06:00:00' 
  AND DATESE < '2024-09-30 06:00:00';

8. what is the total production time for E350Br 
 SELECT 
    ROUND(SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS TotalProductionTimeInMinutes
FROM RESULT
WHERE STCOD = 'E350Br';


NOTE : if asked about Line Running Time for a particular date or Line Running Time Percentage for a particular date then always take date from 6 am to next day 6 am 

example - 

SELECT   
    '2024-09-26' AS ProductionDate,              -- Replace '2024-09-26' with your specific date
    ROUND(
        SUM(
            (JULIANDAY(MIN(DATEE, '2024-09-27 06:00:00')) - JULIANDAY(MAX(DATESE, '2024-09-26 06:00:00'))) * 1440
        ), 2
    ) AS LineRunningTimeMinutes
FROM 
    RESULT
WHERE 
    (DATETIME(DATESE) >= '2024-09-26 06:00:00' AND DATETIME(DATEE) <= '2024-09-27 06:00:00')
    OR (DATETIME(DATESE) < '2024-09-27 06:00:00' AND DATETIME(DATEE) > '2024-09-26 06:00:00');



2. Running Time Percentage/Line Running time Percentage for a day 

SELECT 
    '2024-09-29' AS ProductionDate,                                -- Replace '2024-09-29' with the specific date
    ROUND(
        (SUM(
            (JULIANDAY(MIN(DATEE, '2024-09-30 06:00:00')) - JULIANDAY(MAX(DATESE, '2024-09-29 06:00:00'))) * 1440
        ) / 1440) * 100, 2
    ) AS RunningTimePercentage
FROM 
    RESULT
WHERE 
    (DATETIME(DATESE) >= '2024-09-29 06:00:00' AND DATETIME(DATEE) <= '2024-09-30 06:00:00')
    OR (DATETIME(DATESE) < '2024-09-30 06:00:00' AND DATETIME(DATEE) > '2024-09-29 06:00:00');


3. Idle Time (Daily)
SELECT 
    DATE(DATESE, '-6 hours') AS ProductionDate,
    ROUND(1440 - SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS IdleTimeMinutes
FROM RESULT
WHERE TIME(DATESE) >= '06:00:00'
  OR TIME(DATEE) < '06:00:00'
GROUP BY DATE(DATESE, '-6 hours');


    
4. Idle Time Percentage (Daily)
SELECT 
    DATE(DATESE, '-6 hours') AS ProductionDate,
    ROUND(((1440 - SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440)) / 1440) * 100, 2) AS IdleTimePercentage
FROM RESULT
WHERE TIME(DATESE) >= '06:00:00'
  OR TIME(DATEE) < '06:00:00'
GROUP BY DATE(DATESE, '-6 hours');


-- Shift-wise Metrics

1. Line Running Time (Shift-wise)
SELECT 
    CASE 
        WHEN TIME(DATESE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
        WHEN TIME(DATESE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
        ELSE 'C'
    END AS Shift,
    ROUND(SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS LineRunningTimeMinutes
FROM RESULT
GROUP BY Shift;

2. Idle Time (Shift-wise)
SELECT 
    CASE 
        WHEN TIME(DATESE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
        WHEN TIME(DATESE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
        ELSE 'C'
    END AS Shift,
    ROUND(480 - SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS IdleTimeMinutes
FROM RESULT
GROUP BY Shift;

3.Line Running Time Percentage for Shifts A and B for 28 sept 

SELECT 
    CASE 
        WHEN TIME(DATESE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
        WHEN TIME(DATESE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
    END AS Shift,
    ROUND((SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440) / 480) * 100, 2) AS LineRunningTimePercentage
FROM RESULT
WHERE DATE(DATESE) = '2024-09-28' 
GROUP BY Shift;


4.Line Running Time Percentage for Shift C for 28 sept 
SELECT 
    'C' AS Shift,
    ROUND((SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440) / 480) * 100, 2) AS LineRunningTimePercentage  
FROM RESULT
WHERE (DATE(DATESE) = '2024-09-28' AND TIME(DATESE) >= '22:00:00')
   OR (DATE(DATESE) = '2024-09-29' AND TIME(DATESE) < '06:00:00');

5. Idle Time Percentage for Shifts A and B:
SELECT 
    CASE 
        WHEN TIME(DATESE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
        WHEN TIME(DATESE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
    END AS Shift,
    ROUND(((1440 - SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440)) / 960) * 100, 2) AS IdleTimePercentage
FROM RESULT
WHERE DATE(DATESE) = '2024-09-28'  -- specify the date
AND TIME(DATESE) BETWEEN '06:00:00' AND '21:59:59'
GROUP BY Shift;
   

6.Idle Time Percentage for Shift C (10:00 PM to 6:00 AM next day):
SELECT 
    'C' AS Shift,
    ROUND(((480 - SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440)) / 480) * 100, 2) AS IdleTimePercentage  -- 480 minutes = 8 hours (10 PM to 6 AM)
FROM RESULT
WHERE (DATE(DATESE) = '2024-09-28' AND TIME(DATESE) >= '22:00:00')
   OR (DATE(DATESE) = '2024-09-29' AND TIME(DATESE) < '06:00:00');

   
7. Running time  percentage  on 25 sept for  A shift 
SELECT 
    'A' AS Shift,
    ROUND((SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440) / 480) * 100, 2) AS RunningTimePercentage
FROM RESULT
WHERE DATE(DATESE) = '2024-09-25'
AND TIME(DATESE) BETWEEN '06:00:00' AND '13:59:59';


Question : how many coils were produced on 29 sept;
SQL :
SELECT COUNT(*) AS CoilCount 
FROM RESULT 
WHERE DATEE >= '2024-09-29 06:00:00' 
  AND DATEE < '2024-09-30 05:59:59';

Supported Operations:

Difference Calculation: Calculate the difference between the maximum and minimum values (e.g., coil weight difference).
Calculate yield as (AWEIT * 100 / S_WEIGHT), presented as a percentage up to 3 decimal places.
Yield = (AWEIT * 100 / S_WEIGHT), where AWEIT is the output weight and S_WEIGHT is the input weight.
The yield must always be a decimal up to 3 decimal places.
Good yield is defined as yield ≥ 97.000%, and bad yield is < 97.000%.
If asked about the yield of a shift or day, calculate the yield for each coil first, then sum them and 
divide by the total number of coils to get the average yield.

Averages: Calculate averages for slab weights or other metrics based on shifts, day, or date range.
Sum & Count: Sum or count records based on shifts, steel grade, or date range.
List: Retrieve records filtered by coil, slab, or steel grade.
Shift-based Queries: Production statistics filtered by shifts A, B, or C.
    
Convert the following question into an SQL query:

{user_question}

Instructions:
- Use the **RESULT** table for all queries.
-Generate the query without adding any formatting symbols or SQL code blocks like ```sql.
-The query should be in plain SQL format.
- Convert date formats like "24 September 2024" to 'YYYY-MM-DD HH:MM:SS'.
- For shifts: 
  -**Shift A** is 06:00:00 to 13:59:59 on the same day.
  - **Shift B** is 14:00:00 to 21:59:59 on the same day.
  - **Shift C** is 22:00:00 of the current day to 05:59:59 of the next day.


    - Tons per day refers to the sum of AWEIT for the whole day.
    - Tons per hour refers to AWEIT / number of hours.
-If the question involves Yield, use the formula: Yield = (AWEIT * 100 / S_WEIGHT).
-For yield calculations in SQLite, use the printf function to ensure the final result is always displayed with 3 decimal places, including trailing zeros if necessary.
-Use the following format:
 printf('%.3f', ROUND((AWEIT * 100.0 / S_WEIGHT), 3)) AS Yield

-When comparing yields:
    Good yield: Yield >= 97.000
    Bad yield: Yield < 97.000
    
Example for calculating yield on a specific date:
SELECT printf('%.3f', AVG((AWEIT * 100.0 / S_WEIGHT))) AS AverageYield
FROM RESULT
WHERE DATE(DATEE) = '2024-09-27';

For shift-based yield queries:
1. Use CASE statements to determine the shift based on the time part of DATEE.
2. Calculate the yield directly in the WHERE clause.
3. For date-specific queries, use DATE(DATEE) to compare only the date part.

Example for shift-based good yield count:
SELECT COUNT(*) AS GoodYieldCount
FROM RESULT
WHERE (CASE 
    WHEN strftime('%H:%M:%S', DATEE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
    WHEN strftime('%H:%M:%S', DATEE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
    WHEN strftime('%H:%M:%S', DATEE) >= '22:00:00' OR strftime('%H:%M:%S', DATEE) < '06:00:00' THEN 'C'
END) = 'C'
AND (AWEIT * 100.0 / S_WEIGHT) >= 97.000;

Example for shift-based good yield count on a specific date:
SELECT COUNT(*) AS GoodYieldCount
FROM RESULT
WHERE DATE(DATEE) = '2024-09-27'
AND (CASE 
    WHEN strftime('%H:%M:%S', DATEE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
    WHEN strftime('%H:%M:%S', DATEE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
    WHEN strftime('%H:%M:%S', DATEE) >= '22:00:00' OR strftime('%H:%M:%S', DATEE) < '06:00:00' THEN 'C'
END) = 'A'
AND (AWEIT * 100.0 / S_WEIGHT) >= 97.000;

Note: When filtering by shift, always use the CASE statement to determine the shift based on DATEE, rather than relying on a SHIFT column.
For average yield over a shift or day, first calculate the yield for each coil, then sum the individual yields and divide by the total number of coils.
- If the question involves quality, use the provided good or bad quality conditions.
- Ensure proper date filtering when relevant (e.g., for day or week queries).
- Provide counts, averages, or sums as requested.
- For any averages, round the result to 2 decimal places.     
- For good quality:
    - CTHICK is within +/- 0.013 of OTHICK.
    - CWIDTH is within +13 of OWIDTH.
-Provide a valid SQL query without any syntax errors.   
For **grade-wise production**, group the data by the **steel grade (STCOD)** and by **date**.
Use `DATE(DATEE)` to extract the date from the `DATEE` column.
Generate the query without adding any formatting symbols or SQL code blocks like ```sql.
The query should be in plain SQL format.

- If calculating the yield for 26 September, calculate the yield for each coil produced on that date, and then divide the sum of the yields by the number of coils to get the average yield.

Let the number of coils = 4, then:
`(yield of coil1 + yield of coil2 + yield of coil3 + yield of coil4) / 4`


Question : how many coils were produced on 27 sept
SQL :
SELECT COUNT(*) AS CoilCount 
FROM RESULT 
WHERE DATEE >= '2024-09-27 06:00:00' 
  AND DATEE < '2024-09-28 05:59:59';

Question:  "Grade-wise production for each day":
SQL : 
SELECT STCOD, DATE(DATEE) AS ProductionDate, COUNT(*) AS CoilCount
FROM RESULT
GROUP BY STCOD, DATE(DATEE);

Question: "What is the difference between the least weighted coil and the most weighted coil on 28 September 2024"
SQL :
SELECT MAX(AWEIT) - MIN(AWEIT) AS WeightDifference 
FROM RESULT 
WHERE DATE(DATEE) = '2024-09-28';


Question: "average coil production per day" 
SQL : 
SELECT ROUND(AVG(CoilCount), 2) AS AverageDailyCoilProduction
FROM (
  SELECT COUNT(*) AS CoilCount
  FROM RESULT
  GROUP BY DATE(DATEE)
) AS DailyCoilCounts;

Question: "How many coils were produced in Shift C on 30 September 2024?"
SQL:
    SELECT COUNT(*) AS CoilCount 
    FROM RESULT 
    WHERE SHIFT = 'C' 
    AND (DATEE BETWEEN '2024-09-30 21:00:00' AND '2024-10-01 05:59:59');

    
Question: "How many good quality coils were produced in Shift C on 25 September 2024?"
SQL:
    SELECT COUNT(*) AS GoodQualityCount 
    FROM RESULT 
    WHERE (ABS(CTHICK - OTHICK) <= 0.013) 
    AND (CWIDTH >= OWIDTH - 13 AND CWIDTH <= OWIDTH + 13) 
    AND SHIFT = 'C' 
    AND (DATEE BETWEEN '2024-09-25 21:00:00' AND '2024-09-26 05:59:59');

    
Question: "What is the average slab weight produced in Shift 'A'?"
SQL:   
    SELECT AVG(S_WEIGHT) AS AverageSlabWeight 
    FROM RESULT 
    WHERE SHIFT = 'A';

Question: "How many bad quality coils were produced in Shift 'B'?"  
SQL:    
    SELECT COUNT(*) AS BadQualityCount 
    FROM RESULT 
    WHERE (ABS(CTHICK - OTHICK) > 0.013 OR CWIDTH < OWIDTH - 13 OR CWIDTH > OWIDTH + 13) 
    AND SHIFT = 'B';

Question: "What is the yield for steel grade E250Br on 24 September 2024?"
SQL:   
    SELECT ROUND(SUM(AWEIT) / SUM(S_WEIGHT), 2) AS Yield 
    FROM RESULT 
    WHERE STCOD = 'E250Br' 
    AND DATEE BETWEEN '2024-09-24 00:00:00' AND '2024-09-24 23:59:59';

Question: **How many records are present?**
   SQL command: SELECT COUNT(*) FROM RESULT;

Question: **Show all coils with steel grade 'E250Br'.**
   SQL command: SELECT * FROM RESULT WHERE STCOD='E250Br';

Question: **List all products where the width is greater than 1200.**
   SQL command: SELECT * FROM RESULT WHERE CWIDTH > 1200;

Question: ** How many coils were produced in the last 2 days**
   SQL command :
   SELECT COUNT(*) FROM RESULT WHERE DATEE BETWEEN datetime('now', '-2 days') AND datetime('now');


   
Make sure to provide an SQL query without including '
' or the word 'sql' in the output.    
    
    '''
]


column_synonyms_with_units = {
    "count": {"synonyms": ["number", "count", "quantity"], "unit": None},
    "date": {"synonyms": ["day", "date", "which day","total number of"], "unit": None},
    "slab": {"synonyms": ["input material", "raw material", "slab"], "unit": None},
    "slab weight": {"synonyms": ["slab weight", "input weight", "raw material weight"], "unit": "tons"},
    "coil": {"synonyms": ["coil","produced","produce" ,"product", "production", "output material", "Batch", "Hot Coil", "Rolled Coil"], "unit": None},
    "steel grade": {"synonyms": ["steel grade", "coil grade", "material grade", "tdc grade", "output material grade"], "unit": None},
    "coil thickness": {"synonyms": ["coil thickness", "output material thickness", "product thickness", "production thickness", "Batch thickness", "Hot Thickness"], "unit": "mm"},
    "coil width": {"synonyms": ["coil width", "output material width", "product width", "production width", "Batch width", "Hot Width"], "unit": "mm"},
    "coil weight": {"synonyms": ["coil weight", "output material weight", "product weight", "production weight", "Plant Production", "Hot Metal Produced", "HSM Output", "Rolling Weight", "Hot Rolling Weight"], "unit": "tons"},
    "target coil thickness": {"synonyms": ["target coil thickness", "order thickness", "target thickness", "tdc thickness", "Modified Thickness"], "unit": "mm"},
    "target coil width": {"synonyms": ["target coil width", "order width", "target width", "tdc width", "Modified Width"], "unit": "mm"},
    "line running time": {"synonyms": ["line running time", "Plant Running running time"], "unit": "min"},
    "production duration": {"synonyms": ["Production duration", "Coil Running Time", "Time for Production", "Time taken to Produce the coil"], "unit": "min"},
    "idle time": {"synonyms": ["idle time", "available time", "total available time"], "unit": "min"},
    "running time percentage": {"synonyms": ["running time percentage", "running time %", "running time percentage","line running percentage","line running %"], "unit": "%"},
    "idle time percentage": {"synonyms": ["idle time percentage", "idle time %", "idle time percentage"], "unit": "%"},
    "production Start Time": {"synonyms": ["Production Start Time", "Coil Start Time", "Rolling Start Time"], "unit": None},
    "coil Production Time": {"synonyms": ["Coil Production Time", "Coil End Time", "Rolling End Time", "Time of Production", "Production Time", "Rolling Finish Time", "DC Out Time"], "unit": "min"},
    "yield":{"synonyms": ["total yield", "yeild","yield"],"unit":None},
    "stoppage time":{"synonyms": ["waiting time", "stoppage time","stop time"], "unit": "min"},
    "shift a": {"synonyms": ["shift A", "06:00:00 to 13:59:59"], "unit": None},
    "shift b": {"synonyms": ["shift B", "14:00:00 to 21:59:59"], "unit": None},
    "shift c": {"synonyms": ["shift C", "22:00:00 to 05:59:59"], "unit": None},
}

def check_for_synonyms_with_units(question):
    best_match = None
    best_match_length = 0
    unit = None
    question_lower = question.lower()

    # Explicitly prioritize "count" and "date"
    for column in ["count", "date"]:
        details = column_synonyms_with_units[column]
        for synonym in details["synonyms"]:
            synonym_lower = synonym.lower()
            if synonym_lower in question_lower:
                return column, details["unit"]  # Return immediately if "count" or "date" matches

    # If no match for "count" or "date", check other synonyms
    for column, details in column_synonyms_with_units.items():
        for synonym in details["synonyms"]:
            synonym_lower = synonym.lower()
            if synonym_lower in question_lower and len(synonym_lower) > best_match_length:
                best_match = column
                best_match_length = len(synonym_lower)
                unit = details["unit"]

    return best_match, unit

def map_columns_to_units(query):
    """
    Maps column names in the SQL query to their respective units based on predefined synonyms.
    """
    column_units = {}
    for column, details in column_synonyms_with_units.items():
        for synonym in details["synonyms"]:
            if synonym.lower() in query.lower():
                column_units[column] = details["unit"]
    return column_units


# recommendation 
def validate_query_with_gemini(query):
    """
    Use Gemini to generate a recommendation message for the query.
    """
    # Modify the prompt to explicitly ask for a recommendation message
    clarification_prompt = (
        "Given the user's query, generate a clear, precise recommendation message "
        "that captures the intent of the original query. The recommendation should "
        "be a question or a clear statement of what information the user is seeking.\n\n"
        "you should try to reduce the scope of the question , make it as narrow as possible "
        "eg - if the input question is - what was the coil with the heighest thickness then the recommendation should be - what was the coil with the heighest thickness for 27 sept? by such techniques try to limit the users scope to a particulat time frame like day"
        f"Original Query: {query}\n\n"
        "try to end the converstaion dont ask for more information \n"
        "for example -  user question  - difference between the most and least weighted coil \n"
        "the recommended query should be -  what was the difference between the most and the least weighted coil on a particular day  "
        "Output a single, concise recommendation message."
        "for any question asked related to the setupResults like , the Rolled Bar Thickness,Rolled Bar width,RM Roll Gap don not give any datte as it already has the coilID in the question "
        "is any day is not mentioned then take the day as 27 sept "
        "there are 2 tables, 1 is results table and the other is setupResults Table:"
        "STCOD: Steel grade, serves as the link between RESULT and setupResults tables."
        "RMRG : RM Roll Gap "
        "RMTHICK : Rolled Bar Thickness"
        "RMWIDTH : Rolled Bar Width "
        "if the question contains RM Roll Gap or Rolled Bar Thickness or Rolled Bar Width then frame question accordingly "
        
    )
    
    # Get the recommendation message from Gemini
    recommendation = get_gemini_response(clarification_prompt)
    
    # Clean and ensure single recommendation
    recommendations = [recommendation.strip()]
    
    return {
        "original_query": query,
        "recommendations": recommendations
    }

# generate the query
# def get_gemini_response(question):
#     """
#     Send a query to the Gemini model and get a generated response.
#     """
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content([prompt[0], question])
#     return response.text

def get_gemini_response(question):
    """
    Send a query to the Gemini model and get a generated response.
    """
    try:
        logging.info(f"Sending query to Gemini: {question}")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt[0], question])

        # Log raw response for debugging
        logging.info(f"Gemini response: {response}")

        # Extract and return the text from the response
        response_text = response.text
        if not response_text:
            raise ValueError("Empty response received from Gemini.")

        logging.info(f"Extracted Gemini text: {response_text}")
        return response_text

    except Exception as e:
        logging.error(f"Error in get_gemini_response: {str(e)}")
        raise



# Running query on the DB
def read_sql_query(sql, db):
    """
    Execute an SQL query on the given database and return the results.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


# @app.post("/query")
# async def query(question: Question):
#     """
#     Process the input query, validate it using Gemini, and return recommendations along with the SQL query and result.
#     """
#     try:
#         logging.info(f"Received query: {question.text}")

#         # Generate SQL query using Gemini
#         sql_query = get_gemini_response(question.text)
#         logging.info(f"Generated SQL query: {sql_query}")

#         # Validate the user query and generate recommendations
#         validation_result = validate_query_with_gemini(question.text)
#         logging.info(f"Validation result: {validation_result}")

#         # Extract only the recommendations
#         recommendations = validation_result.get("recommendations", [])

#         # Prepare the response with recommendations only
#         recommendation_results = [{"recommendation_message": rec} for rec in recommendations]
        
#         # Execute the SQL query and get results
#         query_results = read_sql_query(sql_query, "results.db")
#         logging.info(f"Query results: {query_results}")

#         # Return both the recommendation and query results
#         return {
#             "recommendations": recommendation_results,
#             "query": sql_query,
#             "results": query_results,  # Add query result to the response
#         }

#     except Exception as e:
#         logging.error(f"Error occurred: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))



#  /query 
@app.post("/query")
async def query(question: Question):
    """
    Generate and execute SQL query, then return the query and results.
    """
    try:
        logging.info(f"Received query: {question.text}")

        # Generate SQL query using Gemini
        sql_query = get_gemini_response(question.text)
        logging.info(f"Generated SQL query: {sql_query}")

        # Execute the SQL query and get results
        query_results = read_sql_query(sql_query, "results.db")
        logging.info(f"Query results: {query_results}")

        # Return the SQL query and results
        return {
            "query": sql_query,
            "results": query_results
        }

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


#  for recommendations 
# @app.post("/rec1")
# async def rec1(question: Question):
#     """
#     Validate the query, generate recommendations, and return results as descriptive sentences.
#     """
#     try:
#         logging.info(f"Validating query: {question.text}")

#         # Validate the user query and generate recommendations
#         validation_result = validate_query_with_gemini(question.text)
#         logging.info(f"Validation result: {validation_result}")
        
#         # Generate SQL query from Gemini
#         sql_query = get_gemini_response(question.text)
#         logging.info(f"Generated SQL query: {sql_query}")
      

#         # Execute the SQL query and get results
#         query_results = read_sql_query(sql_query, "results.db")
#         logging.info(f"Query results: {query_results}")

#         # Convert query results into descriptive sentences using Gemini
#         description_prompt = (
#             "Based on the following query results, generate a descriptive sentence that conveys the result clearly. "
#             "Ensure the sentence includes relevant information like dates, shifts, or other context.\n\n"
#             f"Query Results: {query_results}\n"
#             f"Query: {sql_query}\n\n"
#             "Output a single, concise sentence in proper English."
#         )
#         descriptive_sentence = get_gemini_response(description_prompt).strip()
#         logging.info(f"Generated description: {descriptive_sentence}")

#         # Extract only the recommendations
#         recommendations = validation_result.get("recommendations", [])
#         recommendation_results = [{"recommendation_message": rec} for rec in recommendations]

#         # Return recommendations, query, results, and descriptive sentence
#         return {
#             "recommendations": recommendation_results,
#             "query": sql_query,
#             "results": query_results,
#             "description": descriptive_sentence
#         }

#     except Exception as e:
#         logging.error(f"Error occurred during validation: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))


@app.post("/rec1")
async def rec1(question: Question):
    """
    Validate the query, generate recommendations, and dynamically return results 
    as either descriptive text or a table based on Gemini's output.
    """
    try:
        logging.info(f"Validating query: {question.text}")

        # Validate the user query
        validation_result = validate_query_with_gemini(question.text)
        logging.info(f"Validation result: {validation_result}")

        # Generate SQL query from Gemini
        sql_query = get_gemini_response(question.text)
        logging.info(f"Generated SQL query: {sql_query}")

        # Execute the SQL query and get results
        query_results = read_sql_query(sql_query, "results.db")
        logging.info(f"Query results: {query_results}")

        # Create a prompt for Gemini to dynamically decide output format
        output_decision_prompt = (
    "You are an assistant generating structured outputs. Based on the query results below, "
    "create a JSON object for a table with 'headers' and 'rows', or generate a descriptive text. "
    "Respond in one of these formats:\n\n"
    "{\n"
    '  "format": "table",\n'
    '  "content": {\n'
    '    "headers": ["Column1", "Column2"],\n'
    '    "rows": [["Value1", "Value2"], ["Value3", "Value4"]]\n'
    "  }\n"
    "}\n\n"
    "{\n"
    '  "format": "text",\n'
    '  "content": "Description of the query results."\n'
    "}\n\n"
    f"Query Results: {query_results}\n"
)


        gemini_output = get_gemini_response(output_decision_prompt)
        logging.info(f"Gemini output: {gemini_output}")

        # Parse Gemini's response
        gemini_decision = json.loads(gemini_output)
        output_format = gemini_decision.get("format")
        output_content = gemini_decision.get("content")

        if output_format == "table":
            # Ensure table format has headers and rows
            table_data = output_content if isinstance(output_content, dict) else {}
            response_data = {
                "format": "table",
                "headers": table_data.get("headers", []),
                "rows": table_data.get("rows", [])
            }
        elif output_format == "text":
            response_data = {
                "format": "text",
                "description": output_content
            }
        else:
            raise ValueError("Invalid format returned by Gemini.")

        # Extract only the recommendations
        recommendations = validation_result.get("recommendations", [])
        recommendation_results = [{"recommendation_message": rec} for rec in recommendations]

        # Combine recommendations and response data
        return {
            "recommendations": recommendation_results,
            "query": sql_query,
            "results": query_results,
            "gemini_output": response_data
        }

    except Exception as e:
        logging.error(f"Error occurred during validation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Welcome to the SQL Query API"}

if __name__ == "__main__":
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



############################################### DO U MEAN ##################################### 

# @app.post("/query")
# async def query(question: Question):
#     try:
#         # Find the best synonym match and its unit
#         synonym, matched_unit = check_for_synonyms_with_units(question.text)
        
#         # Generate SQL query using Gemini
#         sql_query = get_gemini_response(question.text)
        
#         # Create "Do you mean" suggestion
#         do_you_mean = f"Do you mean '{synonym}'?" if synonym else None
        
#         # Execute query
#         conn = sqlite3.connect("results.db")
#         cursor = conn.cursor()
#         cursor.execute(sql_query)
        
#         # Get column names and fetch results
#         columns = [description[0] for description in cursor.description]
#         results = cursor.fetchall()
#         conn.close()
        
#         # Map columns to units based on the query
#         column_units = map_columns_to_units(sql_query)
        
#         # Format results with units
#         formatted_results = []
#         for row in results:
#             formatted_row = []
#             for i, value in enumerate(row):
#                 # Try to find a unit for the current column
#                 column_name = columns[i].lower()
#                 unit = next((
#                     unit for col, unit in column_units.items() 
#                     if col.lower() in column_name
#                 ), None)
                
#                 # Format value with unit if found
#                 formatted_value = f"{value} {unit}" if unit else str(value)
#                 formatted_row.append(formatted_value)
            
#             formatted_results.append(formatted_row)
        
#         return {
#             "query": sql_query,
#             "do_you_mean": do_you_mean,
#             "synonym": synonym,
#             "matched_unit": matched_unit,
#             "results": formatted_results,
#             "columns": columns
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the SQL Query API"}

# if __name__ == "__main__":
    
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# @app.post("/query")
# async def query(question: Question):
#     """
#     Process the input query, validate it using Gemini, and return recommendations along with the SQL query and result.
#     """
#     try:
#         logging.info(f"Received query: {question.text}")

#         # Generate SQL query using Gemini
#         sql_query = get_gemini_response(question.text)
#         logging.info(f"Generated SQL query: {sql_query}")

#         # Validate the user query and generate recommendations
#         validation_result = validate_query_with_gemini(question.text)
#         logging.info(f"Validation result: {validation_result}")

#         # Extract only the recommendations
#         recommendations = validation_result.get("recommendations", [])

#         # Prepare the response with recommendations only
#         recommendation_results = [{"recommendation_message": rec} for rec in recommendations]
        
#         # Execute the SQL query and get results
#         query_results = read_sql_query(sql_query, "results.db")
#         logging.info(f"Query results: {query_results}")

#         # Return both the recommendation and query results
#         return {
#             "recommendations": recommendation_results,
#             "query": sql_query,
#             "results": query_results,  # Add query result to the response
#         }

#     except Exception as e:
#         logging.error(f"Error occurred: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))


# @app.get("/")
# async def root():
#     return {"message": "Welcome to the SQL Query API"}

# if __name__ == "__main__":
    
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
   

# @app.post("/query")
# async def query(question: Question):
#     """
#     Process the input query, validate it using Gemini, and return recommendations along with the SQL query and result.
#     """
#     try:
#         logging.info(f"Received query: {question.text}")

#         # Generate SQL query using Gemini
#         sql_query = get_gemini_response(question.text)
#         logging.info(f"Generated SQL query: {sql_query}")

#         # Validate the user query and generate recommendations
#         validation_result = validate_query_with_gemini(question.text)
#         logging.info(f"Validation result: {validation_result}")

#         # Extract only the recommendations
#         recommendations = validation_result.get("recommendations", [])

#         # Prepare the response with recommendations only
#         recommendation_results = [{"recommendation_message": rec} for rec in recommendations]
        
#         # Execute the SQL query and get results
#         query_results = read_sql_query(sql_query, "results.db")
#         logging.info(f"Query results: {query_results}")

#         # Return both the recommendation and query results
#         return {
#             "recommendations": recommendation_results,
#             "query": sql_query,
#             "results": query_results,  # Add query result to the response
#         }

#     except Exception as e:
#         logging.error(f"Error occurred: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))
    
# @app.get("/")
# async def root():
#     return {"message": "Welcome to the SQL Query API"}

# if __name__ == "__main__":
    
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

#  ----------------------------------------------------------------------------------------
# @app.post("/query")
# async def query(question: Question):
#     """
#     Process the input query, validate it using Gemini, and return recommendations along with the SQL query and result.
#     """
#     try:
#         logging.info(f"Received query: {question.text}")

#         # Generate SQL query using Gemini
#         sql_query = get_gemini_response(question.text)
#         logging.info(f"Generated SQL query: {sql_query}")

#         # Validate the user query and generate recommendations
#         validation_result = validate_query_with_gemini(question.text)
#         logging.info(f"Validation result: {validation_result}")

#         # Extract only the recommendations
#         recommendations = validation_result.get("recommendations", [])

#         # Prepare the response with recommendations only
#         recommendation_results = [{"recommendation_message": rec} for rec in recommendations]
        
#         # Execute the SQL query and get results
#         query_results = read_sql_query(sql_query, "results.db")
#         logging.info(f"Query results: {query_results}")

#         # Return both the recommendation and query results
#         return {
#             "recommendations": recommendation_results,
#             "query": sql_query,
#             "results": query_results,  # Add query result to the response
#         }

#     except Exception as e:
#         logging.error(f"Error occurred: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))




#------------------------ Production code -------------------

# @app.post("/query")
# async def query(question: Question):
#     try:
#         # Find the best synonym match and its unit
#         synonym, matched_unit = check_for_synonyms_with_units(question.text)
        
#         # Generate SQL query using Gemini
#         sql_query = get_gemini_response(question.text)
        
#         # Create "Do you mean" suggestion
#         do_you_mean = f"Do you mean '{synonym}'?" if synonym else None
        
#         # Execute query
#         conn = sqlite3.connect("results.db")
#         cursor = conn.cursor()
#         cursor.execute(sql_query)
        
#         # Get column names and fetch results
#         columns = [description[0] for description in cursor.description]
#         results = cursor.fetchall()
#         conn.close()
        
#         # Map columns to units based on the query
#         column_units = map_columns_to_units(sql_query)
        
#         # Format results with units
#         formatted_results = []
#         for row in results:
#             formatted_row = []
#             for i, value in enumerate(row):
#                 # Try to find a unit for the current column
#                 column_name = columns[i].lower()
#                 unit = next((
#                     unit for col, unit in column_units.items() 
#                     if col.lower() in column_name
#                 ), None)
                
#                 # Format value with unit if found
#                 formatted_value = f"{value} {unit}" if unit else str(value)
#                 formatted_row.append(formatted_value)
            
#             formatted_results.append(formatted_row)
        
#         return {
#             "query": sql_query,
#             "do_you_mean": do_you_mean,
#             "synonym": synonym,
#             "matched_unit": matched_unit,
#             "results": formatted_results,
#             "columns": columns
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))





# -------------------------------------------------------
# @app.post("/query")
# async def query(question: Question):
#     try:
#         validation_result = validate_query_with_gemini(question.text)
    
#         sql_query = get_gemini_response(question.text)

#         conn = sqlite3.connect("results.db")
#         cursor = conn.cursor()
#         cursor.execute(sql_query)
        
#         #  results
#         columns = [description[0] for description in cursor.description]
#         results = cursor.fetchall()
#         conn.close()
        
#         # Map results
#         column_units = map_columns_to_units(sql_query)
#         formatted_results = []
#         for row in results:
#             formatted_row = []
#             for i, value in enumerate(row):
#                 column_name = columns[i].lower()
#                 unit = next(
#                     (unit for col, unit in column_units.items() if col.lower() in column_name),
#                     None
#                 )
#                 formatted_value = f"{value} {unit}" if unit else str(value)
#                 formatted_row.append(formatted_value)
#             formatted_results.append(formatted_row)
        
#         # Return recommendations, executed SQL query, and results
#         return {
#             "recommendations": validation_result["recommendations"],
#             "executed_query": sql_query,
#             "results": formatted_results,
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# -----------------------------------------------------------------------------------------------------------------------


# column_synonyms_with_units = {
#     "count": {"synonyms": ["number", "count", "quantity"], "unit": None},
#     "date": {"synonyms": ["day", "date", "which day","total number of"], "unit": None},
#     "slab": {"synonyms": ["input material", "raw material", "slab"], "unit": None},
#     "slab weight": {"synonyms": ["slab weight", "input weight", "raw material weight"], "unit": "tons"},
#     "coil": {"synonyms": ["coil","produced","produce" ,"product", "production", "output material", "Batch", "Hot Coil", "Rolled Coil"], "unit": None},
#     "steel grade": {"synonyms": ["steel grade", "coil grade", "material grade", "tdc grade", "output material grade"], "unit": None},
#     "coil thickness": {"synonyms": ["coil thickness", "output material thickness", "product thickness", "production thickness", "Batch thickness", "Hot Thickness"], "unit": "mm"},
#     "coil width": {"synonyms": ["coil width", "output material width", "product width", "production width", "Batch width", "Hot Width"], "unit": "mm"},
#     "coil weight": {"synonyms": ["coil weight", "output material weight", "product weight", "production weight", "Plant Production", "Hot Metal Produced", "HSM Output", "Rolling Weight", "Hot Rolling Weight"], "unit": "tons"},
#     "target coil thickness": {"synonyms": ["target coil thickness", "order thickness", "target thickness", "tdc thickness", "Modified Thickness"], "unit": "mm"},
#     "target coil width": {"synonyms": ["target coil width", "order width", "target width", "tdc width", "Modified Width"], "unit": "mm"},
#     "line running time": {"synonyms": ["line running time", "Plant Running running time"], "unit": "min"},
#     "production duration": {"synonyms": ["Production duration", "Coil Running Time", "Time for Production", "Time taken to Produce the coil"], "unit": "min"},
#     "idle time": {"synonyms": ["idle time", "available time", "total available time"], "unit": "min"},
#     "running time percentage": {"synonyms": ["running time percentage", "running time %", "running time percentage","line running percentage","line running %"], "unit": "%"},
#     "idle time percentage": {"synonyms": ["idle time percentage", "idle time %", "idle time percentage"], "unit": "%"},
#     "production Start Time": {"synonyms": ["Production Start Time", "Coil Start Time", "Rolling Start Time"], "unit": None},
#     "coil Production Time": {"synonyms": ["Coil Production Time", "Coil End Time", "Rolling End Time", "Time of Production", "Production Time", "Rolling Finish Time", "DC Out Time"], "unit": "min"},
#     "yield":{"synonyms": ["total yield", "yeild","yield"], "unit": "%"},
#     "shift a": {"synonyms": ["shift A", "06:00:00 to 13:59:59"], "unit": None},
#     "shift b": {"synonyms": ["shift B", "14:00:00 to 21:59:59"], "unit": None},
#     "shift c": {"synonyms": ["shift C", "22:00:00 to 05:59:59"], "unit": None},
# }

# def check_for_synonyms_with_units(question):
#     best_match = None
#     best_match_length = 0
#     unit = None
#     question_lower = question.lower()

#     # Explicitly prioritize "count" and "date"
#     for column in ["count", "date"]:
#         details = column_synonyms_with_units[column]
#         for synonym in details["synonyms"]:
#             synonym_lower = synonym.lower()
#             if synonym_lower in question_lower:
#                 return column, details["unit"]  # Return immediately if "count" or "date" matches

#     # If no match for "count" or "date", check other synonyms
#     for column, details in column_synonyms_with_units.items():
#         for synonym in details["synonyms"]:
#             synonym_lower = synonym.lower()
#             if synonym_lower in question_lower and len(synonym_lower) > best_match_length:
#                 best_match = column
#                 best_match_length = len(synonym_lower)
#                 unit = details["unit"]

#     return best_match, unit

# def map_columns_to_units(query):
#     """
#     Maps column names in the SQL query to their respective units based on predefined synonyms.
#     """
#     column_units = {}
#     for column, details in column_synonyms_with_units.items():
#         for synonym in details["synonyms"]:
#             if synonym.lower() in query.lower():
#                 column_units[column] = details["unit"]
#     return column_units

# @app.post("/query")
# async def query(question: Question):
#     try:
#         # Find the best synonym match and its unit
#         synonym, matched_unit = check_for_synonyms_with_units(question.text)
        
#         # Generate SQL query using Gemini
#         sql_query = get_gemini_response(question.text)
        
#         # Create "Do you mean" suggestion
#         do_you_mean = f"Do you mean '{synonym}'?" if synonym else None
        
#         # Execute query
#         conn = sqlite3.connect("results.db")
#         cursor = conn.cursor()
#         cursor.execute(sql_query)
        
#         # Get column names and fetch results
#         columns = [description[0] for description in cursor.description]
#         results = cursor.fetchall()
#         conn.close()
        
#         # Map columns to units based on the query
#         column_units = map_columns_to_units(sql_query)
        
#         # Format results with units
#         formatted_results = []
#         for row in results:
#             formatted_row = []
#             for i, value in enumerate(row):
#                 # Try to find a unit for the current column
#                 column_name = columns[i].lower()
#                 unit = next((
#                     unit for col, unit in column_units.items() 
#                     if col.lower() in column_name
#                 ), None)
                
#                 # Format value with unit if found
#                 formatted_value = f"{value} {unit}" if unit else str(value)
#                 formatted_row.append(formatted_value)
            
#             formatted_results.append(formatted_row)
        
#         return {
#             "query": sql_query,
#             "do_you_mean": do_you_mean,
#             "synonym": synonym,
#             "matched_unit": matched_unit,
#             "results": formatted_results,
#             "columns": columns
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))




# def check_for_synonyms_with_units(question):
#     best_match = None
#     best_match_length = 0
#     unit = None
#     question_lower = question.lower()
#     for column, details in column_synonyms_with_units.items():
#         for synonym in details["synonyms"]:
#             synonym_lower = synonym.lower()
#             if synonym_lower in question_lower and len(synonym_lower) > best_match_length:
#                 best_match = column
#                 best_match_length = len(synonym_lower)
#                 unit = details["unit"]

#     return best_match, unit



# def generate_gemini_prompt_for_synonyms(question):
#     """
#     Builds a prompt to find the closest synonym and unit match using Gemini AI.
#     """
#     column_details = "\n".join(
#         f"{column}: Synonyms = {', '.join(details['synonyms'])}, Unit = {details['unit'] or 'None'}"
#         for column, details in column_synonyms_with_units.items()
#     )
    
#     prompt = (
#     "You are an intelligent assistant helping to map user questions to database columns. "
#     "Here is a list of columns, their synonyms, and units:\n\n"
#     f"{column_details}\n\n"
#     "The user has asked: '{question}'. Match the user's query to the most appropriate column "
#     "based on the synonyms provided. Return the matched column name and its associated unit. "
#     "If the query is ambiguous, suggest clarification using the format: 'Do you mean <column>?'."
#     "\n\nExample:\n"
#     "Columns and synonyms: \n"
#     "  coil thickness: Synonyms = coil thickness, product thickness, Batch thickness, Unit = mm\n"
#     "  slab weight: Synonyms = slab weight, input weight, raw material weight, Unit = tons\n"
#     "User Query: 'What is the product thickness?'\n"
#     "Output: 'coil thickness, Unit = mm'\n"
#     "If ambiguous:\n"
#     "User Query: 'What is the weight?'\n"
#     "Output: 'Do you mean slab weight?'"
    
#     )
#     return prompt


# def check_for_synonyms_with_units_gemini(question):

#     """
#     Uses Gemini AI to find the best synonym match and determine if a reconfirmation is needed.
#     """
#     prompt = generate_gemini_prompt_for_synonyms(question)
    
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content([prompt])
#     response_text = response.text.strip()
    
#     # Parse Gemini's response for matched column and unit or reconfirmation message
#     if "Do you mean" in response_text:
#         matched_column, unit = None, None
#         reconfirmation_message = response_text
#     else:
#         parts = response_text.split(", Unit =")
#         matched_column = parts[0].strip() if len(parts) > 0 else None
#         unit = parts[1].strip() if len(parts) > 1 else None
#         reconfirmation_message = None
    
#     return matched_column, unit, reconfirmation_message





# @app.post("/query")
# async def query(question: Question):
#     try:
#         # Find the best synonym match and its unit
#         synonym, matched_unit = check_for_synonyms_with_units(question.text)
        
#         # Generate SQL query using Gemini
#         sql_query = get_gemini_response(question.text)
        
#         # Create "Do you mean" suggestion
#         do_you_mean = f"Do you mean '{synonym}'?" if synonym else None
        
#         # Execute query
#         conn = sqlite3.connect("results.db")
#         cursor = conn.cursor()
#         cursor.execute(sql_query)
        
#         # Get column names and fetch results
#         columns = [description[0] for description in cursor.description]
#         results = cursor.fetchall()
#         conn.close()
        
#         # Map columns to units based on the query
#         column_units = map_columns_to_units(sql_query)
        
#         # Format results with units
#         formatted_results = []
#         for row in results:
#             formatted_row = []
#             for i, value in enumerate(row):
#                 # Try to find a unit for the current column
#                 column_name = columns[i].lower()
#                 unit = next((
#                     unit for col, unit in column_units.items() 
#                     if col.lower() in column_name
#                 ), None)
                
#                 # Format value with unit if found
#                 formatted_value = f"{value} {unit}" if unit else str(value)
#                 formatted_row.append(formatted_value)
            
#             formatted_results.append(formatted_row)
        
#         return {
#             "query": sql_query,
#             "do_you_mean": do_you_mean,
#             "synonym": synonym,
#             "matched_unit": matched_unit,
#             "results": formatted_results,
#             "columns": columns
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# new for gemini
# @app.post("/query")
# async def query(question: Question):
#     try:
#         # Use Gemini AI for synonym matching
#         synonym, matched_unit, reconfirmation_message = check_for_synonyms_with_units_gemini(question.text)
        
#         # If reconfirmation is needed, return early
#         if reconfirmation_message:
#             return {
#                 "reconfirmation_message": reconfirmation_message,
#                 "query": None,
#                 "results": None,
#                 "columns": None
#             }
        
#         # Generate SQL query using Gemini
#         sql_query = get_gemini_response(question.text)
        
#         # Execute the SQL query
#         conn = sqlite3.connect("results.db")
#         cursor = conn.cursor()
#         cursor.execute(sql_query)
        
#         # Fetch results and column names
#         columns = [description[0] for description in cursor.description]
#         results = cursor.fetchall()
#         conn.close()
        
#         # Map columns to units and format results
#         column_units = map_columns_to_units(sql_query)
#         formatted_results = format_results_with_units(results, columns, column_units)
        
#         return {
#             "query": sql_query,
#             "synonym": synonym,
#             "matched_unit": matched_unit,
#             "results": formatted_results,
#             "columns": columns
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))




# def generate_reconfirmation_message(question):
#     """
#     Uses Gemini to generate a reconfirmation message for the given question based on column synonyms.
#     """
#     # Define the column details in a readable format for the Gemini model
#     column_details = "\n".join(
#         f"{column}: Synonyms = {details['synonyms']}, Unit = {details['unit'] or 'None'}"
#         for column, details in column_synonyms_with_units.items()
#     )

#     # Build the prompt dynamically
#     prompt_template = (
#         "You are an intelligent assistant. Below is a list of column names, their synonyms, and units:\n"
#         "{column_details}\n\n"
#         "The user has asked: '{question}'. Find the closest matching column based on synonyms and frame a polite "
#         "and concise reconfirmation message. If no synonym matches, respond with: "
#         "'I couldn't identify a specific term. Could you clarify further?'."
#       "example -  question is - what was the average input material weight reconfirmation message - do you mean coil weight ?"
#     )
#     reconfirmation_prompt = prompt_template.format(column_details=column_details, question=question)
    
#     # Call the Gemini model with the new prompt
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content([reconfirmation_prompt])
#     return response.text


# @app.post("/query")
# async def query(question: Question, clarification: Optional[str] = None):
#     """
#     Handles user queries by generating SQL queries, and optionally reconfirms the question if needed.
#     """
#     try:
#         # Determine whether this is a clarified query or an initial query
#         final_question = clarification if clarification else question.text

#         # Generate the SQL query using Gemini
#         sql_query = get_gemini_response(final_question)
        
#         # If clarification is not provided, generate a reconfirmation message
#         if not clarification:
#             reconfirmation_message = generate_reconfirmation_message(question.text)
#             return {
#                 "initial_response": {
#                     "query": sql_query,
#                     "reconfirmation_message": reconfirmation_message,
#                 },
#                 "message": "Please confirm or refine your query."
#             }

#         # Execute the SQL query
#         conn = sqlite3.connect("results.db")
#         cursor = conn.cursor()
#         cursor.execute(sql_query)

#         # Fetch column names and results
#         columns = [description[0] for description in cursor.description]
#         results = cursor.fetchall()
#         conn.close()

#         return {
#             "query": sql_query,
#             "results": results,
#             "columns": columns
#         }
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



 







# -----------------------------------------------------------------------------------


# from dotenv import load_dotenv
# load_dotenv()

# import streamlit as st
# import os
# import sqlite3
# import google.generativeai as genai

# # API key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# st.set_page_config(page_title="SQL Query Generator", page_icon="📊")

# # Header and description
# st.header("🔍 Smart Agent for Natural Language to SQL query")


# # Initialize session state for storing inputs and results
# if "user_inputs" not in st.session_state:
#     st.session_state.user_inputs = {}

# if "show_confirmation" not in st.session_state:
#     st.session_state.show_confirmation = False

# if "show_error_message" not in st.session_state:
#     st.session_state.show_error_message = False

# # Synonyms for column names
# column_synonyms = {
#     "slab": ["input material", "raw material"],
#     "slab weight": ["input weight", "raw material weight"],
#     "coil": ["product", "production", "output material"],
#     "steel grade": ["steel grade", "coil grade", "material grade", "tdc grade"],
#     "coil thickness": ["output material thickness", "product thickness", "production thickness"],
#     "coil width": ["output material width", "product width", "production width"],
#     "Coil weight": ["output material weight", "product weight", "production weight"],
#     "target coil thickness": ["order thickness", "target thickness", "tdc thickness"],
#     "Target coil width": ["order width", "target width", "tdc width"],
#     "production time": ["line running time", "running time"],
#     "idle time": ["available time", "total available time"],
#     "running time percentage": ["running time %", "running time percentage"],
#     "idle time percentage": ["idle time %", "idle time percentage"],
#     "shift a": ["shift A", "06:00:00 to 13:59:59"],
#     "shift b": ["shift B", "14:00:00 to 21:59:59"],
#     "shift c": ["shift C", "22:00:00 to 05:59:59"]
# }

# # Function to check for the best matching synonym in the user question

# def check_for_synonyms(question):
#     best_match = None
#     best_match_length = 0
    
#     # Lowercase the question to make matching case-insensitive
#     question_lower = question.lower()
    
#     # Iterate through the column synonyms
#     for column, synonyms in column_synonyms.items():
#         for synonym in synonyms:
#             synonym_lower = synonym.lower()
#            
#             if synonym_lower in question_lower and len(synonym_lower) > best_match_length:
#                 best_match = column
#                 best_match_length = len(synonym_lower)
                
#     return best_match


# prompt = [
#     '''
#      You are an expert in converting English questions to SQL queries! The SQL database contains a table named RESULT with the following columns:

# - DATEE: Date & time of creation of the slab or coil.
# - DATESE: Staring Date & Time of Creation of slab or coil . 
# - SCHNO: Schedule number.
# - SEQ: Rolling sequence number of the slab.
# - SLAB: Slab ID, also referred to as 'Input Material' or 'Raw Material'.
# - S_WEIGHT: Slab weight, also called 'Input Weight' or 'Raw Material Weight'.
# - COIL: Coil ID, also referred to as 'Output Material', 'Product', or 'Production'.
# - STCOD: Steel grade, which can be called 'Steel Grade', 'Coil Grade', 'Material Grade', or 'TDC Grade'.
# - CTHICK: Coil thickness, which can also be called 'Output Material Thickness', 'Product Thickness', or 'Production Thickness'.
# - CWIDTH: Coil width, referred to as 'Output Material Width', 'Product Width', or 'Production Width'.
# - AWEIT: Coil weight, also called 'Output Material Weight', 'Product Weight', or 'Production Weight'.
# - OTHICK: Target coil thickness, referred to as 'Order Thickness', 'Target Thickness', or 'TDC Thickness'.
# - OWIDTH: Target coil width, referred to as 'Order Width', 'Target Width', or 'TDC Width'.
# - SHIFT: Shift A: 06:00:00 to 13:59:59 Shift B: 14:00:00 to 21:59:59 Shift C: 22:00:00 to 05:59:59 (next day)
# - STIME: Stoppage time refers to the time resulting into stoppage of the manifacturing.
# - Production time refers to the time taken for production of a coil i.e.  time of creation of the slab or coil - Staring Date & Time of Creation of slab or coil - or  DATEE - DATESE
# - Production time =  ( DATEE - DATESE) it should always be in minutes

# Additional concepts:
# 1. Line Running Time / Running Time = sum of Production time for all coils in a given period (day or shift)
# 2. Idle Time = Total available time - Line Running Time
# 3. Running Time Percentage (%) = (Line Running Time / Total available time) * 100
# 4. Idle Time Percentage (%) = (Idle Time / Total available time) * 100
# 5. Total Production time (the sum) is the same as line running time 


# IMPORTANT:
# Do not include any markdown formatting, code block indicators (like ```), or the word 'sql' in your response.
# Provide only the SQL query text, without any additional explanations or comments.
# Ensure the query is syntactically correct and ready for direct execution in an SQL environment.


#    The day cycle starts from 6 AM to 6 AM the following day. Each day will consist of three shifts:
# - **Shift A**: Runs from 06:00 AM to 01:59 PM (13:59:59).
# - **Shift B**: Runs from 02:00 PM to 09:59 PM (21:59:59).
# - **Shift C**: Runs from 10:00 PM to 05:59 AM the next day.

# For example:
# - For **24 September**, the day starts from **06:00 AM** and ends at **05:59 AM** on **25 September**.
# - For **25 September**, the day starts from **06:01 AM** and ends at **05:59 AM** on **26 September**.
# When a coil is produced between 12:00 AM and 6:00 AM, but falls under the C shift of the previous day, it should be recorded as produced on the prior day. 
# For example, if a coil is produced at 02:00 AM on 30/09/2024, it should be considered as produced on 29/09/2024, 
# as it falls within the C shift of 29/09/2024. The day cycle runs from 6:00 AM to 6:00 AM, so any coil produced before 6:00 AM 
# on the following day still belongs to the previous day's shift.
# When handling dates, you should convert normal date formats (like "24 September 2024") into the SQL format "YYYY-MM-DD HH:MM".


# 1. Calculate the average production time per day:
# SQL:
# SELECT 
#     DATE(DATESE) AS ProductionDate,
#     ROUND(AVG((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS AvgProductionTimeInMinutes
# FROM RESULT
# GROUP BY DATE(DATESE);

# SELECT 
#     CASE 
#         WHEN TIME(DATESE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
#         WHEN TIME(DATESE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
#         ELSE 'C'
#     END AS Shift,
#     ROUND(AVG((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS AvgProductionTimeInMinutes
# FROM RESULT
# WHERE TIME(DATEE) >= TIME(DATESE)
# GROUP BY Shift;


# 3. Calculate the total production time per shift:
# SQL:
# SELECT 
#     CASE 
#         WHEN TIME(DATESE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
#         WHEN TIME(DATESE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
#         ELSE 'C'
#     END AS Shift,
#     ROUND(SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS TotalProductionTimeInMinutes
# FROM RESULT
# WHERE TIME(DATEE) >= TIME(DATESE)
# GROUP BY Shift;

# 4. Find the maximum and minimum production times:
# SQL:
# SELECT 
#     COIL,
#     ROUND(MAX((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS MaxProductionTimeInMinutes,
#     ROUND(MIN((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS MinProductionTimeInMinutes
# FROM RESULT
# GROUP BY COIL;


# ------------------------------------------------
# 5. Average Production Time per Day
# SELECT 
#     DATE(DATESE, '-6 hours') AS ProductionDate,
#     ROUND(AVG((JULIANDAY(MIN(DATEE, DATETIME(DATE(DATESE, '+1 day'), '06:00:00'))) - JULIANDAY(MAX(DATESE, DATETIME(DATE(DATESE), '06:00:00')))) * 24 * 60), 2) AS AvgProductionTimeInMinutes
# FROM 
#     RESULT
# WHERE 
#     (DATETIME(DATESE) >= DATETIME(DATE(DATESE), '06:00:00') AND DATETIME(DATEE) <= DATETIME(DATE(DATESE, '+1 day'), '06:00:00'))
#     OR (DATETIME(DATESE) < DATETIME(DATE(DATESE), '+1 day', '06:00:00') AND DATETIME(DATEE) > DATETIME(DATE(DATESE), '06:00:00'))
# GROUP BY 
#     DATE(DATESE, '-6 hours');


# 6. Average production time for "date"

# SELECT 
#     '2024-09-29' AS ProductionDate,  -- Replace '2024-09-29' with your specific date
#     ROUND(
#         AVG(
#             (JULIANDAY(MIN(DATEE, '2024-09-30 06:00:00')) - JULIANDAY(MAX(DATESE, '2024-09-29 06:00:00'))) * 1440
#         ), 2
#     ) AS AvgProductionTimeInMinutes
# FROM 
#     RESULT
# WHERE 
#     (DATETIME(DATESE) >= '2024-09-29 06:00:00' AND DATETIME(DATEE) <= '2024-09-30 06:00:00')
#     OR (DATETIME(DATESE) < '2024-09-30 06:00:00' AND DATETIME(DATEE) > '2024-09-29 06:00:00');

# 7. Average production time between dates.

# SQL Query:
# SELECT 
#     ROUND(SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS TotalProductionTimeInMinutes,
#     COUNT(*) AS NumberOfCoilsProduced,
#     ROUND(SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440) / COUNT(*), 2) AS AverageProductionTimeInMinutes
# FROM RESULT
# WHERE DATESE >= '2024-09-27 06:00:00' 
#   AND DATESE < '2024-09-30 06:00:00';

# 8. what is the total production time for E350Br 
#  SELECT 
#     ROUND(SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS TotalProductionTimeInMinutes
# FROM RESULT
# WHERE STCOD = 'E350Br';


# NOTE : if asked about Line Running Time for a particular date or Line Running Time Percentage for a particular date then always take date from 6 am to next day 6 am 

# example - 

# SELECT   
#     '2024-09-26' AS ProductionDate,              -- Replace '2024-09-26' with your specific date
#     ROUND(
#         SUM(
#             (JULIANDAY(MIN(DATEE, '2024-09-27 06:00:00')) - JULIANDAY(MAX(DATESE, '2024-09-26 06:00:00'))) * 1440
#         ), 2
#     ) AS LineRunningTimeMinutes
# FROM 
#     RESULT
# WHERE 
#     (DATETIME(DATESE) >= '2024-09-26 06:00:00' AND DATETIME(DATEE) <= '2024-09-27 06:00:00')
#     OR (DATETIME(DATESE) < '2024-09-27 06:00:00' AND DATETIME(DATEE) > '2024-09-26 06:00:00');



# 2. Running Time Percentage/Line Running time Percentage for a day 

# SELECT 
#     '2024-09-29' AS ProductionDate,                                -- Replace '2024-09-29' with the specific date
#     ROUND(
#         (SUM(
#             (JULIANDAY(MIN(DATEE, '2024-09-30 06:00:00')) - JULIANDAY(MAX(DATESE, '2024-09-29 06:00:00'))) * 1440
#         ) / 1440) * 100, 2
#     ) AS RunningTimePercentage
# FROM 
#     RESULT
# WHERE 
#     (DATETIME(DATESE) >= '2024-09-29 06:00:00' AND DATETIME(DATEE) <= '2024-09-30 06:00:00')
#     OR (DATETIME(DATESE) < '2024-09-30 06:00:00' AND DATETIME(DATEE) > '2024-09-29 06:00:00');


# 3. Idle Time (Daily)
# SELECT 
#     DATE(DATESE, '-6 hours') AS ProductionDate,
#     ROUND(1440 - SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS IdleTimeMinutes
# FROM RESULT
# WHERE TIME(DATESE) >= '06:00:00'
#   OR TIME(DATEE) < '06:00:00'
# GROUP BY DATE(DATESE, '-6 hours');


    
# 4. Idle Time Percentage (Daily)
# SELECT 
#     DATE(DATESE, '-6 hours') AS ProductionDate,
#     ROUND(((1440 - SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440)) / 1440) * 100, 2) AS IdleTimePercentage
# FROM RESULT
# WHERE TIME(DATESE) >= '06:00:00'
#   OR TIME(DATEE) < '06:00:00'
# GROUP BY DATE(DATESE, '-6 hours');


# -- Shift-wise Metrics

# 1. Line Running Time (Shift-wise)
# SELECT 
#     CASE 
#         WHEN TIME(DATESE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
#         WHEN TIME(DATESE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
#         ELSE 'C'
#     END AS Shift,
#     ROUND(SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS LineRunningTimeMinutes
# FROM RESULT
# GROUP BY Shift;

# 2. Idle Time (Shift-wise)
# SELECT 
#     CASE 
#         WHEN TIME(DATESE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
#         WHEN TIME(DATESE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
#         ELSE 'C'
#     END AS Shift,
#     ROUND(480 - SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440), 2) AS IdleTimeMinutes
# FROM RESULT
# GROUP BY Shift;

# 3.Line Running Time Percentage for Shifts A and B for 28 sept 

# SELECT 
#     CASE 
#         WHEN TIME(DATESE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
#         WHEN TIME(DATESE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
#     END AS Shift,
#     ROUND((SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440) / 480) * 100, 2) AS LineRunningTimePercentage
# FROM RESULT
# WHERE DATE(DATESE) = '2024-09-28' 
# GROUP BY Shift;


# 4.Line Running Time Percentage for Shift C for 28 sept 
# SELECT 
#     'C' AS Shift,
#     ROUND((SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440) / 480) * 100, 2) AS LineRunningTimePercentage  
# FROM RESULT
# WHERE (DATE(DATESE) = '2024-09-28' AND TIME(DATESE) >= '22:00:00')
#    OR (DATE(DATESE) = '2024-09-29' AND TIME(DATESE) < '06:00:00');

# 5. Idle Time Percentage for Shifts A and B:
# SELECT 
#     CASE 
#         WHEN TIME(DATESE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
#         WHEN TIME(DATESE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
#     END AS Shift,
#     ROUND(((1440 - SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440)) / 960) * 100, 2) AS IdleTimePercentage
# FROM RESULT
# WHERE DATE(DATESE) = '2024-09-28'  -- specify the date
# AND TIME(DATESE) BETWEEN '06:00:00' AND '21:59:59'
# GROUP BY Shift;
   

# 6.Idle Time Percentage for Shift C (10:00 PM to 6:00 AM next day):
# SELECT 
#     'C' AS Shift,
#     ROUND(((480 - SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440)) / 480) * 100, 2) AS IdleTimePercentage  -- 480 minutes = 8 hours (10 PM to 6 AM)
# FROM RESULT
# WHERE (DATE(DATESE) = '2024-09-28' AND TIME(DATESE) >= '22:00:00')
#    OR (DATE(DATESE) = '2024-09-29' AND TIME(DATESE) < '06:00:00');

   
# 7. Running time  percentage  on 25 sept for  A shift 
# SELECT 
#     'A' AS Shift,
#     ROUND((SUM((JULIANDAY(DATEE) - JULIANDAY(DATESE)) * 1440) / 480) * 100, 2) AS RunningTimePercentage
# FROM RESULT
# WHERE DATE(DATESE) = '2024-09-25'
# AND TIME(DATESE) BETWEEN '06:00:00' AND '13:59:59';


# Question : how many coils were produced on 29 sept;
# SQL :
# SELECT COUNT(*) AS CoilCount 
# FROM RESULT 
# WHERE DATEE >= '2024-09-29 06:00:00' 
#   AND DATEE < '2024-09-30 05:59:59';

# Supported Operations:

# Difference Calculation: Calculate the difference between the maximum and minimum values (e.g., coil weight difference).
# Calculate yield as (AWEIT * 100 / S_WEIGHT), presented as a percentage up to 3 decimal places.
# Yield = (AWEIT * 100 / S_WEIGHT), where AWEIT is the output weight and S_WEIGHT is the input weight.
# The yield must always be a decimal up to 3 decimal places.
# Good yield is defined as yield ≥ 97.000%, and bad yield is < 97.000%.
# If asked about the yield of a shift or day, calculate the yield for each coil first, then sum them and 
# divide by the total number of coils to get the average yield.

# Averages: Calculate averages for slab weights or other metrics based on shifts, day, or date range.
# Sum & Count: Sum or count records based on shifts, steel grade, or date range.
# List: Retrieve records filtered by coil, slab, or steel grade.
# Shift-based Queries: Production statistics filtered by shifts A, B, or C.
    
# Convert the following question into an SQL query:

# {user_question}

# Instructions:
# - Use the **RESULT** table for all queries.
# -Generate the query without adding any formatting symbols or SQL code blocks like ```sql.
# -The query should be in plain SQL format.
# - Convert date formats like "24 September 2024" to 'YYYY-MM-DD HH:MM:SS'.
# - For shifts: 
#   -**Shift A** is 06:00:00 to 13:59:59 on the same day.
#   - **Shift B** is 14:00:00 to 21:59:59 on the same day.
#   - **Shift C** is 22:00:00 of the current day to 05:59:59 of the next day.

# - If asked about Tons, then calculate the sum of AWEIT. While giving answer , convert it into Tons ( 1 ton = 1000KG )
#     - Tons per day refers to the sum of AWEIT for the whole day.
#     - Tons per hour refers to AWEIT / number of hours.
# -If the question involves Yield, use the formula: Yield = (AWEIT * 100 / S_WEIGHT).
# -For yield calculations in SQLite, use the printf function to ensure the final result is always displayed with 3 decimal places, including trailing zeros if necessary.
# -Use the following format:
#  printf('%.3f', ROUND((AWEIT * 100.0 / S_WEIGHT), 3)) AS Yield

# -When comparing yields:
#     Good yield: Yield >= 97.000
#     Bad yield: Yield < 97.000


# Example for calculating yield on a specific date:
# SELECT printf('%.3f', AVG((AWEIT * 100.0 / S_WEIGHT))) AS AverageYield
# FROM RESULT
# WHERE DATE(DATEE) = '2024-09-27';

# For shift-based yield queries:
# 1. Use CASE statements to determine the shift based on the time part of DATEE.
# 2. Calculate the yield directly in the WHERE clause.
# 3. For date-specific queries, use DATE(DATEE) to compare only the date part.

# Example for shift-based good yield count:
# SELECT COUNT(*) AS GoodYieldCount
# FROM RESULT
# WHERE (CASE 
#     WHEN strftime('%H:%M:%S', DATEE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
#     WHEN strftime('%H:%M:%S', DATEE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
#     WHEN strftime('%H:%M:%S', DATEE) >= '22:00:00' OR strftime('%H:%M:%S', DATEE) < '06:00:00' THEN 'C'
# END) = 'C'
# AND (AWEIT * 100.0 / S_WEIGHT) >= 97.000;

# Example for shift-based good yield count on a specific date:
# SELECT COUNT(*) AS GoodYieldCount
# FROM RESULT
# WHERE DATE(DATEE) = '2024-09-27'
# AND (CASE 
#     WHEN strftime('%H:%M:%S', DATEE) BETWEEN '06:00:00' AND '13:59:59' THEN 'A'
#     WHEN strftime('%H:%M:%S', DATEE) BETWEEN '14:00:00' AND '21:59:59' THEN 'B'
#     WHEN strftime('%H:%M:%S', DATEE) >= '22:00:00' OR strftime('%H:%M:%S', DATEE) < '06:00:00' THEN 'C'
# END) = 'A'
# AND (AWEIT * 100.0 / S_WEIGHT) >= 97.000;

# Note: When filtering by shift, always use the CASE statement to determine the shift based on DATEE, rather than relying on a SHIFT column.
# For average yield over a shift or day, first calculate the yield for each coil, then sum the individual yields and divide by the total number of coils.
# - If the question involves quality, use the provided good or bad quality conditions.
# - Ensure proper date filtering when relevant (e.g., for day or week queries).
# - Provide counts, averages, or sums as requested.
# - For any averages, round the result to 2 decimal places.     
# - For good quality:
#     - CTHICK is within +/- 0.013 of OTHICK.
#     - CWIDTH is within +13 of OWIDTH.
# -Provide a valid SQL query without any syntax errors.   
# For **grade-wise production**, group the data by the **steel grade (STCOD)** and by **date**.
# Use `DATE(DATEE)` to extract the date from the `DATEE` column.
# Generate the query without adding any formatting symbols or SQL code blocks like ```sql.
# The query should be in plain SQL format.

# - If calculating the yield for 26 September, calculate the yield for each coil produced on that date, and then divide the sum of the yields by the number of coils to get the average yield.

# Let the number of coils = 4, then:
# `(yield of coil1 + yield of coil2 + yield of coil3 + yield of coil4) / 4`


# Question : how many coils were produced on 27 sept
# SQL :
# SELECT COUNT(*) AS CoilCount 
# FROM RESULT 
# WHERE DATEE >= '2024-09-27 06:00:00' 
#   AND DATEE < '2024-09-28 05:59:59';

# Question:  "Grade-wise production for each day":
# SQL : 
# SELECT STCOD, DATE(DATEE) AS ProductionDate, COUNT(*) AS CoilCount
# FROM RESULT
# GROUP BY STCOD, DATE(DATEE);

# Question: "What is the difference between the least weighted coil and the most weighted coil on 28 September 2024"
# SQL :
# SELECT MAX(AWEIT) - MIN(AWEIT) AS WeightDifference 
# FROM RESULT 
# WHERE DATE(DATEE) = '2024-09-28';


# Question: "average coil production per day" 
# SQL : 
# SELECT ROUND(AVG(CoilCount), 2) AS AverageDailyCoilProduction
# FROM (
#   SELECT COUNT(*) AS CoilCount
#   FROM RESULT
#   GROUP BY DATE(DATEE)
# ) AS DailyCoilCounts;

# Question: "How many coils were produced in Shift C on 30 September 2024?"
# SQL:
#     SELECT COUNT(*) AS CoilCount 
#     FROM RESULT 
#     WHERE SHIFT = 'C' 
#     AND (DATEE BETWEEN '2024-09-30 21:00:00' AND '2024-10-01 05:59:59');

    
# Question: "How many good quality coils were produced in Shift C on 25 September 2024?"
# SQL:
#     SELECT COUNT(*) AS GoodQualityCount 
#     FROM RESULT 
#     WHERE (ABS(CTHICK - OTHICK) <= 0.013) 
#     AND (CWIDTH >= OWIDTH - 13 AND CWIDTH <= OWIDTH + 13) 
#     AND SHIFT = 'C' 
#     AND (DATEE BETWEEN '2024-09-25 21:00:00' AND '2024-09-26 05:59:59');

    
# Question: "What is the average slab weight produced in Shift 'A'?"
# SQL:   
#     SELECT AVG(S_WEIGHT) AS AverageSlabWeight 
#     FROM RESULT 
#     WHERE SHIFT = 'A';

# Question: "How many bad quality coils were produced in Shift 'B'?"  
# SQL:    
#     SELECT COUNT(*) AS BadQualityCount 
#     FROM RESULT 
#     WHERE (ABS(CTHICK - OTHICK) > 0.013 OR CWIDTH < OWIDTH - 13 OR CWIDTH > OWIDTH + 13) 
#     AND SHIFT = 'B';

# Question: "What is the yield for steel grade E250Br on 24 September 2024?"
# SQL:   
#     SELECT ROUND(SUM(AWEIT) / SUM(S_WEIGHT), 2) AS Yield 
#     FROM RESULT 
#     WHERE STCOD = 'E250Br' 
#     AND DATEE BETWEEN '2024-09-24 00:00:00' AND '2024-09-24 23:59:59';

# Question: **How many records are present?**
#    SQL command: SELECT COUNT(*) FROM RESULT;

# Question: **Show all coils with steel grade 'E250Br'.**
#    SQL command: SELECT * FROM RESULT WHERE STCOD='E250Br';

# Question: **List all products where the width is greater than 1200.**
#    SQL command: SELECT * FROM RESULT WHERE CWIDTH > 1200;

# Question: ** How many coils were produced in the last 2 days**
#    SQL command :
#    SELECT COUNT(*) FROM RESULT WHERE DATEE BETWEEN datetime('now', '-2 days') AND datetime('now');


   
# Make sure to provide an SQL query without including '
# ' or the word 'sql' in the output.    
    
#     '''
# ]

# import sqlite3

# # Load Gemini model and provide SQL query as response

# def get_gemini_response(question, prompt):
#     model = genai.GenerativeModel('gemini-pro')
#     response = model.generate_content([prompt[0], question])
#     return response.text

# # Retrieve query from the database
# def read_sql_query(sql, db):
#     conn = sqlite3.connect(db)
#     cur = conn.cursor()
#     cur.execute(sql)
#     rows = cur.fetchall()
#     conn.commit()
#     conn.close()
#     return rows

# # Function to handle query execution
# def execute_query(question, output_container):
#     # Generate SQL query
#     sql_query = get_gemini_response(question, prompt)
    
#     # Display the generated SQL query in the specified container
#     with output_container:
#         st.subheader("Generated SQL Query:")
#         st.code(sql_query, language="sql")
        
#         # Execute the SQL query
#         try:
#             data = read_sql_query(sql_query, "results.db")
#             st.subheader("The Response is:")
            
#             if data:
#                 for row in data:
#                     st.write(row)
#             else:
#                 st.write("No data found for the query.")
                
#         except Exception as e:
#             st.error(f"An error occurred: {e}")

# # Function to handle Yes button click
# def on_yes_click(output_container):
#     st.session_state.show_confirmation = False
#     st.session_state.show_error_message = False
#     execute_query(st.session_state.current_question, output_container)

# # Function to handle No button click
# def on_no_click():
#     st.session_state.show_confirmation = False
#     st.session_state.show_error_message = True

# # Streamlit App
# question = st.text_input("Input your question: ", key="input")
# submit = st.button("Ask the question")

# # Create an output container for the query result
# output_container = st.container()

# # If submit is clicked
# if submit:
#     st.session_state.current_question = question
#     # Check for synonym in the question
#     synonym_match = check_for_synonyms(question)
    
#     if synonym_match:
#         st.session_state.show_confirmation = True
#         st.write(f"Do you mean '{synonym_match}'?")
        
#         col1, col2 = st.columns(2)
#         with col1:
#             st.button("Yes", on_click=on_yes_click, args=(output_container,), key="yes_button")
#         with col2:
#             st.button("No", on_click=on_no_click, key="no_button")
            
#     else:
#         execute_query(question, output_container)

# # Show error message if No was clicked
# if st.session_state.show_error_message:
#     with output_container:
#         st.error("Please input a valid query")






