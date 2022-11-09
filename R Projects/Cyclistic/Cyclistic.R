install.packages("tidyverse")
install.packages("janitor")
install.packages("lubridate")
install.packages("patchwork")
install.packages("rmarkdown")


library(tidyverse)
library(janitor)
library(lubridate)
library(ggplot2)
library(patchwork)
library(scales)
library(readr)
library(dplyr)


setwd("C:\\Users\\mader\\OneDrive\\Desktop\\Capstone Data")

rm(list=ls())
dir("C:/Users/mader/OneDrive/Desktop/Capstone Data", full.names = T)


m1 <- read.csv("202110-divvy-tripdata.csv")
m2 <- read.csv("202111-divvy-tripdata.csv")
m3 <- read.csv("202112-divvy-tripdata.csv")
m4 <- read.csv("202201-divvy-tripdata.csv")
m5 <- read.csv("202202-divvy-tripdata.csv")
m6 <- read.csv("202203-divvy-tripdata.csv")
m7 <- read.csv("202204-divvy-tripdata.csv")
m8 <- read.csv("202205-divvy-tripdata.csv")
m9 <- read.csv("202206-divvy-tripdata.csv")
m10 <- read.csv("202207-divvy-tripdata.csv")
m11 <- read.csv("202208-divvy-tripdata.csv")
m12 <- read.csv("202209-divvy-publictripdata.csv")

# combine all 12 months into one data frame 
bike_trips <- rbind(m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12)

# clean empty rows/columns
bike_trips <- janitor::remove_empty(bike_trips,which = c("cols"))
bike_trips <- janitor::remove_empty(bike_trips,which = c("rows"))

# clean date formats
bike_trips$started_time <- lubridate::ymd_hms(bike_trips$started_at)
bike_trips$end_time <- lubridate::ymd_hms(bike_trips$ended_at)

# create column for trip duration
bike_trips$trip_duration <- difftime(bike_trips$ended_at,bike_trips$started_at)

# create column for day of week
bike_trips$weekday <- lubridate::wday(bike_trips$started_at, label=TRUE, abbr=FALSE)

# create column for month
bike_trips$month <- lubridate::month(bike_trips$started_at, label=TRUE, abbr=FALSE)

# convert trip_duration to numeric and check
is.factor(bike_trips$trip_duration)
bike_trips$trip_duration <- as.numeric(as.character(bike_trips$trip_duration))
is.numeric(bike_trips$trip_duration)

# remove any negative (-) or "0" ride length
bike_trips_2 <- bike_trips[!(bike_trips$trip_duration <= 0),]

# split the data into member data and casual riders data
data_for_casual<-bike_trips_2 %>% filter(member_casual=="casual")
data_for_member<-bike_trips_2 %>% filter(member_casual=="member")

######### Work with time
# convert seconds to minutes and check
bike_trips_2$trip_duration_minutes <- bike_trips_2$trip_duration / 60
data_for_casual$trip_duration_minutes <- data_for_casual$trip_duration /60
data_for_member$trip_duration_minutes <- data_for_member$trip_duration /60
summary(bike_trips_2$trip_duration_minutes)
summary(data_for_casual$trip_duration_minutes)
summary(data_for_member$trip_duration_minutes)

# find starting hour for each data frame
data_for_casual$start_hour <- format(as.POSIXct(data_for_casual$started_time), format = "%H")
data_for_member$start_hour <- format(as.POSIXct(data_for_member$started_time), format = "%H")
bike_trips_2$start_hour <- format(as.POSIXct(bike_trips_2$started_time), format = "%H")

# Overview/summary of current step data
summary(bike_trips_2$trip_duration_minutes)
summary(data_for_casual)
summary(data_for_member)

# Mean/Median/Max/Min of all data frames
aggregate(bike_trips_2$trip_duration_minutes ~ bike_trips_2$member_casual, FUN = mean) 
aggregate(bike_trips_2$trip_duration_minutes ~ bike_trips_2$member_casual, FUN = median)
aggregate(bike_trips_2$trip_duration_minutes ~ bike_trips_2$member_casual, FUN = max)
aggregate(bike_trips_2$trip_duration_minutes ~ bike_trips_2$member_casual, FUN = min)

aggregate(bike_trips_2$trip_duration_minutes ~ bike_trips_2$member_casual + bike_trips_2$weekday, FUN = mean)



# Create overview visuals for casual vs member
## Types of riders (group)
ggplot(bike_trips_2, aes(x=member_casual)) + geom_bar()+
  labs(title="What types of riders ride the bikes",x="Rider type",y="# of riders")

## Types of riders by  bike (group)
ggplot(bike_trips_2, aes(x=member_casual, fill = rideable_type)) + geom_bar()+
  labs(title="What type of riders ride the bikes by bike type",x="Rider type",y="# of riders")

## Most popular bikes by member (group)
ggplot(bike_trips_2, aes(x=rideable_type, fill = member_casual)) + geom_bar()+
  labs(title="What type of bike do member/casual riders use?",x="Bike type",y="# of riders")

## Rides per day of week by member (group)
ggplot(bike_trips_2, aes(x=weekday, fill = member_casual)) + geom_bar()+
  labs(title="What is the most popular day for a bike ride?",x="weekday",y="# of riders")

## Rides per month (group)
ggplot(bike_trips_2, aes(x=month, fill = member_casual)) + geom_bar()+
  labs(title="What is the most popular month for bike rides?",x="month",y="# of riders")



# Create visuals for member data
## Types of riders with bike type
ggplot(data_for_member, aes(x=member_casual, fill = rideable_type)) + geom_bar()+
  labs(title="What type of bikes member riders use?",x="Rider type",y="# of riders")

## Most popular bikes (member)
ggplot(data_for_member, aes(x=rideable_type, fill=month)) + geom_bar()+
  labs(title="What type of bike do member riders use?",x="Bike type",y="# of riders")

## Rides per day of week (member)
ggplot(bike_trips_2, aes(x=weekday, fill = month)) + geom_bar()+
  labs(title="Rides per Day of the Week",x="Rider type",y="# of riders")

## Rides per month (member)
ggplot(data_for_member, aes(x=month, fill=weekday)) + geom_bar()+
  labs(title="What is the most popular month for member bike rides?",x="month",y="# of riders")

# Create visuals for casual data
## Types of riders 
  ggplot(data_for_member, aes(x=member_casual, fill = rideable_type)) + geom_bar()+
  labs(title="What type of bikes do casual riders use?",x="Rider type",y="# of riders")

## Most popular bikes (casual)
ggplot(data_for_member, aes(x=rideable_type, fill=month)) + geom_bar()+
  labs(title="What type of bike do casual riders use by month?",x="Bike type",y="# of riders")

## Rides per day of week (casual)
ggplot(data_for_member, aes(x=weekday, fill = month)) + geom_bar()+
  labs(title="most popular days for casual bike rides",x="weekday",y="# of riders")

## Rides per month (casual)
ggplot(data_for_member, aes(x=month, fill = weekday)) + geom_bar()+
  labs(title="What is the most popular month for casual bike rides?",x="month",y="# of riders")

# plot data about starting hour for each data frame
ggplot(data_for_casual, aes(x=start_hour, fill=weekday)) + geom_bar(stat="count")+
  labs(title="riders/hour for casual riders", x="starting hour", y="# of riders")

ggplot(data_for_member, aes(x=start_hour, fill=weekday)) + geom_bar(stat="count")+
  labs(title="riders/hour for member riders", x="starting hour", y="# of riders")

ggplot(bike_trips_2, aes(x=start_hour, fill=member_casual)) + geom_bar(stat="count")+
  labs(title="Riders per hour by type", x="starting hour", y="# of riders")

#average trip duration
bike_trips_2 %>% 
  mutate(weekday = wday(started_at, label = TRUE)) %>% 
  group_by(member_casual, weekday) %>% 
  summarise(number_of_rides = n()
            ,average_duration = mean(trip_duration_minutes)) %>% 
  arrange(member_casual, weekday)  %>% 
  ggplot(aes(x = weekday, y = number_of_rides, fill = member_casual)) +
  geom_col(position = "dodge")

