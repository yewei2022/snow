;使用组内数据 500hPa水汽通量 500hPa风速 
;join或者cat数据后，q u v 需要循环读入数据uv数据读出来才是对的

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"
load "/mnt/h/d/ncl_related/code/shapefile_utils.ncl"

;  ncl /mnt/f/snow_related/code/by_ncl/CTC/plot_vap500_group.ncl

begin

type="1" ;123
pth="snow"
pic_dir ="/mnt/f/snow_related/pic/CTC/500_10m/"+pth +"_group/"


; ; 读数据
data_dir="/mnt/f/snow_sts_data/ERA5/"+pth +"_group/"

; 测试单条数据
; 命令行 输入 查看文件变量信息
; ncl_filedump -c /mnt/f/snow_sts_data/ERA5/snow_group/10u/
; era5.10m_u_component_of_wind.20201128.nc
; data    = addfile(data_dir+"10u/era5.10m_u_component_of_wind.20201128.nc", "r")
; u10 = short2flt(data->u10)
; date=cd_string(u10&time, "%Y%N%D%H")
; print(date)


date_dir ="/mnt/f/snow_sts_data/CTC/"+pth +"/"+pth+"_CTC_group.txt"
datefile = asciiread(date_dir,-1,"string")
YYYYMMDD = str_get_field(datefile(1:),1," ")
label    = str_get_field(datefile(1:),2," ") 
q_files = systemfunc("ls "+data_dir+"q/*.nc")
q_f = addfiles(q_files,"r") 
ListSetType(q_f,"cat")
u_files = systemfunc("ls "+data_dir+"u/*.nc")
u_f     = addfiles(u_files,"r") 
ListSetType(u_f,"cat")
v_files = systemfunc("ls "+data_dir+"v/*.nc")
v_f     = addfiles(v_files,"r") 
ListSetType(v_f,"cat")

; u10_files = systemfunc("ls "+data_dir+"u10/*.nc")
; u10_f     = addfiles(u10_files,"r") 
; ListSetType(u10_f,"cat")
; v10_files = systemfunc("ls "+data_dir+"v10/*.nc")
; v10_f     = addfiles(v10_files,"r") 
; ListSetType(v10_f,"cat")

mlat=241
mlon=281

samps=4176
q500  = new((/samps,mlat,mlon/), float)
u500    = new((/samps,mlat,mlon/), float)
v500    = new((/samps,mlat,mlon/), float)

u10    = new((/samps,mlat,mlon/), float)
v10    = new((/samps,mlat,mlon/), float)

;法一 q u500 v500 循环读取 才正确 读数据时经纬度范围随意 画图时调整显示范围即可
do i =0,samps-1
    q500(i,:,:)= short2flt(q_f[:]->q(i,{500},{0:60},{70:140}))
    u500(i,:,:)  = short2flt(u_f[:]->u(i,{500},{0:60},{70:140}))
    v500(i,:,:)  = short2flt(v_f[:]->v(i,{500},{0:60},{70:140}))
    ; u10(i,:,:)  = short2flt(u10_f[:]->u10(i,{0:60},{70:140}))
    ; v10(i,:,:)  = short2flt(v10_f[:]->v10(i,{0:60},{70:140}))
end do


; ;2 以UTC+12的日平均
time= q_f[:]->time
time=time+12 ;UTC+12
q500!0          = "time"
q500&time = time ;UTC+12赋给变量
u500!0          = "time"
u500&time = time ;UTC+12赋给变量
v500!0          = "time"
v500&time = time ;UTC+12赋给变量
; u10!0          = "time"
; u10&time = time ;UTC+12赋给变量
; v10!0          = "time"
; v10&time = time ;UTC+12赋给变量


opt = True
opt@nval_crit = 24  
q_mean = calculate_daily_values(q500, "avg", 0, opt)
u500_mean = calculate_daily_values(u500, "avg", 0, opt)
v500_mean = calculate_daily_values(v500, "avg", 0, opt)
; u10_mean = calculate_daily_values(u10, "avg", 0, opt)
; v10_mean = calculate_daily_values(v10, "avg", 0, opt)


date=cd_string(q_mean&time, "%Y%N%D")
date_ind=new(dimsizes(YYYYMMDD), integer)
do i=0,dimsizes(YYYYMMDD)-1 
    date_ind(i) =str_match_ind(date, YYYYMMDD(i))
end do

q_day=q_mean(date_ind,:,:)
u500_day=u500_mean(date_ind,:,:)
v500_day=v500_mean(date_ind,:,:)
; u10_day=u10_mean(date_ind,:,:)
; v10_day=v10_mean(date_ind,:,:)

;计算水汽通量
  q_day=q_day*1000 ;单位变成g/kg
  qu500_day= q_day*u500_day/9.8
  qv500_day= q_day*v500_day/9.8
  copy_VarCoords(q_day,qu500_day)
  copy_VarCoords(q_day,qv500_day)

  type_ind=str_match_ind(label, type)

  qu_need  =qu500_day(type_ind,:,:)
  qv_need  =qv500_day(type_ind,:,:)
  qu_need!0 = "time"
  qv_need!0 = "time"
  qu_avg  =dim_avg_n_Wrap(qu_need, 0) ;水汽通量矢量
  qv_avg  =dim_avg_n_Wrap(qv_need, 0)
  mm=sqrt(qu_avg^2+qv_avg^2) ;水汽通量大小
  copy_VarCoords(qu_avg,mm)

; vapdiv=uv2dv_cfd(qu_avg, qv_avg,qu_avg&latitude,qu_avg&longitude, 2)
  ; copy_VarCoords(qu_avg, vapdiv)

;   vapdiv=vapdiv*1.e6
; ; ;mask掉高原以外的vapdiv
;   shp_filename  ="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Polygon.shp" 
;   vapdiv_mask =new(dimsizes(vapdiv),typeof(vapdiv),vapdiv@_FillValue)
;   vapdiv_mask =shapefile_mask_data(vapdiv,shp_filename,True) 

; ; 10m风速
;   u10_need  =u10_day(type_ind,:,:)
;   v10_need  =v10_day(type_ind,:,:) 
;   u10_need!0 = "time"
;   v10_need!0 = "time"
;   u10_avg  =dim_avg_n_Wrap(u10_need, 0) ;10m风速矢量
;   v10_avg  =dim_avg_n_Wrap(v10_need, 0)


; 500hPa风速
  u500_need  =u500_day(type_ind,:,:)
  v500_need  =v500_day(type_ind,:,:) 
  u500_need!0 = "time"
  v500_need!0 = "time"
  u500_avg  =dim_avg_n_Wrap(u500_need, 0) ;500m风速矢量
  v500_avg  =dim_avg_n_Wrap(v500_need, 0)


; ;通量写入二进制文件 有这功夫图早都出来了
;   mm@_FillValue=32700.
;   nlat = dimsizes(mm(:,0))
;   nlon = dimsizes(mm(0,:))
;   z      = new ( (/nlat,nlon/), float,32700.)
;   path = "/mnt/f/snow_sts_data/ERA5/snow_group/tongliang.grd"
;   fbindirwrite(path,z(:,:) )

wks = gsn_open_wks("eps", pic_dir+"tongliang_vap_P"+type)

res = True
res@gsnDraw = False
res@gsnFrame = False
; res@gsnMaximize=True
res@gsnLeftString =""
res@gsnRightString = ""
res@tmYROn=False
res@tmXTOn=False
res@tmBorderThicknessF  =2.5    ; border 6x as thick,图框粗细
res@tmXBMajorThicknessF =2.5
res@tmXBMinorThicknessF =2.5
res@tmYLMajorThicknessF =2.5 
res@tmYLMinorThicknessF =2.5  

; ;坐标轴标签大小
; res@tmEqualizeXYSizes   =True 
; ; 现在一个坐标轴设置好后，
; ;(tmXBLabelFontHeightF,(tmXBMajorLengthF,(tmXBMinorLengthF
; ; 其他坐标轴就不用重复设置了
; res@tmXBLabelFontHeightF = 0.02 ; x轴标签字号

;设置地图
mpres = res
mpres@mpFillOn                = False
mpres@mpMinLatF               = 10.
mpres@mpMaxLatF               = 40.
mpres@mpMinLonF               = 70.
mpres@mpMaxLonF               = 110.
mpres@gsnMajorLatSpacing    =10 
mpres@gsnMinorLatSpacing    =2
mpres@gsnMajorLonSpacing    =10 
mpres@gsnMinorLonSpacing    =2 
mpres@mpDataSetName              = "/mnt/h/d/ChinaMap/Earth..4"
mpres@mpDataBaseVersion          = "MediumRes"
mpres@mpOutlineSpecifiers        = (/"China","China:Provinces"/)


;--------------风矢量图--------------
windRes = res
; windRes@gsnRightString ="P"+type
; windRes@gsnRightStringFontHeightF=0.024
; windRes@gsnRightStringOrthogonalPosF=-1
; windRes@txPerimOn=True
; windRes@txPerimThicknessF=2.5
; windRes@txBackgroundFillColor ="white"

windRes@vcGlyphStyle    = "LineArrow"
windRes@vcLineArrowThicknessF = 2.5
windRes@vcMinDistanceF = 0.03
windRes@vcRefMagnitudeF = 5.
windRes@vcRefLengthF    = 0.02
windRes@vcRefAnnoOn = True
windRes@vcRefAnnoFontHeightF =0.015
windRes@vcRefAnnoZone = 1
windRes@vcRefAnnoSide = "Top"
windRes@vcRefAnnoJust = "TopRight"
windRes@vcRefAnnoString1 = "5m/s"
windRes@vcRefAnnoString2On = False
windRes@vcLineArrowHeadMaxSizeF = 0.01
windRes@vcLineArrowHeadMinSizeF = 0.01


;填色-----------------------------------------
  cnres=res
  cnres@cnFillOn        = True                    ; turn on color
  cnres@cnLinesOn       = False                   ; turn off contour lines
  cnres@cnLineLabelsOn  = False                   ; tuen off line labels
  cnres@cnInfoLabelOn   = False 

  cnres@cnLevelSelectionMode  ="ExplicitLevels" 
  cnres@cnFillPalette       = "perc2_9lev"  ;水汽通量填色
  cnres@cnLevels              =fspan(1, 5, 9)
  cnres@cnFillColors          =(/-1,1,2,3,4,5,6,7,8,9/)

  ; cnres@cnFillPalette       = "BlueWhiteOrangeRed"  ;水汽通量散度填色BlueRed
  ; cnres@cnLevelSelectionMode = "ManualLevels" 
  ; cnres@cnMinLevelValF = -4
  ; cnres@cnMaxLevelValF = 4
  ; cnres@cnLevelSpacingF= 0.5

  cnres@pmLabelBarHeightF     = 0.08
  cnres@lbLabelStride         = 2         ; 两个level只标一个标签
  ; cnres@lbLabelAutoStride   = True            ; let NCL determine label spacing
  cnres@lbBoxLinesOn          = True ; 色标之间分界线
  cnres@lbBoxEndCapStyle      = "TriangleBothEnds"
  cnres@lbLabelFontHeightF    = 0.02 
  cnres@pmLabelBarOrthogonalPosF = 0.1;色标条的位置


;绘图
map = gsn_csm_map(wks, mpres)

plot_wind = gsn_csm_vector(wks, u500_avg, v500_avg, windRes)
plot_cn = gsn_csm_contour(wks, mm, cnres)

overlay(map, plot_cn)
overlay(map, plot_wind)


; 读取并绘制风暴位置
file_tc= asciiread("/mnt/f/snow_sts_data/TC/TC_dot_CTC.txt",-1,"string")
lon_tc   = stringtofloat(str_get_field(file_tc(1:),3," "))
lat_tc   = stringtofloat(str_get_field(file_tc(1:),4," "))
type_tc  = str_get_field(file_tc(1:),6," ")

tc_ind=str_match_ind(type_tc, type)
lon_dot=lon_tc(tc_ind)
lat_dot=lat_tc(tc_ind)

txres               = True                     ; text mods desired
txres@txFontHeightF = 0.01                     ; font smaller. default big
txres@txFontThicknessF=1.2
txres@txFontColor="red"
dum_tc = gsn_add_text(wks,map,"~F37~p",lon_dot,lat_dot,txres) 

;高原轮廓线
  shp_line="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Polygon.shp"  
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 6.0           ; 6x thickness          ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shp_line,lnres)

draw(map)
frame(wks)

end