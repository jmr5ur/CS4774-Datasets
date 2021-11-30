# This will take raw data and compile it into one nice CSV :)
# create the file and do other necessary init.
f = open('data/cleanData.csv','w')
countyDataDic = {}
countyDataDicYear = {}
countyToFIPS = {}
# begin by adding bee data
beeData = open('BeeColonyCensusNew.csv','r')
first = True
i = 0
for line in beeData.readlines():
    if first:
        first = False
        continue
    lineSplit = line.replace('"','').split(',')

    fips = lineSplit[3].zfill(2)+lineSplit[7].zfill(3)
    # update the data dict
    if fips not in countyDataDic.keys():
        countyDataDic[fips] = [fips, lineSplit[6], 'No data','No data','No data']
        countyDataDicYear[(fips,2002)] = [2002,fips, lineSplit[6], 'No data']
        countyDataDicYear[(fips,2007)] = [2007,fips, lineSplit[6], 'No data']
        countyDataDicYear[(fips,2012)] = [2012,fips, lineSplit[6], 'No data']
        countyDataDicYear[(fips,2017)] = [2017,fips, lineSplit[6], 'No data']
    year = lineSplit[0]
    if year == '2012':
        try:
            countyDataDic[fips][2] = int(lineSplit[8])
            countyDataDicYear[(fips,2012)][3] = int(lineSplit[8])
        except:
            countyDataDic[fips][2] = lineSplit[8]
            countyDataDicYear[(fips,2012)][3] = lineSplit[8]
    elif year == '2007':
        try:
            countyDataDic[fips][3] = int(lineSplit[8])
            countyDataDicYear[(fips,2007)][3] = int(lineSplit[8])
        except:
            countyDataDic[fips][3] = lineSplit[8]
            countyDataDicYear[(fips,2007)][3] = lineSplit[8]
    elif year == '2002':
        try:
            countyDataDic[fips][4] = int(lineSplit[8])
            countyDataDicYear[(fips,2002)][3] = int(lineSplit[8])
        except:
            countyDataDic[fips][4] = lineSplit[8]
            countyDataDicYear[(fips,2002)][3] = lineSplit[8]
    elif year == '2017':
        try:
            countyDataDic[fips][4] = int(lineSplit[8])
            countyDataDicYear[(fips,2017)][3] = int(lineSplit[8])
        except:
            countyDataDic[fips][4] = lineSplit[8]
            countyDataDicYear[(fips,2017)][3] = lineSplit[8]
    else:
        print('something went wrong!')
    # update the countyToFIPS dict
    countyToFIPS[lineSplit[6].lower()] = fips
beeData.close()

# now we'll read in air quality
# for the sake of openness and not removing that which may be useful later, I'm gonna leave all this code in even though
# none of this is going into the final data
print('***2012***')
aqi2012 = open('annual_aqi_by_county_2012.csv','r')
first = True
for line in aqi2012.readlines():
    if first:
        first=False
        continue
    lineSplit = line.split(',')
    try:
        # add the avg aqi for the year to the dictionary (lower is better)
        fips = countyToFIPS[lineSplit[1].replace('"','').lower()]
        avg = (int(lineSplit[4])*1+int(lineSplit[5])*2+int(lineSplit[6])*3+int(lineSplit[7])*3+int(lineSplit[8])*4+int(lineSplit[9])*5+int(lineSplit[10])*6)/int(lineSplit[3])
        countyDataDic[fips].append(avg)
    except:
        # print(lineSplit[1].replace('"','')+" not found")
        pass
aqi2012.close()
# for any county for whihc there is no data this year, mark that
for key in countyDataDic.keys():
    if len(countyDataDic[key]) != 6:
        countyDataDic[key].append('No data')

aqi2007 = open('annual_aqi_by_county_2007.csv','r')
print('***2007***')
first = True
for line in aqi2007.readlines():
    if first:
        first=False
        continue
    lineSplit = line.split(',')
    try:
        # add the avg aqi for the year to the dictionary (lower is better)
        fips = countyToFIPS[lineSplit[1].replace('"','').lower()]
        avg = (int(lineSplit[4])*1+int(lineSplit[5])*2+int(lineSplit[6])*3+int(lineSplit[7])*3+int(lineSplit[8])*4+int(lineSplit[9])*5+int(lineSplit[10])*6)/int(lineSplit[3])
        countyDataDic[fips].append(avg)
    except:
        # print(lineSplit[1].replace('"','')+" not found")
        pass
aqi2007.close()
# for any county for whihc there is no data this year, mark that
for key in countyDataDic.keys():
    if len(countyDataDic[key]) != 7:
        countyDataDic[key].append('No data')
print('***2002***')
aqi2002 = open('annual_aqi_by_county_2002.csv','r')
first = True
for line in aqi2002.readlines():
    if first:
        first=False
        continue
    lineSplit = line.split(',')
    try:
        # add the avg aqi for the year to the dictionary (lower is better)
        fips = countyToFIPS[lineSplit[1].replace('"','').lower()]
        avg = (int(lineSplit[4])*1+int(lineSplit[5])*2+int(lineSplit[6])*3+int(lineSplit[7])*3+int(lineSplit[8])*4+int(lineSplit[9])*5+int(lineSplit[10])*6)/int(lineSplit[3])
        countyDataDic[fips].append(avg)
    except:
        # print(lineSplit[1].replace('"','')+" not found")
        pass
aqi2002.close()
# for any county for whihc there is no data this year, mark that
for key in countyDataDic.keys():
    if len(countyDataDic[key]) != 8:
        countyDataDic[key].append('No data')
# read in the new air quality data : as a note, more data can be added here lol
aqpm25 = open('aq_pm25_2.csv','r')
first = True
i=0
for line in aqpm25.readlines():
    if first:
        first = False
        continue
    lineSplit = line.replace('"','').split(',')
    fips = lineSplit[2]
    try:
        if lineSplit[4] == "2002":
            countyDataDicYear[(fips,2002)].append(float(lineSplit[5]))
        elif lineSplit[4] == "2007":
            countyDataDicYear[(fips,2007)].append(float(lineSplit[5]))
        elif lineSplit[4] == "2012":
            countyDataDicYear[(fips, 2012)].append(float(lineSplit[5]))
        elif lineSplit[4] == "2016":
            countyDataDicYear[(fips, 2017)].append(float(lineSplit[5]))
    except KeyError: # this should only be reached if there is some sort of keyerror (we haven't seen bee data, so for now we'll just skip)
        pass
# Time to read in the pesticide use data here
pest2012 = open('EPest.county.estimates.2012.txt', 'r')
first = True
pest2012Dic = {}
i = 0
for line in pest2012.readlines():
    lineSplit = line.split('\t')
    if first:
        first = False
        continue
    fips = lineSplit[2] + lineSplit[3]
    if fips not in pest2012Dic.keys():
        pest2012Dic[fips] = 0
    # add the low estimate (some only have high estimate, so this is easiest)
    # print(lineSplit[-1].replace('\n',''),lineSplit[-2],i)
    lowEst = lineSplit[-2]
    highEst = lineSplit[-1].replace('\n','')
    if lowEst == '':
        lowEst = highEst
    if highEst == '':
        highEst = lowEst
    pest2012Dic[fips] += (float(highEst)+float(lowEst))/2
    i+=1
for key in countyDataDic.keys():
    try:
        # if the key is in our pest dict, add the estimated pesticide usage to CDD
        countyDataDic[key].append(pest2012Dic[key])
        countyDataDicYear[(key, 2012)].append(pest2012Dic[key])
    except:
        # otherwise, add a no data marker
        countyDataDic[key].append('No data')
        countyDataDicYear[(key, 2012)].append('No data')
pest2012.close()

pest2007 = open('EPest.county.estimates.2007.txt', 'r')
first = True
pest2007Dic = {}
i = 0
for line in pest2007.readlines():
    lineSplit = line.split('\t')
    if first:
        first = False
        continue

    fips = lineSplit[2] + lineSplit[3]
    if fips not in pest2007Dic.keys():
        pest2007Dic[fips] = 0
    # add midpoint of estimates (in cases where there is only one value, just take that value)
    # print(lineSplit[-1].replace('\n',''),lineSplit[-2],i)
    lowEst = lineSplit[-2]
    highEst = lineSplit[-1].replace('\n','')
    if lowEst == '':
        lowEst = highEst
    if highEst == '':
        highEst = lowEst
    pest2007Dic[fips] += (float(highEst)+float(lowEst))/2
    i+=1
for key in countyDataDic.keys():
    try:
        # if the key is in our pest dict, add the estimated pesticide usage to CDD
        countyDataDic[key].append(pest2007Dic[key])
        countyDataDicYear[(key, 2007)].append(pest2007Dic[key])
    except:
        # otherwise, add a no data marker
        countyDataDic[key].append('No data')
        countyDataDicYear[(key, 2007)].append('No data')
pest2007.close()

pest2002 = open('EPest.county.estimates.2002.txt', 'r')
first = True
pest2002Dic = {}
i = 0
for line in pest2002.readlines():
    lineSplit = line.split('\t')
    if first:
        first = False
        continue

    fips = lineSplit[2] + lineSplit[3]
    if fips not in pest2002Dic.keys():
        pest2002Dic[fips] = 0
    # add midpoint of estimates (in cases where there is only one value, just take that value)
    # print(lineSplit[-1].replace('\n',''),lineSplit[-2],i)
    lowEst = lineSplit[-2]
    highEst = lineSplit[-1].replace('\n','')
    if lowEst == '':
        lowEst = highEst
    if highEst == '':
        highEst = lowEst
    pest2002Dic[fips] += (float(highEst)+float(lowEst))/2
    i+=1
for key in countyDataDic.keys():
    try:
        # if the key is in our pest dict, add the estimated pesticide usage to CDD
        countyDataDic[key].append(pest2002Dic[key])
        countyDataDicYear[(key, 2002)].append(pest2002Dic[key])
    except:
        # otherwise, add a no data marker
        countyDataDic[key].append('No data')
        countyDataDicYear[(key, 2002)].append('No data')
pest2007.close()
# add empty data to all vals
for key in countyDataDicYear.keys():
    countyDataDicYear[key].append('No data')
# 2017 pest data
pest2017 = open('EPest.county.estimates.2007.txt', 'r')
first = True
pest2017Dic = {}
i = 0
for line in pest2017.readlines():
    lineSplit = line.split('\t')
    if first:
        first = False
        continue

    fips = lineSplit[2] + lineSplit[3]
    if fips not in pest2007Dic.keys():
        pest2007Dic[fips] = 0
    # add midpoint of estimates (in cases where there is only one value, just take that value)
    # print(lineSplit[-1].replace('\n',''),lineSplit[-2],i)
    if lineSplit[1] == '2017':
        lowEst = lineSplit[-2]
        highEst = lineSplit[-1].replace('\n','')
        if lowEst == '':
            lowEst = highEst
        if highEst == '':
            highEst = lowEst
        pest2017Dic[fips] += (float(highEst)+float(lowEst))/2
    i+=1
for key in countyDataDic.keys():
    try:
        # if the key is in our pest dict, add the estimated pesticide usage to CDD
        countyDataDic[key].append(pest2017Dic[key])
        countyDataDicYear[(key, 2017)].append(pest2017Dic[key])
    except:
        # otherwise, add a no data marker
        countyDataDic[key].append('No data')
        countyDataDicYear[(key, 2017)].append('No data')
pest2007.close()
# do the water data
water2013 = open('2013CountyHealthRankingsNationalDataCSV.csv','r')
i = 0
for line in water2013.readlines():
    # do the actual parsing lol
    try:
        lineSplit = line.split(',')
        fips = lineSplit[0]
        presence = int(lineSplit[-11]) > 0
        if presence:
            countyDataDicYear[(fips, 2012)][-1] = "Yes"
        else:
            countyDataDicYear[(fips, 2012)][-1] = 'No'
        print(countyDataDicYear[((fips, 2012))])
    except:
        # there's nothing to do here except for skip over this data point
        pass
    i += 1
water2017 = open('2017CountyHealthRankingsDataCSV.csv','r')
for line in water2017.readlines():
    try:
        lineSplit = line.split(',')
        fips = lineSplit[0]
        countyDataDicYear[(fips, 2017)][-1]=lineSplit[-19]
        print(countyDataDicYear[(fips, 2017)][-1])
    except:
        pass
headers1 = ['FIPS','County','2012_colonies','2007_colonies','2002_colonies',
        '2012_avg_aqi','2007_avg_aqi', '2002_avg_aqi',
        '2012_pest_e','2007_pest_e','2002_pest_e']
headers2 = ["year",'fips','county','num_colonies', 'AQ_PM2.5','pest_e','water_viol']
f2 = open('data/cleanData2.csv','w')
f.write(','.join(headers2)+'\n')
f2.write(','.join(headers1)+'\n')
for key in countyDataDic.keys():
    for i in range(len(countyDataDic[key])):
        countyDataDic[key][i] = str(countyDataDic[key][i])
    f2.write(','.join(countyDataDic[key])+'\n')
count = 0
for key in countyDataDicYear.keys():
    if len(countyDataDicYear[key]) == 7:
        for i in range(len(countyDataDicYear[key])):
            countyDataDicYear[key][i] = str(countyDataDicYear[key][i])
        f.write(','.join(countyDataDicYear[key])+'\n')
    count += 1
print(count)
f.close()
print(countyDataDicYear)
# print(countyDataDic)
# AS A NOTE: This script is pretty easily modular, just need to add the specific code to parse whatever dataset you're using
# ALSO OF NOTE: We currently don't have water quality data, that is difficult to work with, looking for alt. sources