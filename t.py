#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
__author__ = 'Leon'
#coding=utf-8
import urllib2
import re
import MySQLdb

class teamLink(object):
    players = []
    def __init__(self,team,link):
        self.team = team;
        self.link = link

    def setPlayers(self,players):
        self.players = players


class Player(object):
    def __init__(self,link,chName,enName,no,weight,height,birth,detail,money):
        self.link = link
        self.chName = chName
        self.enName = enName
        self.no = no
        self.height = height
        self.weight = weight
        self.birth = birth
        self.detail = detail
        self.money = money




#
def getTeams():
    Items = re.findall('<span class="team_name"><a href=".*?</a></span>',html,re.S)
    for item in Items:
        link = item.replace('<span class="team_name"><a href="','')
        team = re.findall('">.*?</a></span>',link,re.S)[0]
        link = 'http://g.hupu.com/'+link.replace(team,'')
        team = team.replace('">','').replace('</a></span>','')
        teamList.append(teamLink(team,link))

#
def getPlayers(team):
    print '球队 : '+team.team+'   链接 : '+team.link
    players = []
    response = urllib2.urlopen(team.link)
    html = response.read()
    html = html.replace('\n','')
    html = html.replace(' ','')
    html = re.findall('<tableclass="players_table"style="display:block;">.*?</table>',html,re.S)[0]
    ps = re.findall('<tr><tdclass="td_padding">.*?</td></tr>',html,re.S)
    for phtml in ps:
        #print phtml
        plink = phtml.replace('<tr><tdclass="td_padding"><ahref="','')
        plink = replaceByRegular(plink,'','"target="_blank">.*?</td></tr>')
        #print plink
        pChName = replaceByRegular(phtml,'','<tr><tdclass="td_padding"><ahref="'+plink+'.*?'+plink+'">')
        pChName = replaceByRegular(pChName,'','</a></b><p>.*?</td></tr>')
        #print pChName
        pEnName = replaceByRegular(phtml,'','<tr><tdclass="td_padding"><ahref=.*?</a></b><p>\(<b>')
        pEnName = replaceByRegular(pEnName,'','\)</b></p>.*?</td></tr>')
        pEnName = pEnName.replace("'","\\'")
        #print 'write to File  '+pChName+'('+pEnName+')'
        #write2File(pChName+'('+pEnName+')',TEAMFILE)
        tmp = replaceByRegular(phtml,'','<tr><tdclass="td_padding"><ahref=".*?\)</b></p></td>')
        #print tmp
        tmp = replaceByRegular(tmp,'','<tdclass="left">.*?</b></td></tr>')
        arr = re.findall('<td>.*?</td>',tmp,re.S)
        pNo = arr[0].replace("</td>",'')
        pNo = pNo.replace("<td>",'')
        pHeight = arr[2].replace("</td>",'')
        pHeight = pHeight.replace("<td>",'')
        pWeight = arr[3].replace("</td>",'')
        pWeight = pWeight.replace("<td>",'')
        pBirth = arr[4].replace("</td>",'')
        pBirth = pBirth.replace("<td>",'')
        pDetail = replaceByRegular(phtml,'','<tr><tdclass="td_padding"><ahref=".*?\-\d\d</td><tdclass="left">')
        pDetail = replaceByRegular(pDetail,'','</td></tr>')
        pMoney = re.findall('<b>.*?</b>',pDetail,re.S)
        if(len(pMoney) == 0):
            if(pDetail == ''):
                #write2File(pChName+'-------->无资料',PLAYERFILE)
                sql = "insert into players values (null,'%s','%s','%s','%d','%s','%s','%s',null,'%d')"%(pChName,pEnName,team.team,int(pNo),pHeight,pWeight,pBirth,0)
            else:
                # write2File(pChName+'-------->'+pDetail,PLAYERFILE)
                pMoney = re.findall('\d*万美元',pDetail,re.S)
                if(len(pMoney) == 0):
                    sql = "insert into players values (null,'%s','%s','%s','%d','%s','%s','%s','%s','%d')"%(pChName,pEnName,team.team,int(pNo),pHeight,pWeight,pBirth,pDetail,0)
                else:
                    pMoney = pMoney[0].replace('万美元','')
                    #sql = 'insert into players values (null,'+pChName+','+pEnName+','+team.team+','+int(pNo)+','+pHeight+','+pWeight+','+pBirth+',null,'+int(pMoney)+')'
                    sql = "insert into players values (null,'%s','%s','%s','%d','%s','%s','%s',null,'%d')"%(pChName,pEnName,team.team,int(pNo),pHeight,pWeight,pBirth,int(pMoney))

                print pDetail

        else:
            pDetail = pDetail.replace('<br>'+pMoney[0],'')
            pMoney = re.findall('\d*万美元',pMoney[0],re.S)
            pMoney = pMoney[0].replace('万美元','')
            #sql = 'insert into players values (null,'+pChName+','+pEnName+','+team.team+','+int(pNo)+','+pHeight+','+pWeight+','+pBirth+','+pDetail+','+int(pMoney)+')'
            sql = "insert into players values (null,'%s','%s','%s','%d','%s','%s','%s','%s','%d')"%(pChName,pEnName,team.team,int(pNo),pHeight,pWeight,pBirth,pDetail,int(pMoney))
            #write2File(pChName+'-------->今年年薪'+pMoney+"万美元",PLAYERFILE)
        print pChName+ 'SQL : '+sql
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
            print "Warnning : insert failed !  name : "+pChName


def replaceByRegular(str,replaceword,Regular):
    arr = re.findall(Regular,str,re.S)
    if(len(arr) == 1):
        str = str.replace(arr[0],replaceword)
    return str


def write2File(str,filename):
    output = open(filename, 'a')
    output.write(str)
    output.write('\n')
    output.close()

TEAMFILE = "teamData.txt"
PLAYERFILE = "playerData.txt"

conn = MySQLdb.connect(host="localhost",user="root",passwd="root",db="NBA",charset="utf8")
#sql = 'insert into players values (null,'+pChName+','+pEnName+','+team.team+','+int(pNo)+','+pHeight+','+pWeight+','+pBirth+','+pDetail+','+int(pMoney)+')''
sql = ''
cursor = conn.cursor()
response = urllib2.urlopen("http://g.hupu.com/nba/players/")
html = response.read()
teamList = []
getTeams()
for team in teamList:
    write2File('================'+team.team+'================',PLAYERFILE)
    getPlayers(team)

conn.close()