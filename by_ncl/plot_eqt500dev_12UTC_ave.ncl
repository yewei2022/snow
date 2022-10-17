; 日历转换时 time的type 可以是double 也可以是integer 但不能是int64
; python 和ncl 处理 结果相同 用python处理过的 画图快些
; step 3 4 和图片名同时换
;  ncl /mnt/f/snow_related/code/by_ncl/plot_eqt500dev_12UTC_ave.ncl

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"


begin


typelabel=2
pic_dir  = "/mnt/f/snow_related/pic/atmos_env/REOF/" 

; ===================一  用python处理过的的TC日均值===============================
data_dir0 ="/mnt/f/snow_sts_data/ERA5/all/pick/rh_tmp500.nc" 
data0    = addfile(data_dir0, "r")

rh = data0->rh
tmp  = data0->tmp
level  = data0->level

time0  = data0->time
time1=new(1025, integer)
do i =0,1024
  time1(i)=tointeger(time0(i))
end do
copy_VarMeta(time0, time1) ;属性复制 比如units calendar的

rh@_FillValue = 32700
tmp@_FillValue = 32700
level@_FillValue = 32700
level=level*100
level@units="Pa"

; printVarSummary(rh)
; printVarSummary(level)
; print(max(rh))
; exit

; ; ;计算相当位温-----------------------------------
  eqt_need= pot_temp_equiv(level,tmp, rh, 1, "rh")  ;Pa K %
  copy_VarCoords(tmp, eqt_need)
  eqt_need1=eqt_need(:,{500},:,:)
  date_TC=cd_string(time1, "%Y%N%D")
  ; print(date_TC)

; ================================================================



; ; =============二  用ncl处理TC日均值=========================================
; ; 1 read ERA5
; name1=(/"rh500","tmp500"/)
; count:=0
; data_dir0 ="/mnt/f/snow_sts_data/ERA5/all/pick/"+name1(count)+"_6h.nc" 
; count:=1
; data_dir1 ="/mnt/f/snow_sts_data/ERA5/all/pick/"+name1(count)+"_6h.nc" 


; ; 1 读数据
; data0    = addfile(data_dir0, "r")
; data1    = addfile(data_dir1, "r")

; rh = data0->r
; tmp = data1->t
; level= data0&level
; level=level*100
; level@units="Pa"

; ; ;2 以UTC+12的日平均
; time= data0->time
; time=time+12 ;UTC+12
; ; date=cd_string(time, "%Y%N%D%H")
; ; print(date(0:96))
; rh&time       = time ;UTC+12赋给变量
; tmp&time       = time ;UTC+12赋给变量
; opt = True
; opt@nval_crit = 4  
; rh_Day_mean = calculate_daily_values(rh, "avg", 0, opt)
; ; printVarSummary(Day_mean)
; date_mean=cd_string(rh_Day_mean&time, "%Y%N%D")
; ; print(date)
; ;  同理
; tmp_Day_mean = calculate_daily_values(tmp, "avg", 0, opt)

; ; 读取TC活动日 挑出TC活动日的日均值
; date_dir_TC ="/mnt/f/snow_sts_data/TC/all_tc_days.txt"  ;1025
; datefile_TC = asciiread(date_dir_TC,-1,"string")
; YYYYMMDD_TC = str_get_field(datefile_TC(1:),2," ") 
; date_ind_TC=new(dimsizes(YYYYMMDD_TC), integer)
; do i=0,dimsizes(YYYYMMDD_TC)-1 
;   date_ind_TC(i) =str_match_ind(date_mean, YYYYMMDD_TC(i))
; end do
; ; print(date_mean(date_ind_TC))
; ; exit
; ; 挑出TC活动日的日均值
; rh_need1=rh_Day_mean(date_ind_TC,:,:,:) ;TC日均值
; tmp_need1=tmp_Day_mean(date_ind_TC,:,:,:)

; eqt_need= pot_temp_equiv(level,tmp_need1, rh_need1, 1, "rh") ;Pa K %
; copy_VarCoords(tmp_need1, eqt_need)
; eqt_need1=eqt_need(:,0,:,:)

; date_TC=cd_string(eqt_need1&time, "%Y%N%D")
; ; ==========================================================



; step 3 合成TC日
   eqt_avg=dim_avg_n_Wrap(eqt_need1, 0) ;TC日z平均场合成

; step 4 降雪日距平 1025日 每日距平
;   eqt_RmvTime  = dim_rmvmean_n_Wrap(eqt_need1,0)

;   ; 读取降雪日 116日 挑出降雪日的日均值 日距平
;   date_dir_snow ="/mnt/f/snow_sts_data/REOF/spa_index.txt" ;75
;   datefile_snow = asciiread(date_dir_snow,-1,"string")
;   YYYYMMDD_snow = str_get_field(datefile_snow(1:),1," ") 
;   type          = str_get_field(datefile_snow(1:),4," ")
;   indexes_type  = ind(type.eq.typelabel)
;   YYYYMMDD_type = YYYYMMDD_snow(indexes_type)
;   date_ind_snow=new(dimsizes(YYYYMMDD_type), integer)
;   do i=0,dimsizes(YYYYMMDD_type)-1 
;   date_ind_snow(i) =str_match_ind(date_TC, YYYYMMDD_type(i))
;   end do
;   ; print(YYYYMMDD_type)

;   ; 挑降雪日均值和距平
;   eqt_need2 = eqt_need1(date_ind_snow,:,:) ;均值
;   eqt_need3 = eqt_RmvTime(date_ind_snow,:,:) ;距平

;   ; 合成降雪日
;   eqt_avg=dim_avg_n_Wrap(eqt_need2, 0) ;降雪日z平均场合成
;   eqt_dev=dim_avg_n_Wrap(eqt_need3, 0) ;降雪日z距平场合成


;-------------------------------------------------------------------------------------------
; wks = gsn_open_wks("eps", pic_dir+"snowday_"+"eqt500_Type"+tostring(typelabel))
wks = gsn_open_wks("eps", pic_dir+"TCday_"+"eqt500")


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




  eqtres=res
  eqtres@cnFillOn = False  ;cn means ContourPlot
  eqtres@cnLinesOn = True 
  eqtres@cnLineColor="black"
  eqtres@cnLineLabelsOn=True
  eqtres@cnLineLabelFontHeightF=0.016
  eqtres@cnLineLabelBackgroundColor="white" ;-1是透明
  ;res@cnMonoLineColor = False
  ; eqtres@cnLabelMasking = True ;???打开就看不到label了
  ; eqtres@cnLineLabelPlacementMode = "Constant"
  eqtres@cnLineDashSegLenF    = 0.3
  eqtres@cnInfoLabelOn = False ; set false will not set an information label
  eqtres@cnLineThicknessF = 3
  eqtres@cnLevelSelectionMode = "ManualLevels" 
  eqtres@cnLevelSpacingF = 2  
  eqtres@cnLineLabelInterval=2 
  eqtres@cnLineLabelFormat ="3.3f"

  ; 距平填色 BlueRed
  cnres=res
  cnres@cnFillOn        = True                    ; turn on color
  cnres@cnLinesOn       = False                   ; turn off contour lines
  cnres@cnLineLabelsOn  = False                   ; tuen off line labels
  cnres@cnInfoLabelOn   = False
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


;----------------绘图----------------------
map = gsn_csm_map(wks, mpres)
contour_avg = gsn_csm_contour(wks,eqt_avg, eqtres)


; contour_dev = gsn_csm_contour(wks,eqt_dev, cnres)
; overlay(map, contour_dev)


overlay(map, contour_avg)


;高原轮廓线
  shpfile  ="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Polygon.shp"
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 6.0           ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shpfile,lnres) 


draw(map)
frame(wks)
end