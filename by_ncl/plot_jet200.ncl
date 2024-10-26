;读取组内的TC所有活动日（包含顺延一天) ERA5 200hPa nc资料，
;以UTC12为日界 做日平均 
;计算每日距平 
;1 选出降雪日距平再做平均，绘图
;2 TC日平均 绘图
;3 改step3  picname 绘图dev

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"

;  ncl /mnt/e/backups/f/snow_related/code/by_ncl/plot_jet200.ncl

begin

typelabel = 1  ;1 2 分别是东南型、偏西型
pic_dir   = "/mnt/e/backups/f/snow_related/pic/atmos_env/REOF/review1/" 

; 1 read ERA5
name1=(/"geo200","u200","v200"/)
count:=0
data_dir0 ="/mnt/e/backups/f/snow_sts_data/ERA5/pick/"+name1(count)+"_6h.nc" 
count:=1
data_dir1 ="/mnt/e/backups/f/snow_sts_data/ERA5/pick/"+name1(count)+"_6h.nc" 
count:=2
data_dir2 ="/mnt/e/backups/f/snow_sts_data/ERA5/pick/"+name1(count)+"_6h.nc" 

; 1 读数据
data0    = addfile(data_dir0, "r")
data1    = addfile(data_dir1, "r")
data2    = addfile(data_dir2, "r")

z = short2flt(data0->z(:,{200},:,:))
u = data1->u(:,{200},:,:)
v = data2->v(:,{200},:,:)

z = z/9.8
; printVarSummary(z)

; ;2 以UTC+12的日平均
time= data0->time
time=time+12 ;UTC+12
; date=cd_string(time, "%Y%N%D%H")
; print(date(0:96))
z&time       = time ;UTC+12赋给变量
u&time       = time ;UTC+12赋给变量
v&time       = time ;UTC+12赋给变量

opt = True
opt@nval_crit = 4  
z_Day_mean = calculate_daily_values(z, "avg", 0, opt)
; printVarSummary(Day_mean)
date_mean=cd_string(z_Day_mean&time, "%Y%N%D")
; print(date)
; u v 同理
u_Day_mean = calculate_daily_values(u, "avg", 0, opt)
v_Day_mean = calculate_daily_values(v, "avg", 0, opt)

; ; 3 读取TC活动日 挑出TC活动日的日均值
date_dir_TC ="/mnt/e/backups/f/snow_sts_data/TC/all_tc_days.txt"  ;1025
datefile_TC = asciiread(date_dir_TC,-1,"string")
YYYYMMDD_TC = str_get_field(datefile_TC(1:),2," ") 
date_ind_TC=new(dimsizes(YYYYMMDD_TC), integer)
do i=0,dimsizes(YYYYMMDD_TC)-1 
	date_ind_TC(i) =str_match_ind(date_mean, YYYYMMDD_TC(i))
end do
; print(date(date_ind))
z_need1=z_Day_mean(date_ind_TC,:,:) ;TC日均值
u_need1=u_Day_mean(date_ind_TC,:,:)
v_need1=v_Day_mean(date_ind_TC,:,:)


; step3 算距平 1025日 每日距平
  z_RmvTime  = dim_rmvmean_n_Wrap(z_need1,0)
  date_RmvTime=cd_string(z_RmvTime&time, "%Y%N%D")
  ; print(date_RmvTime)

  ; ; 读取降雪日 116日 挑出降雪日的日均值 日距平
  date_dir_snow ="/mnt/e/backups/f/snow_sts_data/REOF/spa_index.txt" ;118
  datefile_snow = asciiread(date_dir_snow,-1,"string")
  YYYYMMDD_snow = str_get_field(datefile_snow(1:),1," ") 
  type          = str_get_field(datefile_snow(1:),4," ")
  indexes_type  = ind(type.eq.typelabel)
  YYYYMMDD_type = YYYYMMDD_snow(indexes_type)
  date_ind_snow=new(dimsizes(YYYYMMDD_type), integer)
  do i=0,dimsizes(YYYYMMDD_type)-1 
  date_ind_snow(i) =str_match_ind(date_RmvTime, YYYYMMDD_type(i))
  end do
  print(YYYYMMDD_type)

  ; 挑均值和距平
  z_need2 = z_need1(date_ind_snow,:,:) ;均值
  z_need3 = z_RmvTime(date_ind_snow,:,:) ;距平
    ; z_need1 和 z_RmvTime 时间维相同
  ; printVarSummary(z_need2)
  u_need2 = u_need1(date_ind_snow,:,:) ;降雪日u均值
  v_need2 = v_need1(date_ind_snow,:,:) ;降雪日v均值

  ; 合成
  z_avg=dim_avg_n_Wrap(z_need2, 0) ;降雪日z平均场合成
  u_avg=dim_avg_n_Wrap(u_need2, 0) ;降雪日u平均场合成
  v_avg=dim_avg_n_Wrap(v_need2, 0) ;降雪日v平均场合成
  z_dev=dim_avg_n_Wrap(z_need3, 0) ;降雪日z距平场合成
  V_avg = sqrt(u_avg^2 + v_avg^2)
  ; printVarSummary(V_avg)
  ; print(max(V_avg))
  ; exit
  copy_VarCoords(u_avg, V_avg)


;  绘图
delete([/data0,data1,data2,z,u,v,\
       z_Day_mean,u_Day_mean,v_Day_mean/])


wks = gsn_open_wks("pdf", pic_dir+"snowday_"+"V200_Type"+\
                   tostring(typelabel))
; wks = gsn_open_wks("eps", pic_dir+"TCday_"+"geo200")


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

;--------------等值线--------------

	cnres1 = res
	cnres1@cnFillOn        = False  ;cn means ContourPlot
	cnres1@cnLinesOn       = True   
	;cnres1@cnMonoLineColor= False
	cnres1@cnLineColor     ="blue"
	;cnres1@cnSpanLinePalette = True
	;cnres1@cnLinePalette     = "rainbow"
	cnres1@cnLineLabelsOn     = True  
	cnres1@cnInfoLabelOn      = False ; set false will not set an information label
	cnres1@cnLevelSelectionMode = "ManualLevels" 
	cnres1@cnMinLevelValF      = 11000
	cnres1@cnMaxLevelValF      = 12520
	cnres1@cnLevelSpacingF      = 40
	cnres1@cnLineThicknessF     = 3
	cnres1@cnLineLabelFontHeightF=0.015
	;cnres1@gsnSpreadColorStart = 1
	;cnres1@gsnSpreadColorStart = 17
	;cnres1@gsnSpreadColors     = True ; 6.1.0



; 填色
cnres2                    = res
  cnres2@cnFillOn           = True  ;cn means ContourPlot
  cnres2@cnLinesOn          = False   
  cnres2@cnInfoLabelOn        = False

  cmap  = read_colormap_file("precip3_16lev")
  ; id=ispan(0, 18, 1)
  ; cmap1= cmap(id,:)
  colors=cmap
  cnres2@cnFillPalette       =colors
  ; cnres2@cnFillOpacityF      = 0.50   ; make partially transparent
  cnres2@cnLevelSelectionMode = "ManualLevels" 
  cnres2@cnMinLevelValF      = 30
  cnres2@cnMaxLevelValF      = 55
  cnres2@cnLevelSpacingF      = 5

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
windRes@vcRefMagnitudeF = 15.
windRes@vcRefLengthF    = 0.02
windRes@vcRefAnnoOn = True
windRes@vcRefAnnoFontHeightF =0.015
windRes@vcRefAnnoZone = 1
windRes@vcRefAnnoSide = "Top"
windRes@vcRefAnnoJust = "TopRight"
windRes@vcRefAnnoString1 = "15 m/s"
windRes@vcRefAnnoString2On = False
windRes@vcLineArrowHeadMaxSizeF = 0.01
windRes@vcLineArrowHeadMinSizeF = 0.01
windRes@vcRefAnnoOrthogonalPosF=0
windRes@vcRefAnnoPerimSpaceF=0.1
windRes@vcRefAnnoArrowSpaceF=1

;大于30 换颜色 找出急流轴
windRes@vcMonoLineArrowColor=False
windRes@vcLevelSelectionMode="ExplicitLevels" 
jet = 40; 急流 超过多少 灰色箭头
windRes@vcLevels= jet
windRes@vcLevelColors=(/"black","gray"/)
windRes@lbLabelBarOn        = False

;绘图

map = gsn_csm_map(wks, mpres)
contour = gsn_csm_contour(wks,V_avg, cnres2) 
windPlot = gsn_csm_vector(wks, u_avg , v_avg , windRes)

overlay(map, contour)
overlay(map, windPlot)



;高原轮廓线
  shpfile  ="/mnt/e/backups/f/snow_sts_data/TPshp/DBATP/DBATP_Polygon.shp"
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 6.0           ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shpfile,lnres) 

draw(map)
frame(wks)


end