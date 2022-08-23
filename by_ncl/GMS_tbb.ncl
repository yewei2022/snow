;---------------------------------------------------
;GMS 卫星数据
;下一步对于每日 将格点tbb插值到站点
;根据tbb范围划定站点大概经纬度框，再选取tbb<=-20的站点
;labelbar的标标题设置参考 
;http://www.ncl.ucar.edu/Document/Graphics/Resources/lb.shtml#lbTitlePosition
;  ncl /mnt/f/snow_related/code/by_ncl/GMS_tbb.ncl

;---------------------------------------------------
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"


begin

;1 读TBB并处理----------------------------------
  data_dir       ="/mnt/h/JMA-TBB-1981-1997/grd/"
  file_name      ="1981.grd"   
  pic_dir        ="/mnt/f/snow_related/pic/tbb/" 

  ntim           =2920
  nlat           =120
  nlon           =120
  ; UNDEF          =0
  ; tbb            = new ( (/ntim,nlat,nlon/), integer, UNDEF)
  ; setfileoption("bin", "ReadByteOrder", "LittleEndian") ;不要也罢
  tbb=fbindirread (data_dir+file_name,0,(/ntim,nlat,nlon/), "float")

  ; 时间属性
  tinvl          = 3 ;3h-interval
  tbb!0          = "time"
  tbb&time       =   ispan(0, (ntim - 1) * tinvl, tinvl)
  tbb&time@units =   "hours since 1981-01-01 00:00:0.0"; 实际是06:00
  ; tim_format = "%Y%N%D%H" ;1981120506
  tim_format     = "%Y-%N-%D %H:00 "  ;1981-12-05 06:00
  str_time       = cd_string(tbb&time,tim_format)
  ; YYYYMMDDHH   = cd_calendar(tbb&time,-3)   ;tbb&time can  be identified
  ; print(YYYYMMDDHH)
  ; exit
  init_time="1981-11-18 12:00"
  init_n   = str_match_ind(str_time, init_time)
  end_time ="1981-11-20 09:00"
  end_n    = str_match_ind(str_time, end_time)
  ; 返回str_time中和end_time匹配的位置ind
  npts=end_n-init_n+1

  ;其他属性
  tbb!1          ="lat"
  tbb!2          ="lon"
  lat            =fspan(-59.5, 59.5, 120)
  lon            =fspan(80.5, 200.5, 120)
  lat@units      = "degrees_north"
  lon@units      = "degrees_east"
  tbb&lat        = lat
  tbb&lon        = lon
  tbb@_FillValue = -9.990001e+08;0
  tbb@units      = "degree Kelvin"
  tbb@long_name  = "Temperature of Bright Blackbody"
  tbb@coordinates= "lat lon"
  tbb            = tbb+100-273        ;(convert degree Kelvin to degree Celsius)
  tbb@units      = "degree Celsius"


  ; printVarSummary(tbb(N,:,:))
  ; exit


;---- Begin to plot.
wks = gsn_open_wks("eps",pic_dir+str_time(end_n))


res = True
  res@gsnDraw                        = False
  res@gsnFrame                       = False
  ; res@gsnMaximize                  = True
  ;res@gsnAddCyclic                  = False 
  ; regional data, don't add longitude cyclic point
  ;res@pmTickMarkDisplayMode         = "Always" 
  ;关掉不需要的刻度,次刻度线和右上刻度线
  res@gsnLeftString=""
  res@gsnRightString=""
  res@tmYROn=False
  res@tmXTOn=False
  ; res@tiMainString =str_time(N)
  ;绘制省界
  mpres                                =res
  mpres@mpFillOn                       = False
  mpres@mpDataSetName                  = "/mnt/d/ChinaMap/Earth..4"
  mpres@mpDataBaseVersion              = "MediumRes"
  mpres@mpOutlineSpecifiers            = (/"China","China:Provinces"/)
  ;绘制国界
  mpres@mpOutlineOn                    = True
  mpres@mpOutlineBoundarySets          = "National"
  mpres@mpGridAndLimbOn =True
  mpres@mpGridLatSpacingF=2.5
  mpres@mpGridLonSpacingF=2.5
  mpres@mpGridLineDashPattern=15

  ;地图边界
  mpres@mpMinLonF                    = 80
  mpres@mpMaxLonF                    = 120
  mpres@mpMinLatF                    = 10
  mpres@mpMaxLatF                    = 45
  mpres@gsnMajorLonSpacing    =5. 
  mpres@gsnMinorLonSpacing    =1.    
  mpres@gsnMajorLatSpacing    =5. 
  mpres@gsnMinorLatSpacing    =1.


  ;tbb填图
  tbbres                                = res
  tbbres@cnFillOn                       = True
  ; tbbres@cnFillMode                   = "RasterFill" ;矩形栅格填充
  tbbres@cnLinesOn                      = False
  tbbres@cnInfoLabelOn=False

  tbbres@lbLabelBarOn                   = False

  ; tbbres@lbBoxLinesOn                   = True ; 色标之间分界线
  ; tbbres@lbOrientation                  = "vertical"            ; 垂直坐标
  ; tbbres@lbBoxEndCapStyle               = "TriangleBothEnds"
  ; tbbres@lbTitleOn                      = True
  ; tbbres@lbTitleString                  = "TBB/~S~o~N~C"
  ; tbbres@lbTitleJust                    = "TopRight"
  ; tbbres@lbTitlePosition                = "Bottom"
  ; tbbres@lbTitleFontHeightF             = 0.02
  ; tbbres@pmLabelBarOrthogonalPosF       = 0.02 ;色标条与图之间的距离
  ; tbbres@pmLabelBarWidthF               = 0.08     ;色标变窄
  ; tbbres@pmLabelBarHeightF              = 0.6

  tbbres@cnFillPalette                  = "perc2_9lev"   
  ; tbbres@cnLevelSelectionMode           ="ManualLevels"
  tbbres@cnLevelSelectionMode           = "ExplicitLevels"
  tbbres@cnLevels                       = (/-10,-20,-30,-40,-50,-60/)
  tbbres@cnFillColors                   = (/9,8,7,6,4,2,-1/) 

;组图
  pres=True
  pres@gsnFrame        = False  ; don't advance frame yet，以便后面使用gsn_legend_ndc   
  pres@gsnMaximize           = True                 ; maximize in frame
  pres@gsnPaperOrientation   = "Portrait"            ;portra和maximize必须同时设置才会生效
  pres@gsnPanelLabelBar      =True    ;共用一个色标
  ; pres@pmLabelBarOrthogonalPosF       = -0.008 ;色标条与图之间的距离
  ; pres@pmLabelBarParallelPosF         = 0.0 
  pres@pmLabelBarWidthF               = 0.5    
  pres@pmLabelBarHeightF              = 0.05
  pres@lbBoxLinesOn                   = True ; 色标之间分界线
  pres@lbBoxEndCapStyle               = "TriangleBothEnds"
  pres@lbLabelFontHeightF             = 0.01
  pres@gsnPanelFigureStrings          = str_time(init_n:end_n)
  pres@amJust                         ="topLeft"

;绘图
map=new(npts,graphic)
tbb_plot=new(npts,graphic)
do i=0, npts-1
  map(i) = gsn_csm_map(wks, mpres)
  tbb_plot(i) = gsn_csm_contour(wks,tbb(i+init_n,:,:),tbbres)
  overlay(map(i), tbb_plot(i))
end do


;高原轮廓线可以在循环之外,panel之前
  shp_line="/mnt/f/snow_sts_data/TPBoundary2021/TPBoundary_new(2021).shp"  
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 4.0           ; 6x thickness          ; 6x thickness  
 shp_plot               = gsn_add_shapefile_polylines(wks,map,shp_line,lnres)

print(npts) 
gsn_panel(wks, map, (/4,4/), pres)      
; draw(map)
frame(wks) 
end 
