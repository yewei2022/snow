;将我重新下载的ERA5 nc数据，处理成txt 就网格点数量不一样而已
; snow 118  extrm 64
; !!!时间只取出每日12时
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"

;  ncl /mnt/f/snow_related/code/by_ncl/CTC/read_mydown.ncl

begin

count=2
name=(/"geopotential","u","v"/)
pth="snow"
data_dir ="/mnt/f/snow_sts_data/ERA5/"+pth +"_mydown/"+name(count)+"/" 

; 测试单条数据
; data    = addfile(data_dir+"era5.geopotential.19811210.nc", "r")
; z = short2flt(data->z)
; print(z&level)

nc_files = systemfunc("ls "+data_dir+"*.nc")
var_f = addfiles(nc_files,"r") 
ListSetType(var_f,"join")

npts=118

; ;法一  循环读取 法一法二效果相同
; var  = new((/npts,241,281/), float)
; do i =0,npts-1
;     var(i,:,:)= short2flt(var_f[:]->z(i,12,{500},:,:))
; end do

;法二  直接读取
; var   = short2flt(var_f[:]->z(:,12,{500},{5:45},{65:110}))
; var   = short2flt(var_f[:]->u(:,12,{500},{5:45},{65:110}))
var   = short2flt(var_f[:]->v(:,12,{500},{5:45},{65:110}))


var_rvs=var(:,:,:)
var_1d= reshape(var_rvs,(/npts,161*181/))
; printVarSummary(var_1d)

fname="/mnt/f/snow_sts_data/CTC/"+pth +"/"+name(count)+"_mydown.txt"
dimx  = dimsizes (var_1d)
nrows = dimx(0)                                  ; ncols = dimx(1)
lines = new (nrows, string)

do i = 0, nrows-1
 lines(i) = str_concat (sprintf ("%8.2f,", var_1d(i,:)))
end do
asciiwrite (fname, lines)

end