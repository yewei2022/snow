;读取组内的TC所有活动日（包含顺延一天) ERA5 500hPa nc资料，
;以UTC12为日界 做日平均 
;计算每日水汽通量和散度 
;1 选出降雪日平均，绘图
;2 TC日平均 绘图
; 通量 通量散度 平均 距平 都可画
; 改step3 和4  picname 

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"

;  ncl /mnt/f/snow_related/code/by_ncl/plot_500vap_12UTC_ave.ncl

begin

typelabel     = 2 ;1 2

pic_dir  = "/mnt/f/snow_related/pic/atmos_env/REOF/" 

; 1 read ERA5
name1=(/"q500","u500","v500"/)
count:=0
data_dir0 ="/mnt/f/snow_sts_data/ERA5/all/pick/"+name1(count)+"_6h.nc" 
count:=1
data_dir1 ="/mnt/f/snow_sts_data/ERA5/all/pick/"+name1(count)+"_6h.nc" 
count:=2
data_dir2 ="/mnt/f/snow_sts_data/ERA5/all/pick/"+name1(count)+"_6h.nc" 

; 1 读数据
data0    = addfile(data_dir0, "r")
data1    = addfile(data_dir1, "r")
data2    = addfile(data_dir2, "r")

q = data0->q(:,{500},:,:)
u = data1->u(:,{500},:,:)
v = data2->v(:,{500},:,:)

; ;2 以UTC+12的日平均
time= data0->time
time=time+12 ;UTC+12
; date=cd_string(time, "%Y%N%D%H")
; print(date(0:96))
q&time       = time ;UTC+12赋给变量
u&time       = time ;UTC+12赋给变量
v&time       = time ;UTC+12赋给变量

opt = True
opt@nval_crit = 4  
q_Day_mean = calculate_daily_values(q, "avg", 0, opt)
; printVarSummary(Day_mean)
date_mean=cd_string(q_Day_mean&time, "%Y%N%D")
; print(date)
; u v 同理
u_Day_mean = calculate_daily_values(u, "avg", 0, opt)
v_Day_mean = calculate_daily_values(v, "avg", 0, opt)

; ; 3 读取TC活动日 挑出TC活动日的日均值
date_dir_TC ="/mnt/f/snow_sts_data/TC/all_tc_days.txt"  ;1025
datefile_TC = asciiread(date_dir_TC,-1,"string")
YYYYMMDD_TC = str_get_field(datefile_TC(1:),2," ") 
date_ind_TC=new(dimsizes(YYYYMMDD_TC), integer)
do i=0,dimsizes(YYYYMMDD_TC)-1 
	date_ind_TC(i) =str_match_ind(date_mean, YYYYMMDD_TC(i))
end do
; print(date(date_ind))
q_need1=q_Day_mean(date_ind_TC,:,:) ;TC日均值
u_need1=u_Day_mean(date_ind_TC,:,:)
v_need1=v_Day_mean(date_ind_TC,:,:)

; 算TC活动日水汽通量和散度
;计算水汽通量
q_need1=q_need1*1000 ;单位变成g/kg
qu_need1= q_need1*u_need1/9.8
qv_need1= q_need1*v_need1/9.8
copy_VarCoords(q_need1,qu_need1)
copy_VarCoords(q_need1,qv_need1)
flux=sqrt(qu_need1^2+qv_need1^2) ;水汽通量 单位g/(s*hPa*cm)
copy_VarCoords(q_need1,flux)

;算散度
div=uv2dv_cfd(qu_need1, qv_need1,qu_need1&latitude,qu_need1&longitude, 2)
copy_VarCoords(qu_need1, div)
div=div*1.e6

; ; 水汽通量距平
; fluxdev  = dim_rmvmean_n_Wrap(flux,0)

; ; step4 合成TC日
; qu_avg=dim_avg_n_Wrap(qu_need1, 0) ;TC日u平均场合成
; qv_avg=dim_avg_n_Wrap(qv_need1, 0) ;TC日v平均场合成
; div_avg=dim_avg_n_Wrap(div, 0) ;TC日div平均场合成
; ; flux_avg=dim_avg_n_Wrap(flux, 0) ;TC日flux平均场合成



; ; step5 读取降雪日 116日 挑出降雪日的日均值和距平
  date_q_need1=cd_string(q_need1&time, "%Y%N%D")
  date_dir_snow ="/mnt/f/snow_sts_data/REOF/spa_index.txt" ;118
  datefile_snow = asciiread(date_dir_snow,-1,"string")
  YYYYMMDD_snow = str_get_field(datefile_snow(1:),1," ") 
  type          = str_get_field(datefile_snow(1:),4," ")
  indexes_type  = ind(type.eq.typelabel)
  YYYYMMDD_type = YYYYMMDD_snow(indexes_type)
  date_ind_snow=new(dimsizes(YYYYMMDD_type), integer)
  do i=0,dimsizes(YYYYMMDD_type)-1 
  date_ind_snow(i) =str_match_ind(date_q_need1, YYYYMMDD_type(i))
  end do
  print(YYYYMMDD_type)

  ; 挑降雪日日均值 距平
  qu_need2 = qu_need1(date_ind_snow,:,:) ;降雪日qu日值
  qv_need2 = qv_need1(date_ind_snow,:,:) ;降雪日qv日值
  div_need  = div(date_ind_snow,:,:) ;降雪日div日值
  flux_need = flux(date_ind_snow,:,:) ;降雪日flux日值
  ; fluxdev_need = fluxdev(date_ind_snow,:,:) ;降雪日flux距平

  ; 合成降雪日
  qu_avg=dim_avg_n_Wrap(qu_need2, 0) ;降雪日u平均场合成
  qv_avg=dim_avg_n_Wrap(qv_need2, 0) ;降雪日v平均场合成
  div_avg=dim_avg_n_Wrap(div_need, 0) ;降雪日div平均场合成
  flux_avg =dim_avg_n_Wrap(flux_need, 0) ;降雪日flux平均场合成
  ; fluxdev_avg=dim_avg_n_Wrap(fluxdev_need, 0) ;降雪日flux距平场合成


;  绘图
delete([/data0,data1,data2,q,u,v,\
       q_Day_mean,u_Day_mean,v_Day_mean/])

wks = gsn_open_wks("eps", pic_dir+"snowday"+"_fluxdiv500_Type"+tostring(typelabel))
; wks = gsn_open_wks("eps", pic_dir+"TCday_"+"fluxdiv500")



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

  cnres=res
  cnres@cnFillOn        = True                    ; turn on color
  cnres@cnLinesOn       = False                   ; turn off contour lines
  cnres@cnLineLabelsOn  = False                   ; tuen off line labels
  cnres@cnInfoLabelOn   = False 

  ; ;水汽通量填色
  ; cnres@cnLevelSelectionMode  ="ExplicitLevels" 
  ; cnres@cnFillPalette       = "perc2_9lev"  
  ; cnres@cnLevels              =fspan(1, 5, 9)
  ; cnres@cnFillColors          =(/-1,1,2,3,4,5,6,7,8,9/)

  ; ; 水汽通量距平填色
  ; cnres@cnFillPalette        = "perc2_9lev"
  ; cnres@cnLevelSelectionMode = "ExplicitLevels"  
  ; cnres@cnLevels             = fspan(0, 2, 6)
  ; cnres@cnFillColors         = (/-1,2,3,4,5,6,7/)

  ; 水汽通量散度填色BlueRed
  cnres@cnFillPalette       = "MPL_coolwarm"  
  cnres@cnLevelSelectionMode = "ManualLevels" 
  cnres@cnMinLevelValF = -10
  cnres@cnMaxLevelValF = 10
  cnres@cnLevelSpacingF= 2

  cnres@pmLabelBarHeightF     = 0.08
  cnres@lbLabelStride         = 1        ; 两个level只标一个标签
  ; cnres@lbLabelAutoStride   = True            ; let NCL determine label spacing
  cnres@lbBoxLinesOn          = True ; 色标之间分界线
  cnres@lbBoxEndCapStyle      = "TriangleBothEnds"
  cnres@lbLabelFontHeightF    = 0.02
  cnres@pmLabelBarOrthogonalPosF = 0.12;色标条的位置


;--------------矢量图--------------
  windRes = res
  ;windRes@vcGlyphStyle            = "FillArrow"   ; turn on curly vectors
  windRes@vcGlyphStyle    = "LineArrow"
  windRes@vcLineArrowThicknessF = 3
  windRes@vcMinDistanceF = 0.04
  windRes@vcRefMagnitudeF = 2
  windRes@vcRefLengthF    = 0.02
  windRes@vcRefAnnoOn = True
  windRes@vcRefAnnoFontHeightF =0.015
  windRes@vcRefAnnoZone = 1
  windRes@vcRefAnnoSide = "Top"
  windRes@vcRefAnnoJust = "TopRight"
  windRes@vcRefAnnoString1 = "2"
  windRes@vcRefAnnoString2On = False
  windRes@vcLineArrowHeadMaxSizeF = 0.01
  windRes@vcLineArrowHeadMinSizeF = 0.01
  windRes@vcRefAnnoOrthogonalPosF=0
  windRes@vcRefAnnoPerimSpaceF=0.1
  windRes@vcRefAnnoArrowSpaceF=1
  windRes@vcMonoLineArrowColor=False
  windRes@lbLabelBarOn        = False
  ;大于2 换颜色
  windRes@vcLevelSelectionMode="ExplicitLevels" 
  windRes@vcLevels=(/2/)
  windRes@vcLevelColors=(/"black","red"/)
  ; windRes@vcRefAnnoArrowUseVecColor=False
  ; windRes@vcRefAnnoArrowLineColor="red"


;绘图

map = gsn_csm_map(wks, mpres)
windPlot = gsn_csm_vector(wks, qu_avg , qv_avg , windRes)

contour_avg = gsn_csm_contour(wks,div_avg, cnres)
overlay(map, contour_avg)

; contour_dev = gsn_csm_contour(wks,fluxdev_avg, cnres)
; overlay(map, contour_dev)

overlay(map, windPlot) ;箭头后叠

;高原轮廓线
  shpfile  ="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Polygon.shp"
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 6.0           ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shpfile,lnres) 

draw(map)
frame(wks)


end