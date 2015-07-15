# asha

主要用于数据的分析。源数据文件是已经清洗好的数据文件，每列有固定字段，字段可以为空，分隔符是 '\t' (其实不推荐，因为字段值里面容易出现，仅仅测试)

由于只涉及到渠道一个维度的用户统计，所以清洗的适合 只带渠道即可

awk -F'\t' {'print $8,$28'} 20150610.log|sort -u>20150610_user.data


1、计算当天的活跃

dau=`cat 20150610_user.data|wc -l`
 
2、计算新增
sort 20150610.data history.data history.data|uniq -u > 20150610_new.data
dnu=`cat 20150610_new.data|wc -l `

3、计算留存
sort 20150610_new.data 20150611_new.data > 20150610_1_remain.data
drm=`cat 20150610_1_remain.data |wc -l`
