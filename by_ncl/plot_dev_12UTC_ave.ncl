;读取组内的TC所有活动日（包含顺延一天) ERA5 nc资料，
;以UTC12为日界 做日平均 
;计算每日距平 
;选出降雪日距平再做平均，绘图
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"

;  ncl /mnt/f/snow_related/code/by_ncl/plot_dev_12UTC_ave.ncl

begin

; 1 read ERA5
count=0
name1=(/"geopotential","u","v"/)
name2=(/"geo500_1","u500_1","v500_1"/)
data_dir ="/mnt/f/snow_sts_data/ERA5/all/"+name1(count)+"/"+name2(count)+".nc" 

; 1 读数据
data    = addfile(data_dir, "r")
z = short2flt(data->z(:,{500},:,:))
z = z/9.8
; printVarSummary(z)

; ;2 以UTC+12的日平均
time= data->time
time=time+12 ;UTC+12
; date=cd_string(time, "%Y%N%D%H")
; print(date(0:96))
z&time       = time ;UTC+12赋给变量
opt = True
opt@nval_crit = 4  
z_Day_mean = calculate_daily_values(z, "avg", 0, opt)
; printVarSummary(Day_mean)
date_mean=cd_string(z_Day_mean&time, "%Y%N%D")
; print(date)


; ; 3 读取TC活动日 挑出需要的日均值
date_dir_TC ="/mnt/f/snow_sts_data/TC/all_tc_days.txt"  ;1025
datefile_TC = asciiread(date_dir_TC,-1,"string")
YYYYMMDD_TC = str_get_field(datefile_TC(1:),2," ") 
date_ind_TC=new(dimsizes(YYYYMMDD_TC), integer)
do i=0,dimsizes(YYYYMMDD_TC)-1 
    date_ind_TC(i) =str_match_ind(date_mean, YYYYMMDD_TC(i))
end do
; print(date(date_ind))
z_need1=z_Day_mean(date_ind_TC,:,:)


; 4 算距平 1025日 每日距平
  z_RmvTime  = dim_rmvmean_n_Wrap(z_need1,0)
  date_RmvTime=cd_string(z_RmvTime&time, "%Y%N%D")
  ; print(date_RmvTime)


; ; 5 读取降雪时间 挑出需要的日距平
date_dir_snow ="/mnt/f/snow_sts_data/1981-2020/snow_date.txt" ;118
datefile_snow = asciiread(date_dir_snow,-1,"string")
YYYYMMDD_snow = str_get_field(datefile_snow(1:),1," ") 
date_ind_snow=new(dimsizes(YYYYMMDD_snow), integer)
do i=0,dimsizes(YYYYMMDD_snow)-1 
    date_ind_snow(i) =str_match_ind(date_RmvTime, YYYYMMDD_snow(i))
end do
print(date_ind_snow)
; z_need2 = z_RmvTime(date_ind_snow,:,:)
; printVarSummary(z_need2)


end