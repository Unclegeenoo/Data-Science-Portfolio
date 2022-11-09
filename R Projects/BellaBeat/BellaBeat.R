#set up environment

install.packages("tidyverse")
install.packages("janitor")
install.packages("lubridate")
install.packages("patchwork")
install.packages("rmarkdown")
install.packages("psych")

library(tidyverse)
library(janitor)
library(lubridate)
library(ggplot2)
library(patchwork)
library(scales)
library(readr)
library(dplyr)
library(psych)


setwd("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16")

rm(list=ls())
dir("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16", full.names = T)

activity_daily <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/dailyActivity_merged.csv")  
calories_daily <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/dailyCalories_merged.csv")
intensities_daily <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/dailyIntensities_merged.csv")
steps_daily <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/dailySteps_merged.csv")  
heartrate_seconds <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/heartrate_seconds_merged.csv")  
calories_hourly <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/hourlyCalories_merged.csv") 
intensities_hourly <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/hourlyIntensities_merged.csv") 
steps_hourly <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/hourlySteps_merged.csv")  
calories_narrow_minute <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/minuteCaloriesNarrow_merged.csv")     
calories_wide_minute <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/minuteCaloriesWide_merged.csv") 
intensities_narrow_minute <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/minuteIntensitiesNarrow_merged.csv")
intensities_wide_minute <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/minuteIntensitiesWide_merged.csv")
mets_narrow_minute <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/minuteMETsNarrow_merged.csv") 
sleep_minute <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/minuteSleep_merged.csv") 
steps_narrow_minute <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/minuteStepsNarrow_merged.csv") 
steps_wide_minute <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/minuteStepsWide_merged.csv") 
sleep_day <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/sleepDay_merged.csv")
weight_loginfo <- read.csv("C:/Users/mader/OneDrive/Desktop/Capstone Data/Fitabase Data 4.12.16-5.12.16/weightLogInfo_merged.csv")


#Check how many distinct ids the data set has
n_distinct(activity_daily$Id)
n_distinct(calories_daily$Id)
n_distinct(calories_hourly$Id)
n_distinct(calories_narrow_minute$Id)
n_distinct(calories_wide_minute$Id)
n_distinct(heartrate_seconds$Id)
n_distinct(intensities_daily$Id)
n_distinct(intensities_hourly$Id)
n_distinct(intensities_narrow_minute$Id)
n_distinct(intensities_wide_minute$Id)
n_distinct(mets_narrow_minute$Id)
n_distinct(sleep_day$Id)
n_distinct(sleep_minute$Id)
n_distinct(steps_daily$Id)
n_distinct(steps_hourly$Id)
n_distinct(steps_narrow_minute$Id)
n_distinct(steps_wide_minute$Id)
n_distinct(weight_loginfo$Id)


# summarize data
summary(activity_daily)
summary(calories_daily)
summary(calories_hourly)
summary(calories_narrow_minute)
summary(heartrate_seconds)
summary(intensities_daily)
summary(intensities_hourly)
summary(intensities_narrow_minute)
summary(mets_narrow_minute)
summary(sleep_day)
summary(sleep_minute)
summary(steps_daily)
summary(steps_hourly)
summary(steps_narrow_minute)
summary(weight_loginfo)

# check for null values in ever column
is.null(activity_daily)
is.null(calories_daily)
is.null(calories_hourly)
is.null(calories_narrow_minute)
is.null(heartrate_seconds)
is.null(intensities_daily)
is.null(intensities_hourly)
is.null(intensities_narrow_minute)
is.null(mets_narrow_minute)
is.null(sleep_day)
is.null(sleep_minute)
is.null(steps_daily)
is.null(steps_hourly)
is.null(steps_narrow_minute)
is.null(weight_loginfo)


# add data columns
## total active minutes
activity_daily <- activity_daily %>% 
  mutate(total_active_minutes = VeryActiveMinutes+FairlyActiveMinutes+LightlyActiveMinutes)

intensities_daily <- intensities_daily %>% 
  mutate(total_active_minutes = VeryActiveMinutes+FairlyActiveMinutes+LightlyActiveMinutes)


## total minutes worn
activity_daily <- activity_daily %>% 
  mutate(total_minutes_worn = VeryActiveMinutes+FairlyActiveMinutes+LightlyActiveMinutes+SedentaryMinutes)

## total hours worn
activity_daily$total_hours_worn <- activity_daily$total_active_minutes / 60



# format Data Types (id to character, minutes to mins), make time columns identical format
activity_daily_formatted <- mutate(activity_daily, Id = as.character(Id),
                                   ActivityDate=as_date(ActivityDate, format=("%m/%d/%Y")))
                               

calories_daily_formatted <-  mutate(calories_daily, Id = as.character(Id),
                                    ActivityDate=as_date(ActivityDay, format=("%m/%d/%Y")))


intensities_daily_formatted <- mutate(intensities_daily, Id = as.character(Id),
                                      ActivityDate=as_date(ActivityDay, format=("%m/%d/%Y")))
                                   


sleep_day_formatted <-  mutate(sleep_day, Id = as.character(Id),
                               ActivityDate=as_date(SleepDay, format=("%m/%d/%Y")))
                     

weight_loginfo_formatted <- mutate(weight_loginfo, Id=as.character(Id),
                                   ActivityDate=as_date(Date, format=("%m/%d/%Y")))

steps_daily_formatted <- mutate(steps_daily, Id=as.character(Id),
                                ActivityDate=as_date(ActivityDay, format=("%m/%d/%Y")))

#Rename time/date column for consistency
sleep_day <- rename (sleep_day,
                     ActivityDate=SleepDay)

calories_daily <- rename(calories_daily, 
                         ActivityDate=ActivityDay)

intensities_daily <- rename(intensities_daily, 
                            ActivityDate=ActivityDay)

weight_loginfo <- rename(weight_loginfo, 
                         ActivityDate=Date)




#join into one frame
activity_sleep_combined <- full_join(activity_daily_formatted,sleep_day_formatted, by=c("Id","ActivityDate"))

activity_full <- full_join(activity_sleep_combined, weight_loginfo_formatted, by=c("Id","ActivityDate"))


# sumarize new data set
View(activity_full)
str(activity_full)
summary(activity_full)






# create summary rows/table
##customer id, total minutes active, total minutes asleep, amount of days worn, sedentary minutes, total steps per day
activity_count <- activity_daily_formatted %>% 
  group_by(Id) %>% 
  summarize(count=n())

average_steps <- steps_daily_formatted %>% 
  group_by(Id) %>% 
  summarize(mean(StepTotal))

average_active_minutes <- intensities_daily_formatted %>% 
  group_by(Id) %>% 
  summarize(mean(total_active_minutes))

average_sedentary_minutes <- intensities_daily_formatted %>% 
  group_by(Id) %>% 
  summarize(mean(SedentaryMinutes))


average_calories <- calories_daily_formatted %>% 
  group_by(Id) %>% 
  summarize(mean(Calories))

average_weight <- weight_loginfo_formatted %>% 
  group_by(Id) %>% 
  summarize(mean(WeightPounds))

average_bmi <- weight_loginfo_formatted %>% 
  group_by(Id) %>% 
  summarize(mean(BMI))

## Create dataframe with new summary rows

                                                                           
summary_table <- list(activity_count,
                      average_steps,
                      average_active_minutes,
                      average_sedentary_minutes,
                      average_calories,
                      average_weight,
                      average_bmi) %>% 
  reduce(left_join, by='Id')                                                                                    





# rename summary_table columns
summary_table <- rename (summary_table,
                     average_steps="mean(StepTotal)")

summary_table <- rename (summary_table,
                         average_active_minutes="mean(total_active_minutes)")

summary_table <- rename (summary_table,
                         average_sedentary_minutes="mean(SedentaryMinutes)")

summary_table <- rename (summary_table,
                         average_calories="mean(Calories)")

summary_table <- rename (summary_table,
                         average_weight="mean(WeightPounds)")

summary_table <- rename (summary_table,
                         average_bmi="mean(BMI)")


# total average minutes column
summary_table$total_average_minutes  <- rowSums(summary_table[ , c(4,5)])


# summarize summary_table dataframe

summary_table %>% 
  summarize(avg_steps=mean(average_steps), avg_active_minutes=mean(average_active_minutes),
            avg_sedentary_minutes=mean(average_sedentary_minutes), avge_calories = mean(average_calories), 
            avg_weight=mean(average_weight), avg_bmi = mean(average_bmi), 
            total_avg_hours=mean(total_average_minutes))


summary_avg_hours <- summary_table %>% 
  summarize(tibble(avg_steps=mean(average_steps), avg_active_hrs=mean(average_active_minutes / 60),
                   avg_sedentary_hrs=mean(average_sedentary_minutes / 60), avg_calories = mean(average_calories)), 
            total_avg_hrs=mean(total_average_minutes / 60)) %>% 
  print(summary_avg_hours, n = NULL, n_extra = NULL, width = getOption("width"))



# total average minutes column
summary_table$total_average_minutes  <- rowSums(summary_table[ , c(4,5)])
  
# visualization 
ggplot(data=summary_table, aes(x=average_steps, y=Id))+geom_bar(stat="identity")
ggplot(data=summary_table, aes(x=average_active_minutes, y=Id))+geom_bar(stat="identity")
ggplot(data=summary_table, aes(x=average_sedentary_minutes, y=Id))+geom_bar(stat="identity")
ggplot(data=summary_table, aes(x=average_calories, y=Id))+geom_bar(stat="identity")
ggplot(data=summary_table, aes(x=average_weight, y=Id))+geom_bar(stat="identity")
ggplot(data=summary_table, aes(x=average_bmi, y=Id))+geom_bar(stat="identity")

## pivot longer
summary_pivot <- summary_table %>% 
  pivot_longer(cols=c("average_sedentary_minutes", "average_active_minutes"),
               names_to="time_type",
               values_to="minutes")


## time comparison 
ggplot(summary_pivot, aes(x=Id, y=minutes, fill=time_type))+
  geom_col(position = "dodge")+
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1))

ggplot(summary_pivot, aes(x=minutes, fill=time_type, y=Id))+
  geom_col()+
  geom_text(aes(label=round(minutes),size=3))
  



