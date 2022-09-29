;读取组内的TC所有活动日（包含顺延一天) ERA5 500hPa nc资料，
;以UTC12为日界 做日平均 
;计算每日距平 
;1 选出降雪日距平再做平均，绘图
;2 TC日平均 绘图
; 改step3 和4  picname 绘图dev

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"

;  ncl /mnt/f/snow_related/code/by_ncl/plot_VMS_12UTC_ave.ncl

begin

typelabel     = 1 ;1 2
pic_dir  = "/mnt/f/snow_related/pic/atmos_env/REOF/" 

; 1 read ERA5
name1=(/"u200","v200","u850","v850"/)
count:=0
data_dir0 ="/mnt/f/snow_sts_data/ERA5/all/pick/"+name1(count)+"_6h.nc" 
count:=1
data_dir1 ="/mnt/f/snow_sts_data/ERA5/all/pick/"+name1(count)+"_6h.nc" 
count:=2
data_dir2 ="/mnt/f/snow_sts_data/ERA5/all/pick/"+name1(count)+"_6h.nc" 
count:=3
data_dir3 ="/mnt/f/snow_sts_data/ERA5/all/pick/"+name1(count)+"_6h.nc" 

; 1 读数据
data0    = addfile(data_dir0, "r")
data1    = addfile(data_dir1, "r")
data2    = addfile(data_dir2, "r")
data3    = addfile(data_dir3, "r")

u200 = data0->u(:,{200},:,:)
v200 = data1->v(:,{200},:,:)
u850 = data2->u(:,{850},:,:)
v850 = data3->v(:,{850},:,:)


; ;2 以UTC+12的日平均
time= data0->time
time=time+12 ;UTC+12
; date=cd_string(time, "%Y%N%D%H")
; print(date(0:96))
u200&time       = time ;UTC+12赋给变量
v200&time       = time ;UTC+12赋给变量
u850&time       = time ;UTC+12赋给变量
v850&time       = time ;UTC+12赋给变量

opt = True
opt@nval_crit = 4  
u200_Day_mean = calculate_daily_values(u200, "avg", 0, opt)
date_mean=cd_string(u200_Day_mean&time, "%Y%N%D")
u850_Day_mean = calculate_daily_values(u850, "avg", 0, opt)
v200_Day_mean = calculate_daily_values(v200, "avg", 0, opt)
v850_Day_mean = calculate_daily_values(v850, "avg", 0, opt)

; 读取TC活动日 挑出TC活动日的日均值
date_dir_TC ="/mnt/f/snow_sts_data/TC/all_tc_days.txt"  ;1025
datefile_TC = asciiread(date_dir_TC,-1,"string")
YYYYMMDD_TC = str_get_field(datefile_TC(1:),2," ") 
date_ind_TC=new(dimsizes(YYYYMMDD_TC), integer)
do i=0,dimsizes(YYYYMMDD_TC)-1 
	date_ind_TC(i) =str_match_ind(date_mean, YYYYMMDD_TC(i))
end do
;TC各变量日均值
u200_need1=u200_Day_mean(date_ind_TC,:,:) 
u850_need1=u850_Day_mean(date_ind_TC,:,:)
v200_need1=v200_Day_mean(date_ind_TC,:,:)
v850_need1=v850_Day_mean(date_ind_TC,:,:)

u_diff_TC=u200_need1-u850_need1
v_diff_TC=v200_need1-v850_need1
copy_VarCoords(u200_need1, u_diff_TC)
copy_VarCoords(u200_need1, v_diff_TC)

vms_TC=sqrt(u_diff_TC^2+v_diff_TC^2)
; copy_VarCoords_not_n(u_diff_TC, vms_TC,1)
copy_VarCoords(u200_need1, vms_TC)


; ; 3 合成TC日

;   vms_avg=dim_avg_n_Wrap(vms_TC, 0) ;TC日z平均场合成
;   u_avg=dim_avg_n_Wrap(u_diff_TC, 0) ;TC日u平均场合成
;   v_avg=dim_avg_n_Wrap(v_diff_TC, 0) ;TC日v平均场合成


; 4 降雪日

  vmsdev_TC  = dim_rmvmean_n_Wrap(vms_TC,0)
  date_u200_need1=cd_string(u200_need1&time, "%Y%N%D")
  ; print(date_RmvTime)

  ; 读取降雪日 116日 挑出降雪日的日均值 日距平
  date_dir_snow ="/mnt/f/snow_sts_data/REOF/spa_index.txt" ;118
  datefile_snow = asciiread(date_dir_snow,-1,"string")
  YYYYMMDD_snow = str_get_field(datefile_snow(1:),1," ") 
  type          = str_get_field(datefile_snow(1:),4," ")
  indexes_type  = ind(type.eq.typelabel)
  YYYYMMDD_type = YYYYMMDD_snow(indexes_type)
  date_ind_snow=new(dimsizes(YYYYMMDD_type), integer)
  do i=0,dimsizes(YYYYMMDD_type)-1 
  date_ind_snow(i) =str_match_ind(date_u200_need1, YYYYMMDD_type(i))
  end do
  print(YYYYMMDD_type)

  ; 挑均值和距平
  u_diff_snow = u_diff_TC(date_ind_snow,:,:) ;降雪日u均值
  v_diff_snow = v_diff_TC(date_ind_snow,:,:) ;降雪日u均值
  vms_snow = vms_TC(date_ind_snow,:,:) ;降雪日u均值
  vmsdev_snow = vmsdev_TC(date_ind_snow,:,:) ;降雪日u均值


  ; 合成降雪日
  vms_avg=dim_avg_n_Wrap(vms_snow, 0) ;降雪日z平均场合成
  vms_dev=dim_avg_n_Wrap(vmsdev_snow, 0) ;降雪日距平场合成
  u_avg=dim_avg_n_Wrap(u_diff_snow, 0) ;降雪日u平均场合成
  v_avg=dim_avg_n_Wrap(v_diff_snow, 0) ;降雪日v平均场合成


;  绘图
delete([/data0,data1,data2,data3,u200,v200,u850,v850,\
       u200_Day_mean,u850_Day_mean,v200_Day_mean,v850_Day_mean/])

wks = gsn_open_wks("eps", pic_dir+"snowday_"+"VMSdev_Type"+tostring(typelabel))
; wks = gsn_open_wks("eps", pic_dir+"TCday_"+"VMS")


;---Set up some map resources.
  res                       = True
  ; res@gsnMaximize           = True             ; Maximize plot in frame.
  res@gsnDraw               = False            ; Will draw later
  res@gsnFrame              = False            ; Don't advance the frame
  res@gsnLeftString         = ""
  res@gsnRightString        = ""
  res@tmYROn                =False
  res@tmXTOn                =False
  res@gsnAddCyclic          =False
  res@tmEqualizeXYSizes     =True
  ; res@tmXBLabelFontHeightF  =0.02

  mpres                       =res
  mpres@mpMinLatF             = 10.
  mpres@mpMaxLatF             = 40.
  mpres@mpMinLonF             = 70
  mpres@mpMaxLonF             = 110
  mpres@gsnMajorLonSpacing    =10. 
  mpres@gsnMinorLonSpacing    =5.    
  mpres@gsnMajorLatSpacing    =10. 
  mpres@gsnMinorLatSpacing    =5

  mpres@mpFillOn=False

  mpres@mpDataBaseVersion       = "MediumRes"
  mpres@mpDataSetName           =  "/mnt/d/ChinaMap/Earth..4"
  mpres@mpOutlineSpecifiers     = (/"China:states"/)


; 填色
cnres2                    = res
  cnres2@cnFillOn           = True  ;cn means ContourPlot
  cnres2@cnLinesOn          = False   
  cnres2@cnInfoLabelOn        = False

  ; ; 试一下取值范围
  ; cmap  = read_colormap_file("BlAqGrWh2YeOrReVi22")
  ; id=ispan(2, 18, 1)
  ; cmap1= cmap(id,:)
  ; colors=cmap1
  ; cnres2@cnFillPalette       =colors
  ; cnres2@cnLevelSelectionMode = "ManualLevels" 

; ; 均值填色
;   cnres2@cnFillPalette        = "perc2_9lev"
;   cnres2@cnLevelSelectionMode = "ManualLevels" 
;   cnres2@cnMinLevelValF       =12
;   cnres2@cnMaxLevelValF       =52
;   cnres2@cnLevelSpacingF       =4

; 距平填色
  cnres2@cnFillPalette        = "MPL_coolwarm"
  cnres2@cnLevelSelectionMode = "ManualLevels" 
  cnres2@cnMinLevelValF       =-16
  cnres2@cnMaxLevelValF       =16
  cnres2@cnLevelSpacingF       =4


  cnres2@lbLabelFontHeightF  = 0.02
  cnres2@lbBoxLinesOn        = True ; Label bar
  ; cnres2@lbLabelStride =2 ;每两个一个标签
  ; cnres2@lbLabelAutoStride    = True               ; let NCL determine label spacing
  ; cnres2@lbOrientation        = "Vertical"         ; vertical label bar
  ; cnres2@pmLabelBarWidthF     = 0.05    
  cnres2@pmLabelBarHeightF    = 0.1
  cnres2@pmLabelBarOrthogonalPosF  = 0.1 ;色标离图的距离
  cnres2@lbBoxEndCapStyle = "TriangleBothEnds"


;--------------矢量图--------------

windRes = res
;windRes@vcGlyphStyle            = "FillArrow"   ; turn on curly vectors
windRes@vcGlyphStyle    = "LineArrow"
windRes@vcLineArrowThicknessF = 3
windRes@vcMinDistanceF = 0.04
windRes@vcRefMagnitudeF = 10.
windRes@vcRefLengthF    = 0.02
windRes@vcRefAnnoOn = True
windRes@vcRefAnnoFontHeightF =0.015
windRes@vcRefAnnoZone = 1
windRes@vcRefAnnoSide = "Top"
windRes@vcRefAnnoJust = "TopRight"
windRes@vcRefAnnoString1 = "10 m/s"
windRes@vcRefAnnoString2On = False
windRes@vcLineArrowHeadMaxSizeF = 0.01
windRes@vcLineArrowHeadMinSizeF = 0.01
windRes@vcRefAnnoOrthogonalPosF=0
windRes@vcRefAnnoPerimSpaceF=0.1
windRes@vcRefAnnoArrowSpaceF=1


;绘图

map = gsn_csm_map(wks, mpres)
; contour_avg = gsn_csm_contour(wks,vms_avg, cnres2)
windPlot = gsn_csm_vector(wks, u_avg , v_avg , windRes)

contour_dev = gsn_csm_contour(wks,vms_dev, cnres2)
overlay(map, contour_dev)

; overlay(map, contour_avg)
overlay(map, windPlot)


; ; 读取并绘制风暴位置
; file_tc= asciiread("/mnt/f/snow_sts_data/TC/TC_dot_REOF.txt",-1,"string")
; lon_tc   = stringtofloat(str_get_field(file_tc(1:),3," "))
; lat_tc   = stringtofloat(str_get_field(file_tc(1:),4," "))
; type_tc  = str_get_field(file_tc(1:),7," ")

; tc_ind=str_match_ind(type_tc, tostring(typelabel))
; lon_dot=lon_tc(tc_ind)
; lat_dot=lat_tc(tc_ind)

; txres               = True                     ; text mods desired
; txres@txFontHeightF = 0.01                     ; font smaller. default big
; txres@txFontThicknessF=1.2
; txres@txFontColor="red"
; dum_tc = gsn_add_text(wks,map,"~F37~p",lon_dot,lat_dot,txres) 

;高原轮廓线
  shpfile  ="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Polygon.shp"
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 6.0           ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shpfile,lnres) 

draw(map)
frame(wks)


end