;读取组内的TC所有活动日（包含顺延一天) ERA5 500hPa nc资料，
;以UTC12为日界 做日平均 
;计算每日水汽通量和散度 
;选出降雪日再做平均，绘图
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"

;  ncl /mnt/e/f/snow_related/code/by_ncl/RTC/plot_500vap_12UTC_ave.ncl


begin

pic_dir  = "/mnt/e/f/snow_related/pic/RTC/atmos_env/" 

type_save_name="snow_date_1" ;all_tc_days snow_date_3
var_save_name="vap500_"
fout_name = "/mnt/f/f/snow_sts_data/RTC/"+\
var_save_name+type_save_name+".nc"
data    = addfile(fout_name, "r")

flux_avg = data->var01
fluxdev_avg = data->var02
qu_avg = data->var03
qv_avg = data->var04

; flux_avg = data->var01
; qu_avg = data->var02
; qv_avg = data->var03

;  绘图
wks = gsn_open_wks("png", pic_dir+var_save_name+"dev_"+type_save_name)


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
  mpres@mpDataSetName           =  "/mnt/e/d/ChinaMap/Earth..4"
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

  ; ; 水汽通量距平填色 弃用
  ; cmap  = read_colormap_file("BlWhRe")
  ; id=ispan(30, 70, 1)
  ; cmap1= cmap(id,:)
  ; colors=cmap1
  ; cnres@cnFillPalette       =colors
  ; cnres@cnLevelSelectionMode = "ManualLevels" 
  ; cnres@cnMinLevelValF      = -2
  ; cnres@cnMaxLevelValF      = 2
  ; cnres@cnLevelSpacingF      = 0.5

  ; ; 水汽通量距平填色 
    cnres@cnFillPalette        = "perc2_9lev"
    cnres@cnLevelSelectionMode = "ExplicitLevels"  
    cnres@cnLevels             = fspan(0, 4, 9)
    cnres@cnFillColors         = (/-1,1,2,3,4,5,6,7,8,9/)

  ;水汽通量散度填色BlueRed
  ; cnres@cnFillPalette       = "BlueWhiteOrangeRed"  
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


;绘图

map = gsn_csm_map(wks, mpres)
windPlot = gsn_csm_vector(wks, qu_avg , qv_avg , windRes)

contour_dev = gsn_csm_contour(wks,fluxdev_avg, cnres)
overlay(map, contour_dev)

; contour_avg = gsn_csm_contour(wks,flux_avg, cnres)
; overlay(map, contour_avg)

overlay(map, windPlot)


;高原轮廓线
shp="/mnt/e/d/data/TPshp/DBATP/DBATP_Line.shp"  
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 6.0           ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shp,lnres) 

draw(map)
frame(wks)


end