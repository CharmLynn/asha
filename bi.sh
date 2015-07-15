#! /bin/bash

if [ ! -n "$1" ] ;then
    dateday=`date -d "yesterday" +%Y%m%d`
    date2day=`date -d "2 days ago" +%Y%m%d`
else
    dateday=$1
fi

# clean original log file 
echo $dateday
echo $date2day
awk -F'\t' '{print $28}' ${dateday}".log"|sort -u >${dateday}"_user.data"

sort ${dateday}"_user.data" history_user.data history_user.data |uniq -u > ${dateday}"_new.data"
#sort ${date2day}"_new.data" ${dateday}"_user.data"|uniq -d > ${date2day}"_remian.data"

#计算新增和活跃
uv=`cat ${dateday}"_user.data"|wc -l`
nv=`cat ${dateday}"_new.data"|wc -l`
mysql -uasha -pasha -Dbi -e "insert into day_result(dateday,uv,nv) values('$dateday','$uv')"

#计算1~7日的留存和睡眠用户
for i in `seq 2 8`;do
    dateoffset=`date -d "$i days ago" +%%Y%m%d`
    j=$i-1
    sort ${dateoffset}"_user.data" ${dateday}"_user.data" > ${dateoffset}"_"${j}"_remian.data"
    #"nr_"${dateoffset}"_"${j}=`cat ${dateoffset}"_"${j}"_remian.data|wc -l`
    remianvalue=`cat ${dateoffset}"_"${j}"_remian.data|wc -l`
    mysql -uasha -pasha -Dbi -e "update day_remain set $j'_remain'='$remianvalue' where dateday='$dateoffset'"
    if [i eq 2]
        sort ${dateoffset}"_user.data" ${dateday}"_user.data" ${dateday}"_user.data" > ${datesleep}"_sleep.data"
    else:
        sort ${datesleep}"_sleep.data" ${dateday}"_user.data" ${dateday}"_user.data" > ${datesleep}"_sleep.data"
    fi
    sleepvalue=`cat ${datesleep}"_sleep.data|wc -l`
    mysql -uasha -pasha -Dbi -e "insert into day_sleep(dateday,sleepvalue,checkdate) values('$dateday','$sleepvalue','$dateoffset')"
done

#计算8~30日的睡眠用户
for i in `seq 9 31`;do
    datesleep=`date -d "$i days ago" +%Y%m%d`
    sort ${datesleep}"_sleep.data" ${dateday}"_user.data" ${dateday}"_user.data" > ${datesleep}"_sleep.data"
done

