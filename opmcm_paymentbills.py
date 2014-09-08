# coding=utf-8
import bs4
import hashlib
import MySQLdb
import re
import requests

class BillingConsts(object):
    SN = 0
    DESCRIPTION = 1
    ACCOUNT_NO = 2
    EXPENSE_HEADING = 3
    PROCUREMENT_METHOD = 4
    PAN_NO = 5
    VENDOR = 6
    APPLICATION_DATE = 7
    AMOUNT = 8
    REMARKS = 9
    UPLOAD_DATETIME = 10
    AGENCY = 1000
    HASH = 2000


def getAgencyPageUrl(content):
    soup = bs4.BeautifulSoup(content)
    links = []
    for a in soup.select('div.wrapper div.bodypart div.centerbody font a'):
        links.append({'href': a.attrs.get('href'), 
            'name': a.text})
    return links

def getAgencyBills(content):
    soup = bs4.BeautifulSoup(content)
    trs = soup.select('div.innerbody table tr')
    allPaymentDetails = []
    for tr in trs:
        details = getBillDetails(str(tr))
        if len(details):
            allPaymentDetails.append(details)
    return allPaymentDetails

def extractDateFromTdValue(val):
    m = re.search(u'dd= "([^"]*)"', val)
    if m is None:
        return val.decode('utf-8')
    else:
        return m.group(1)


def getBillDetails(row):
    soup = bs4.BeautifulSoup(row)
    tds = soup.select('td')
    if 11 == len(tds) and "सि.नं" != tds[BillingConsts.SN].text.encode('utf-8'):
        # print extractDateFromTdValue(unicode(tds[BillingConsts.UPLOAD_DATETIME].text))
        return {
            BillingConsts.SN: tds[BillingConsts.SN].text,
            BillingConsts.DESCRIPTION: tds[BillingConsts.DESCRIPTION].text,
            BillingConsts.ACCOUNT_NO: tds[BillingConsts.ACCOUNT_NO].text,
            BillingConsts.EXPENSE_HEADING: tds[BillingConsts.EXPENSE_HEADING].text,
            BillingConsts.PROCUREMENT_METHOD: tds[BillingConsts.PROCUREMENT_METHOD].text,
            BillingConsts.PAN_NO: tds[BillingConsts.PAN_NO].text,
            BillingConsts.VENDOR: tds[BillingConsts.VENDOR].text,
            BillingConsts.APPLICATION_DATE: tds[BillingConsts.APPLICATION_DATE].text,
            BillingConsts.AMOUNT: tds[BillingConsts.AMOUNT].text,
            BillingConsts.REMARKS: tds[BillingConsts.REMARKS].text,
            BillingConsts.UPLOAD_DATETIME: extractDateFromTdValue(tds[BillingConsts.UPLOAD_DATETIME].text.encode('utf-8')),
        }
    return {}

def saveAgencyBillDetails(agency, agencyBillDetails):
    for bill in agencyBillDetails:
        insertBill

def getHash(billDetails):
    billTuple = [v for (k,v) in billDetails.iteritems()]
    return hashlib.sha256((''.join(billTuple)).encode('utf-8')).hexdigest()

def prepareBillSql(agency, billDetails):
    sql = "INSERT INTO bills VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    billTuple = [v for (k,v) in billDetails.iteritems()]
    billHash = getHash(billDetails)
    billSqlTuple = tuple([agency, billHash]) + tuple(billTuple)
    return {'sql': sql, 'val': billSqlTuple}

def insertBill(cur, agency, billDetails):
    sha = getHash(billDetails)
    numrows = cur.execute("select sha from bills where sha = '%s'" % sha)
    if not numrows:
        sqlParts = prepareBillSql(agency, billDetails)
        cur.execute(sqlParts['sql'], sqlParts['val'])

def main():
    db = MySQLdb.connect(host="localhost", # your host, usually localhost
                        user="root", # your username
                        passwd="", # your password
                        db="opendata_opmcm_bills",
                        use_unicode=True)    # setupDatabase(conn)
    db.set_character_set('utf8')    
    cur = db.cursor() 
    index_url = "http://www.opmcm.gov.np/bills/payment.php"
    response = requests.get(index_url)
    response.encoding = 'utf-8'
    links = getAgencyPageUrl(response.text)
    for link in links:
        agency = link['name'].encode('utf-8')
        print "Reading ", agency #, " page at ", link['href'].encode('utf-8')
        agencyPage = requests.get("http://www.opmcm.gov.np/bills/" + link['href'])
        bills = getAgencyBills(agencyPage.text)
        print "Found bills ", len(bills)
        for bill in bills:
            insertBill(cur, agency, bill)        
        db.commit()
    db.close()        

if __name__ == "__main__":
    main()



