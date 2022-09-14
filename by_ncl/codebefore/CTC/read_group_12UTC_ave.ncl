;将组内的ERA5 nc资料，以UTC12日界 做日平均 将所需时间数据处理成txt
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"

;  ncl /mnt/f/snow_related/code/by_ncl/CTC/read_group_12UTC_ave.ncl

begin

; 1 read ERA5
count=4
name=(/"geopotential","u","v","u10","v10"/)
pth="snow"
data_dir ="/mnt/f/snow_sts_data/ERA5/"+pth +"_group/"+name(count)+"/" 

; ; 测试单条数据
; data    = addfile(data_dir+"era5.geopotential.19811121.nc", "r")
; z = short2flt(data->z)
; print(z&level)
; printVarSummary(z)

nc_files = systemfunc("ls "+data_dir+"*.nc")
var_f = addfiles(nc_files,"r") 
ListSetType(var_f,"cat")
npts=174
; ;法一  循环读取 法一法二效果相同
;法二  直接读取
; var   = short2flt(var_f[:]->z(:,{500},{10:40},{70:110}))
; var   = short2flt(var_f[:]->u(:,{500},{10:40},{70:110}))
; var   = short2flt(var_f[:]->v(:,{500},{10:40},{70:110}))
; var   = short2flt(var_f[:]->u10(:,{10:40},{70:110}))
var   = short2flt(var_f[:]->v10(:,{10:40},{70:110}))


; ;2 以UTC+12的日平均
time= var_f[:]->time
time=time+12 ;UTC+12
; date=cd_string(time, "%Y%N%D%H")
; ; print(date(48:96))
var&time       = time ;UTC+12赋给变量
opt = True
opt@nval_crit = 24  
Day_mean = calculate_daily_values(var, "avg", 0, opt)
; printVarSummary(Day_mean)
date=cd_string(Day_mean&time, "%Y%N%D")
; print(date)

; 3 读取降雪时间
date_dir ="/mnt/f/snow_sts_data/CTC/snow_date.txt"
datefile = asciiread(date_dir,-1,"string")
YYYYMMDD = str_get_field(datefile(1:),1," ") 
date_ind=new(dimsizes(YYYYMMDD), integer)
do i=0,dimsizes(YYYYMMDD)-1 
    date_ind(i) =str_match_ind(date, YYYYMMDD(i))
end do
; print(date_ind)
var_need=Day_mean(date_ind,:,:)
; printVarSummary(var_need)


; 3 变一维
mlat=dimsizes(var(0,:,0))
mlon=dimsizes(var(0,0,:))
var_rvs=var_need(:,:,:) ;var_rvs=var_need(:,::-1,:) 不对
var_1d= reshape(var_rvs,(/dimsizes(YYYYMMDD),mlat*mlon/))
; 测试
; print(var_need(0,0,0))
; print(var_need(0,0,1))
; print(var_rvs(0,0,0))
; print(var_rvs(0,0,1))
; print(var_1d(0,0))
; print(var_1d(0,1))
; 因为如果纬度本来就是从小到大排列的话，正常变成一维就是从西南向东北的


fname="/mnt/f/snow_sts_data/CTC/"+pth +"/"+name(count)+"_group.txt"
dimx  = dimsizes (var_1d)
nrows = dimx(0)                                  ; ncols = dimx(1)
lines = new (nrows, string)

do i = 0, nrows-1
  lines(i) = str_concat (sprintf ("%8.2f,", var_1d(i,:)))
end do
asciiwrite (fname, lines)

end