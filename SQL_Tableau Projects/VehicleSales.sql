---Inspect data
select * from "Data" limit 20

---Checking unique values
select distinct status from "Data" 
select distinct YEAR_ID  from "Data" 
select distinct PRODUCTLINE  from "Data" 
select distinct COUNTRY  from "Data" 
select distinct DEALSIZE  from "Data" 
select distinct TERRITORY  from "Data" 

select distinct MONTH_ID from "Data" 
where YEAR_ID = 2005


---Analysis
--group sales by product line
select PRODUCTLINE, sum(sales) Revenue
from "Data" 
group by PRODUCTLINE 
order by 2 DESC 

select YEAR_ID, sum(sales) Revenue
from "Data" 
group by YEAR_ID 
order by 2 DESC 

---year 2005 has unusually low sales, check to see if all years have data from all 12 months
--
select distinct MONTH_ID from "Data" where YEAR_ID = 2003 
select distinct MONTH_ID from "Data" where YEAR_ID = 2004
select distinct MONTH_ID from "Data" where YEAR_ID = 2005


--dealsize revenue
select DEALSIZE , sum(sales) Revenue
from "Data" 
group by DEALSIZE  
order by 2 DESC 



--what is the best month for sales in a specific year? how much was earned that month?
--all years combined
select MONTH_ID , SUM(SALES) Revenue, count (ORDERNUMBER) Frequency
FROM "Data" 
group by MONTH_ID 
order by 2 DESC 
--2003
select MONTH_ID , SUM(SALES) Revenue, count (ORDERNUMBER) Frequency
FROM "Data" 
WHERE YEAR_ID = 2003
group by MONTH_ID 
order by 2 DESC
--2004
select MONTH_ID , SUM(SALES) Revenue, count (ORDERNUMBER) Frequency
FROM "Data" 
WHERE YEAR_ID = 2004
group by MONTH_ID 
order by 2 DESC 
--2005
select MONTH_ID , SUM(SALES) Revenue, count (ORDERNUMBER) Frequency
FROM "Data" 
WHERE YEAR_ID = 2005
group by MONTH_ID 
order by 2 DESC 

---November Analysis
--all novembers 2003-2005
select MONTH_ID , PRODUCTLINE , sum(sales) Revenue, count(ORDERNUMBER)
FROM "Data" 
WHERE  MONTH_ID = 11 --change year and month to see other years and months
GROUP BY MONTH_ID , PRODUCTLINE 
order by 3 DESC 
-- nov 2005
select MONTH_ID , PRODUCTLINE , sum(sales) Revenue, count(ORDERNUMBER)
FROM "Data" 
WHERE YEAR_ID = 2005 and MONTH_ID = 11 --change year and month to see other years and months
GROUP BY MONTH_ID , PRODUCTLINE 
order by 3 DESC 
--all of 2005
select MONTH_ID , PRODUCTLINE , sum(sales) Revenue, count(ORDERNUMBER)
FROM "Data" 
WHERE YEAR_ID = 2005 --change year and month to see other years and months
GROUP BY  PRODUCTLINE 
order by 3 DESC 
--nov 2004
select MONTH_ID , PRODUCTLINE , sum(sales) Revenue, count(ORDERNUMBER)
FROM "Data" 
WHERE YEAR_ID = 2004 and MONTH_ID = 11 --change year and month to see other years and months
GROUP BY MONTH_ID , PRODUCTLINE 
order by 3 DESC 
--all of 2004
select MONTH_ID , PRODUCTLINE , sum(sales) Revenue, count(ORDERNUMBER)
FROM "Data" 
WHERE YEAR_ID = 2004 --change year and month to see other years and months
GROUP BY  PRODUCTLINE 
order by 3 DESC 
--nov 2003
select MONTH_ID , PRODUCTLINE , sum(sales) Revenue, count(ORDERNUMBER), YEAR_ID 
FROM "Data" 
WHERE YEAR_ID = 2003 and MONTH_ID = 11  --change year and month to see other years and months
GROUP BY MONTH_ID , PRODUCTLINE 
order by 3 DESC 
--all of 2003
select MONTH_ID , PRODUCTLINE , sum(sales) Revenue, count(ORDERNUMBER)
FROM "Data" 
WHERE YEAR_ID = 2003 --change year and month to see other years and months
GROUP BY  PRODUCTLINE 
order by 3 DESC 

---who is our best customer
--recency - last order date
--frequency - count of total orders
--monetary value - total spend

SELECT CUSTOMERNAME, max(ORDERDATE), avg(sales) as Avg_spend, count(ORDERNUMBER) as sales_count, sum(sales) as Revenue
FROM "Data" 
GROUP BY CUSTOMERNAME 
ORDER BY 4 DESC 


--region with most sales volume (by state, territory, country, city)
SELECT TERRITORY, sum(sales) as Revenue
from "Data" 
Group by TERRITORY 
order by 2 DESC 
--
SELECT STATE , sum(sales) as Revenue
from "Data" 
Group by STATE  
order by 2 DESC 
--
SELECT COUNTRY, sum(sales) as Revenue
from "Data" 
Group by COUNTRY  
order by 2 DESC 
--
SELECT CITY, sum(sales) as Revenue
from "Data" 
Group by CITY 
order by 2 DESC 
--
SELECT POSTALCODE, sum(sales) as Revenue
from "Data" 
Group by POSTALCODE  
order by 2 DESC 

--dealsize information 
--sum of deals
SELECT DEALSIZE, sum(SALES) as Revenue
FROM "Data" 
group by DEALSIZE 
--count of sales
SELECT DEALSIZE, count(DEALSIZE) as Deals
FROM "Data" 
group by DEALSIZE 

--product line information 
--sum of sales
SELECT PRODUCTLINE, sum(sales) as Revenue
from "Data" 
Group by PRODUCTLINE  
order by 2 DESC 
--count of sales
SELECT PRODUCTLINE,  count(sales) as Deals 
from "Data"  
group by PRODUCTLINE 
order by 2 DESC 




