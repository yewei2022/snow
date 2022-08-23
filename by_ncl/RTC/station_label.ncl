;读取站点分类
;  ncl /mnt/e/f/snow_related/code/by_ncl/RTC/station_label.ncl


load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"


;贴上区域分割线
undef("mark_area")
  procedure mark_area(wks,map,xpts,ypts)
  begin
  resp                  = True                      ; polyline mods desired
  resp@gsLineColor      = "black"                     ; color of lines
  resp@gsLineThicknessF = 3.0                       ; thickness of lines
  dum_box=gsn_add_polyline(wks,map,xpts,ypts,resp)      
  map@$unique_string("dum_box")$ = dum_box
  end



;根据label将经纬度数组分类
undef("mark_lat_lon")
  function mark_lat_lon(num_distinct_markers,R,levels,lat,lon,npts)
  local num_distinct_markers,R,levels,lat,lon,npts,i,indexes,\
  npts_range,lat_new,lon_new
  ; Create X and Y arrays to hold the points for each range and initialize
  ; them to missing values.  We want to use num_distinct_markers
  ; different colors, so we need num_distinct_markers sets of X and
  ; Y points.
  begin
  ; Group the points according to which range they fall in. At the
  ; same time, create the label that we will use later in the labelbar  
  lat_new = new((/num_distinct_markers,npts/),float,-999);设置成二维，标记*站点数
  lon_new = new((/num_distinct_markers,npts/),float,-999)

  do i = 0, num_distinct_markers-1
    indexes = ind(R.eq.levels(i))
    if (.not.any(ismissing(indexes))) then 
      npts_range = dimsizes(indexes)   ; # of points in this range.
      lat_new(i,0:npts_range-1) = lat(indexes)
      lon_new(i,0:npts_range-1) = lon(indexes)
    end if
    delete(indexes)            ; Necessary b/c "indexes" may be a different
  end do

  return([/lat_new,lon_new/])
 end

undef("plot_rain_scatter")
  procedure plot_rain_scatter(wks,colors,num_distinct_markers,\
                        lat_new,lon_new,mapplot)
  local i,gsres,pmid
  begin
  pmid = new(num_distinct_markers,graphic)
  gsres               = True
  gsres@gsMarkerIndex = 16  ;
  gsres@gsMarkerSizeF      = 0.01
  gsres@gsMarkerThicknessF = 1
  do i = 0, num_distinct_markers-1
    if (.not.ismissing(lat_new(i,0)))
      gsres@gsMarkerColor      = colors(i)
      pmid(i) = gsn_add_polymarker(wks,mapplot,lon_new(i,:),lat_new(i,:),gsres)      
    end if
  end do
  mapplot@$unique_string("pmid")$ = pmid
  end

;-----------------------------main code------------------------------------
begin

;--------------------读站点数据----------------------------------
  filename="f_mean_station_label"
  filepath = "/mnt/f/f/snow_sts_data/RTC/"+filename+".txt"  ;参数文件路径
  pic_dir = "/mnt/e/f/snow_related/pic/RTC/"
  f       = asciiread(filepath,-1,"string")
  ; sta     = stringtointeger(str_get_field(f,1," "))  ;读取站号
  lon     = stringtofloat(str_get_field(f(1:),2," ")) 
  lat     = stringtofloat(str_get_field(f(1:),3," "))
  label   = stringtofloat(str_get_field(f(1:),4," "))
  label@_FillValue = 32700

  npts    = numAsciiRow(filepath)-1 ;获取行数-站点数

  levels=(/0., 1., 2., 3./)
  colors  = (/"blue","red","purple","black"/)
  num_distinct_markers = dimsizes(levels)        ; number of distinct markers

  ref   =mark_lat_lon(num_distinct_markers,label,levels,lat,lon,npts)
  lat_new_total=ref[0]
  lon_new_total=ref[1]


;读地形文件
  topo        = addfile("/mnt/e/d/data/other/ETOPO2v2c_f4.nc", "r")
  elev        = topo->z({0:50},{70:110}) 
  lat_topo    = topo->y({0:50})
  lon_topo    = topo->x({70:110}) 
  lat_topo!0     = "lat"
  lon_topo!0     = "lon"
  lat_topo@units = "degrees_north"
  lon_topo@units = "degrees_east"
  lat_topo&lat   = lat_topo
  lon_topo&lon   = lon_topo

  ;---Attach the coordinate arrays
  elev!0    = "lat"
  elev!1    = "lon"
  elev&lat  = lat_topo
  elev&lon  = lon_topo

;===========================================================================
; Begin plotting section.
  wks = gsn_open_wks("png",pic_dir+filename)              ; send graphics to PNG file

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
  res@tmXBLabelFontHeightF  =0.02

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
  mpres@mpDataSetName           =  "/mnt/e/d/ChinaMap/Earth..4"
  mpres@mpOutlineSpecifiers     = (/"China:states"/)
  ; ;边界线
  ; mpres@mpOutlineBoundarySets   = "National"


  ;---高原地形填图
  topores                    = res
  topores@cnFillOn           = True             ; turn off contour fill
  topores@cnFillPalette      = "OceanLakeLandSnow" ;topo_15lev OceanLakeLandSnow MPL_Greys
  topores@cnLinesOn          = False
  topores@cnLevelSelectionMode="ManualLevels" 
  topores@cnLevelSpacingF    = 500
  topores@cnMinLevelValF     = 0
  topores@cnMaxLevelValF     =5000            
  topores@cnFillMode         = "RasterFill"     ; much faster than AreaFill
  topores@lbBoxLinesOn       = True ; Label bar
  ; topores@lbLabelAutoStride  = True            ; let NCL determine label spacing
  topores@lbLabelStride  = 2            ; let NCL determine label spacing

  topores@cnLineLabelsOn     = False            ; turn off line labels
  topores@cnInfoLabelOn      = False            ; turn off info label
  topores@pmLabelBarHeightF  = 0.12
  topores@lbBoxEndCapStyle   ="TriangleBothEnds"
  topores@pmLabelBarOrthogonalPosF  = 0.15 ;色标离图的距离
  topores@lbTitleString                  ="elevation(m)"
  topores@lbTitleJust                    ="BottomRight"
  topores@lbTitlePosition                ="Bottom"
  topores@lbLabelFontHeightF = 0.01
  topores@lbTitleFontHeightF = 0.01

;-----------------------------绘图-------
  map = gsn_csm_map(wks,mpres)
  ; topo_plot = gsn_csm_contour(wks,elev,topores)
  ; overlay(map, topo_plot)
  plot_rain_scatter(wks,colors,num_distinct_markers,lat_new_total,\
                    lon_new_total,map)

  ypts1 = (/37.8,  35.1,  32.1,  27.8/)
  xpts1 = (/86.2,  99.3,  100.8, 100.8/)
  mark_area(wks,map,xpts1,ypts1)

  ypts2 = (/ 36.4,30,30.4,32.1,32.1/)
  xpts2 = (/ 82,88,95,97.5,100.8 /)
  mark_area(wks,map,xpts2,ypts2)

  ; ypts3 = (/ 32.5,28.2,28.5,28.8,29.3,30.5,30.5/)
  ; xpts3 = (/ 79.1,87, 89.5,92.5,95,98,100.8/)
  ; mark_area(wks,map,xpts3,ypts3)

  ; ypts4 = (/ 30., 27.9/) ;27.9
  ; xpts4 = (/ 97,  97/) ;97
  ; mark_area(wks,map,xpts4,ypts4)

  ;标记区域名称
  letters=(/"E","C","S","SM","SE"/)
  lat_letter=(/37, 35, 30, 31.5, 29.5/)
  lon_letter=(/99, 92, 86, 79.5, 99/)
  dumletter=new(dimsizes(letters), graphic)
  reslet = True
  reslet@txFontHeightF = 0.02
  reslet@txFontThicknessF=0.24
  reslet@txFontColor = "black"
  ; reslet@txJust = "CenterLeft"
  do i=0,dimsizes(letters)-3
  dumletter(i)= gsn_add_text(wks,map,letters(i),lon_letter(i), \
                             lat_letter(i), reslet)
  end do

;高原轮廓线
  shp_line="/mnt/f/f/snow_sts_data/TPshp/DBATP/DBATP_Line.shp"   
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 4.0           ; 6x thickness          ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shp_line,lnres)

draw(map)
frame(wks)

end     
 


 

