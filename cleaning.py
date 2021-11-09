# This will take raw data and compile it into one nice CSV :)
# create the file and do other necessary init.
f = open('data/cleanData.csv','w')
countyDataDic = {}
countyToFIPS = {}
# begin by adding bee data
beeData = open('Bee Colony Census Data by County.csv','r')
first = True
for line in beeData.readlines():
    if first:
        first = False
        continue
    lineSplit = line.split(',')
    if lineSplit[2] == 'VIRGINIA':
        fips = lineSplit[3].zfill(2)+lineSplit[7].zfill(3)
        # update the data dict
        if fips not in countyDataDic.keys():
            countyDataDic[fips] = [fips, lineSplit[6], 'No data','No data','No data']
        year = lineSplit[0]
        if year == '2012':
            try:
                countyDataDic[fips][2] = int(lineSplit[8])
            except:
                countyDataDic[fips][2] = lineSplit[8]
        elif year == '2007':
            try:
                countyDataDic[fips][3] = int(lineSplit[8])
            except:
                countyDataDic[fips][3] = lineSplit[8]
        elif year == '2002':
            try:
                countyDataDic[fips][4] = int(lineSplit[8])
            except:
                countyDataDic[fips][4] = lineSplit[8]
        else:
            print('something went wrong!')
        # update the countyToFIPS dict
        countyToFIPS[lineSplit[6].lower()] = fips
beeData.close()

# now we'll read in air quality
print('***2012***')
aqi2012 = open('annual_aqi_by_county_2012.csv','r')
first = True
for line in aqi2012.readlines():
    if first:
        first=False
        continue
    lineSplit = line.split(',')
    if lineSplit[0] == '"Virginia"':
        try:
            # add the avg aqi for the year to the dictionary (lower is better)
            fips = countyToFIPS[lineSplit[1].replace('"','').lower()]
            avg = (int(lineSplit[4])*1+int(lineSplit[5])*2+int(lineSplit[6])*3+int(lineSplit[7])*3+int(lineSplit[8])*4+int(lineSplit[9])*5+int(lineSplit[10])*6)/int(lineSplit[3])
            countyDataDic[fips].append(avg)
        except:
            print(lineSplit[1].replace('"','')+" not found")
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
    if lineSplit[0] == '"Virginia"':
        try:
            # add the avg aqi for the year to the dictionary (lower is better)
            fips = countyToFIPS[lineSplit[1].replace('"','').lower()]
            avg = (int(lineSplit[4])*1+int(lineSplit[5])*2+int(lineSplit[6])*3+int(lineSplit[7])*3+int(lineSplit[8])*4+int(lineSplit[9])*5+int(lineSplit[10])*6)/int(lineSplit[3])
            countyDataDic[fips].append(avg)
        except:
            print(lineSplit[1].replace('"','')+" not found")
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
    if lineSplit[0] == '"Virginia"':
        try:
            # add the avg aqi for the year to the dictionary (lower is better)
            fips = countyToFIPS[lineSplit[1].replace('"','').lower()]
            avg = (int(lineSplit[4])*1+int(lineSplit[5])*2+int(lineSplit[6])*3+int(lineSplit[7])*3+int(lineSplit[8])*4+int(lineSplit[9])*5+int(lineSplit[10])*6)/int(lineSplit[3])
            countyDataDic[fips].append(avg)
        except:
            print(lineSplit[1].replace('"','')+" not found")
            pass
aqi2002.close()
# for any county for whihc there is no data this year, mark that
for key in countyDataDic.keys():
    if len(countyDataDic[key]) != 8:
        countyDataDic[key].append('No data')

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
    if lineSplit[2] == '51':
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
    except:
        # otherwise, add a no data marker
        countyDataDic[key].append('No data')
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
    if lineSplit[2] == '51':
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
    except:
        # otherwise, add a no data marker
        countyDataDic[key].append('No data')
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
    if lineSplit[2] == '51':
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
    except:
        # otherwise, add a no data marker
        countyDataDic[key].append('No data')
pest2007.close()

headers=['FIPS','County','2012_colonies','2007_colonies','2002_colonies',
        '2012_avg_aqi','2007_avg_aqi', '2002_avg_aqi',
        '2012_pest_e','2007_pest_e','2002_pest_e']
f.write(','.join(headers)+'\n')
for key in countyDataDic.keys():
    for i in range(len(countyDataDic[key])):
        countyDataDic[key][i] = str(countyDataDic[key][i])
    f.write(','.join(countyDataDic[key])+'\n')

f.close()
print(countyDataDic)
# AS A NOTE: This script is pretty easily modular, just need to add the specific code to parse whatever dataset you're using
# ALSO OF NOTE: We currently don't have water quality data, that is difficult to work with, looking for alt. sources