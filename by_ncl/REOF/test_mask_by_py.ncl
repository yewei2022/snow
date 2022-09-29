load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "/mnt/f/snow_related/code/by_ncl/shapefile_utils.ncl"

; 测试分类
;  ncl /mnt/f/snow_related/code/by_ncl/REOF/test_mask_by_py.ncl


begin
;---Generate random data with an average of 10 and a stddev of 3.
  pic_dir ="/mnt/f/snow_related/pic/snow_TC/REOF/"
  count=73 ;2南部型 3北部型
  filename="time_tpmask_pre"
  file_dir="/mnt/f/snow_sts_data/REOF/"+filename+".nc" 
  data    = addfile(file_dir, "r")
  var     = data->pre(count,:,:)
  var@_FillValue = -999

; printVarSummary(var)

  ; ; 赋予坐标属性 可有可无
  ; lat     = data->lat
  ; lon     = data->lon
  ; lat@units      = "degrees_north"
  ; lon@units      = "degrees_east"
  ; var&lat        = lat
  ; var&lon        = lon
  ; print(max(var))
  ; print(min(var))


;---- Begin to plot.
wks = gsn_open_wks("x11",pic_dir+filename+tostring(count+1))

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
  mpres@mpMinLatF             = 26.
  mpres@mpMaxLatF             = 40.
  mpres@mpMinLonF             = 74
  mpres@mpMaxLonF             = 105
  mpres@gsnMajorLonSpacing    =5. 
  mpres@gsnMinorLonSpacing    =1.    
  mpres@gsnMajorLatSpacing    =5. 
  mpres@gsnMinorLatSpacing    =1

  mpres@mpFillOn=False

  mpres@mpDataBaseVersion       = "MediumRes"
  mpres@mpDataSetName           =  "/mnt/d/ChinaMap/Earth..4"
  mpres@mpOutlineSpecifiers     = (/"China:states"/)


  ;tbb填图
  cnres                               = res
  ;字符
  cnres@tiMainString ="REOF"+tostring(count+1)
  ; cnres@gsnLeftStringFontHeightF     =0.025
  ; cnres@gsnLeftStringOrthogonalPosF  =-0.12
  ; cnres@gsnLeftStringParallelPosF    =0.01
  ; cnres@txPerimOn=True
  ; cnres@txPerimThicknessF=2.5
  ; cnres@txBackgroundFillColor ="white"
  cnres@cnFillPalette= "BlueRed"
  cnres@cnFillOn                       = True
  ; cnres@cnFillMode                     = "RasterFill" ;矩形栅格填充
  cnres@cnLinesOn                      = False

 ; ;----测试数值范围
 ;  cnres@cnLevelSelectionMode ="ManualLevels"
 ;  ; cnres@cnMinLevelValF=-0.4
 ;  ; cnres@cnMaxLevelValF=0.4

  ; ; 正儿八经填色
  cnres@cnLevelSelectionMode = "ExplicitLevels"
  cnres@cnLevels = fspan(-1, 1, 11) 
  cnres@cnFillColors=(/2,22,42,62,92,122,128,148,168,188,208,228/)

  cnres@lbBoxLinesOn        = True ; Label bar
  ; cnres@lbLabelStride =2 ;每两个一个标签
  ; cnres@lbLabelAutoStride    = True               ; let NCL determine label spacing
  ; cnres@lbOrientation        = "Vertical"         ; vertical label bar
  ; cnres@pmLabelBarWidthF     = 0.05    
  cnres@pmLabelBarHeightF    = 0.15
  cnres@pmLabelBarOrthogonalPosF  = 0.15 ;色标离图的距离
  cnres@lbBoxEndCapStyle = "TriangleBothEnds"
  cnres@cnLineDrawOrder   ="PreDraw"
  cnres@cnFillDrawOrder   ="PreDraw"


map = gsn_csm_map(wks, mpres)
contour = gsn_csm_contour(wks,var, cnres)
overlay(map, contour)


;高原轮廓线
  shpfile  ="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Polygon.shp"
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 4.0           ; 6x thickness          ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shpfile,\
                                                       lnres)

draw(map)
frame(wks)
end

