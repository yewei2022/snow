;使用组内数据 500hPa 相当位温
;join或者cat数据后，q u v 需要循环读入数据uv数据读出来才是对的

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"
load "/mnt/h/d/ncl_related/code/shapefile_utils.ncl"

;  ncl /mnt/f/snow_related/code/by_ncl/CTC/plot_hgt200_group.ncl

begin

type="3" ;123
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
hgt_files = systemfunc("ls "+data_dir+"geopotential/*.nc")
hgt_f = addfiles(hgt_files,"r") 
ListSetType(hgt_f,"cat")
u_files = systemfunc("ls "+data_dir+"u/*.nc")
u_f     = addfiles(u_files,"r") 
ListSetType(u_f,"cat")
v_files = systemfunc("ls "+data_dir+"v/*.nc")
v_f     = addfiles(v_files,"r") 
ListSetType(v_f,"cat")

mlat=241
mlon=281

samps=4176
hgt  = new((/samps,mlat,mlon/), float)
u_wind    = new((/samps,mlat,mlon/), float)
v_wind    = new((/samps,mlat,mlon/), float)


;法一 q u_wind v_wind 循环读取 才正确 读数据时经纬度范围随意 画图时调整显示范围即可
do i =0,samps-1
    hgt(i,:,:)= short2flt(hgt_f[:]->z(i,{200},{0:60},{70:140}))
    u_wind(i,:,:)  = short2flt(u_f[:]->u(i,{200},{0:60},{70:140}))
    v_wind(i,:,:)  = short2flt(v_f[:]->v(i,{200},{0:60},{70:140}))
end do


; ;2 以UTC+12的日平均
time= hgt_f[:]->time
time=time+12 ;UTC+12
hgt!0          = "time"
hgt&time = time ;UTC+12赋给变量
u_wind!0          = "time"
u_wind&time = time ;UTC+12赋给变量
v_wind!0          = "time"
v_wind&time = time ;UTC+12赋给变量


opt = True
opt@nval_crit = 24  
hgt_mean = calculate_daily_values(hgt, "avg", 0, opt)
u_wind_mean = calculate_daily_values(u_wind, "avg", 0, opt)
v_wind_mean = calculate_daily_values(v_wind, "avg", 0, opt)

date=cd_string(hgt_mean&time, "%Y%N%D")
date_ind=new(dimsizes(YYYYMMDD), integer)
do i=0,dimsizes(YYYYMMDD)-1 
    date_ind(i) =str_match_ind(date, YYYYMMDD(i))
end do

hgt_day=hgt_mean(date_ind,:,:)
u_wind_day=u_wind_mean(date_ind,:,:)
v_wind_day=v_wind_mean(date_ind,:,:)

;挑出符合type的数据 包含位势 风速
  type_ind=str_match_ind(label, type)
  hgt_need  =hgt_day(type_ind,:,:)
  hgt_need!0 = "time"
  hgt_avg  =dim_avg_n_Wrap(hgt_need, 0) ;500m风速矢量
  hgt_avg=hgt_avg/9.8
  ; 200hPa风速
  u_wind_need  =u_wind_day(type_ind,:,:)
  v_wind_need  =v_wind_day(type_ind,:,:) 
  u_wind_need!0 = "time"
  v_wind_need!0 = "time"
  u_wind_avg  =dim_avg_n_Wrap(u_wind_need, 0) ;500m风速矢量
  v_wind_avg  =dim_avg_n_Wrap(v_wind_need, 0)

  ;计算散度
  div = uv2dv_cfd(u_wind_avg,v_wind_avg,u_wind_avg&latitude,u_wind_avg&longitude, 2)  ;中央差分计算散度
  copy_VarCoords(u_wind_avg, div)
  div = div*1.e5
; ; ;mask掉高原以外的div
  shp_filename  ="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Polygon.shp" 
  div_mask =new(dimsizes(div),typeof(div),div@_FillValue)
  div_mask =shapefile_mask_data(div,shp_filename,True) 
  


wks = gsn_open_wks("eps", pic_dir+"hgt200_P"+type)

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
  windRes@vcRefMagnitudeF = 15.
  windRes@vcRefLengthF    = 0.02
  windRes@vcRefAnnoOn = True
  windRes@vcRefAnnoFontHeightF =0.015
  windRes@vcRefAnnoZone = 1
  windRes@vcRefAnnoSide = "Top"
  windRes@vcRefAnnoJust = "TopRight"
  windRes@vcRefAnnoString1 = "15m/s"
  windRes@vcRefAnnoString2On = False
  windRes@vcLineArrowHeadMaxSizeF = 0.01
  windRes@vcLineArrowHeadMinSizeF = 0.01


;填色-----------------------------------------
  cnres=res
  cnres@cnFillOn        = True                    ; turn on color
  cnres@cnLinesOn       = False                   ; turn off contour lines
  cnres@cnLineLabelsOn  = False                   ; tuen off line labels
  cnres@cnInfoLabelOn   = False 

  ; cnres@cnFillPalette       = "WhiteBlueGreenYellowRed"  ;散度填色BlueRed
  ; cnres@cnLevelSelectionMode = "ManualLevels" 
  ; cnres@cnMinLevelValF = 0
  ; cnres@cnMaxLevelValF = 1.6
  ; ; cnres@cnLevelSpacingF= 0.2

    ; ;填色
  cnres@cnFillPalette       = "wgne15"  
  cnres@cnLevelSelectionMode  ="ExplicitLevels" 
  cnres@cnLevels              = fspan(0, 1.6, 5)
  cnres@cnFillColors          =(/-1,3,6,10,12,13/)
  ; cnres@cnFillOpacityF      = 0.80                  ; make partially transparent


  cnres@pmLabelBarHeightF     = 0.08
  cnres@lbLabelStride         = 2         ; 两个level只标一个标签
  ; cnres@lbLabelAutoStride   = True            ; let NCL determine label spacing
  cnres@lbBoxLinesOn          = True ; 色标之间分界线
  cnres@lbBoxEndCapStyle      = "TriangleBothEnds"
  cnres@lbLabelFontHeightF    = 0.02 
  cnres@pmLabelBarOrthogonalPosF = 0.1;色标条的位置

;--------------叠加高度场--------------
  hgtRes = res
  hgtRes@cnFillOn  = False  ;cn means ContourPlot
  hgtRes@cnLinesOn = True   
  ;hgtRes@cnMonoLineColor = False
  hgtRes@cnLineColor="blue"
  hgtRes@cnLineLabelsOn = True  
  hgtRes@cnLineLabelFontHeightF=0.015
  hgtRes@cnInfoLabelOn  = False ; set false will not set an information label
  hgtRes@cnLineThicknessF = 3
  hgtRes@cnLevelSelectionMode = "ManualLevels" 
  hgtRes@cnMinLevelValF = 12440
  hgtRes@cnMaxLevelValF = 12500
  hgtRes@cnLevelSpacingF  = 20
  hgtRes@cnLineLabelInterval=1
  hgtRes@cnLineLabelDensityF=0.5
  ; hgtRes@ExplicitLineLabelsOn=true
  ; cnLineLabelStrings 


;绘图
map = gsn_csm_map(wks, mpres)

plot_wind = gsn_csm_vector(wks, u_wind_avg, v_wind_avg, windRes)
plot_cn = gsn_csm_contour(wks, div_mask, cnres)
plot_hgt = gsn_csm_contour(wks,hgt_avg, hgtRes)


overlay(map, plot_cn)
overlay(map, plot_wind)
overlay(map, plot_hgt)



;高原轮廓线
  shp_line="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Polygon.shp"  
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 6.0           ; 6x thickness          ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shp_line,lnres)

draw(map)
frame(wks)

end