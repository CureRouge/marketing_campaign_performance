## load libraries
import pandas as pd # data manipulation
import seaborn as sns # data visualization
import numpy as np # data analysis
import matplotlib.pyplot as plt # data visualization
import scipy.stats as stats # statistical test
# produce plots
%matplotlib inline 
# set plotting style
plt.style.use('bmh')

# reading in the flat files
# for bid_requests
bid_requests = pd.read_csv('bid_requests.csv')
# for user_attributes.csv 
user_attributes = pd.read_csv('user_attributes.csv')

# split it into columns so the attributes can be explicitly used as features
user_attributes = pd.concat([user_attributes, #concatenate to the original df user_attributes 
                      pd.DataFrame(list(user_attributes.attributes.map(eval)))], #the extracted attributes from dictionary
                            axis = 1) # to columns
# map the user features to the bid requests by joining the data frames on user_id
bid_requests_attributes = pd.merge(bid_requests, user_attributes,  # join the data frames
                                       on = 'user_id').drop(columns = 'attributes') 
# on user_id, and drop the attributes

# plotting with seaborn
sns.set_style("white") # white background for contrast
plt.figure(figsize=(7, 6)) # adjust figure size
# Plot a filled kernel density estimate
x = sns.distplot(bid_requests_attributes['user_id'].value_counts(), 
                 hist=False, color="g", kde_kws={"shade": True})
x.set(xlabel='requests per user', ylabel='density');  # adjust label name

# only keep the won bids
bid_requests_attributes_won = bid_requests_attributes[bid_requests_attributes['win'] == 1]
# make the conversion to customer_id one-to-one relationship
bid_requests_attributes_won_sorted = bid_requests_attributes_won.sort_values(by = ['user_id','conversion'], 
                                        ascending= [False, False]).drop_duplicates(subset = 'user_id', keep = 'first')

# only keep the won bids
bid_requests_attributes_won = bid_requests_attributes[bid_requests_attributes['win'] == 1]# make the
#conversion to customer_id one-to-one relationship
bid_requests_attributes_won_sorted = bid_requests_attributes_won.sort_values(by = ['user_id','conversion'], 
                                        ascending= [False, False]).drop_duplicates(subset = 'user_id', keep = 'first')
# get the test/conversion 2X2 array combinations

# conversion = 1, test = 1
con_test = bid_requests_attributes_won[(bid_requests_attributes_won['conversion'] == 1) & (
                                                  bid_requests_attributes_won['test'] == 1)].user_id.nunique()
# conversion = 0, test = 1
nocon_test = bid_requests_attributes_won[(bid_requests_attributes_won['conversion'] == 0)&(
                                                    bid_requests_attributes_won['test'] == 1)].user_id.nunique()
# conversion = 1, test = 0
con_notest = bid_requests_attributes_won[(bid_requests_attributes_won['conversion'] == 0)&(
                                                    bid_requests_attributes_won['test'] == 1)].user_id.nunique()
# conversion = 1, test = 0
nocon_notest = bid_requests_attributes_won[(bid_requests_attributes_won['conversion'] == 0) &(
                                                      bid_requests_attributes_won['test'] == 0)].user_id.nunique()

print("not tested and not converted", nocon_notest)
print("not tested and converted", con_notest)
print("tested and converted", con_test)
print("tested and not converted", con_notest)

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels_not = 'not tested and not converted', 'not tested and converted'
sizes_not = [nocon_notest, con_notest]
explode_not = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

labels = 'tested and not converted', 'tested and converted'
sizes = [nocon_test, con_test]
explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()

ax1.pie(sizes_not, explode=explode_not, labels=labels_not, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


plt.show()
plt.show()

# Apply Fischer's exact test to get an estimate of enrichment in conversion due to new creative
oddsratio, pvalue = stats.fisher_exact([ [nocon_notest, con_notest],[nocon_test, con_test]])

print("oddsratio", oddsratio)
print("pvalue", pvalue)
