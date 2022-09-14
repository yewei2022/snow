;读取不同路径的降水量，画累积彩色散点图
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;散点图参考 http://www.ncl.ucar.edu/Applications/polyg.shtml polyg_8_lbar.ncl
;  ncl /mnt/f/snow_related/code/by_ncl/track_amts.ncl


load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

; Give a contour/map plot, retrieve the contour levels associated with it.
undef("get_contour_levels")
  function get_contour_levels(plot)
  begin
    getvalues plot@contour
      "cnLevels" : levels
  end getvalues
  return(levels)
  end

; Give a contour/map plot, retrieve the contour colors associated with the levels
undef("get_contour_colors")
  function get_contour_colors(plot)
  begin
    getvalues plot@contour
      "cnLineColors" : colors
  end getvalues
  return(colors)
  end


; 一张图的色标图例 
undef("add_labelbar")
  procedure add_labelbar(wks,levels,colors)
  local lbres, labels
  begin
  nlevels = dimsizes(levels)
  ; Draw a labelbar
  lbres                    = True
  lbres@vpWidthF           = 0.4           ; width
  lbres@vpHeightF          = 0.08            ; height
  lbres@lbPerimOn          = False            ; Turn off perimeter.
  lbres@lbOrientation      = "Horizontal"     ; Default is vertical.
  lbres@lbLabelAlignment   = "InteriorEdges"  ; Default is "BoxCenters",标签如何与标签栏对齐
  lbres@lbFillColors       = colors           ; Colors for boxes.
  lbres@lbMonoFillPattern  = True             ; Fill them all solid.
  lbres@lbLabelFontHeightF = 0.015            ; label font height
  lbres@lbBoxLinesOn       =True
  ; lbres@lbBoxEndCapStyle   = "TriangleBothEnds"
  lbres@lbTitleString      ="(mm)"
  lbres@lbTitleFontHeightF = 0.015
  lbres@lbTitleJust        ="BottomRight"
  lbres@lbTitlePosition    ="Bottom"
  lbres@lbLabelStride      =1

  labels = sprintf("%2.1f",levels)

  gsn_labelbar_ndc(wks,nlevels+1,labels,0.3,0.18,lbres)
  frame(wks)                                   ; now advance the frame

  end

;根据降水量将经纬度数组分类
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
    if (i.eq.0) then ;第一个范围
      indexes = ind(R.lt.levels(0)) ;定位，且小于等于第一个level的点会画出来
    end if
    if (i.eq.num_distinct_markers-1) then ;最后一个范围
      indexes = ind(R.ge.max(levels))
    end if
    if (i.gt.0.and.i.lt.num_distinct_markers-1) then    ;中间的范围，因为格式不一样，要分别设置
      indexes = ind(R.ge.levels(i-1).and.R.lt.levels(i))
    end if
   ; Now that we have the set of indexes whose values fall within 
   ; the given range, take the corresponding lat/lon values and store
   ; them, so later we can color this set of markers with the appropriate color.
    if (.not.any(ismissing(indexes))) then 
      npts_range = dimsizes(indexes)   ; # of points in this range.
      lat_new(i,0:npts_range-1) = lat(indexes)
      lon_new(i,0:npts_range-1) = lon(indexes)
    end if
    delete(indexes)            ; Necessary b/c "indexes" may be a different
    ; size next time.
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
  gsres@gsMarkerSizeF      = 0.008
  gsres@gsMarkerThicknessF = 1.5 
  do i = 0, num_distinct_markers-1
    if (.not.ismissing(lat_new(i,0)))
      gsres@gsMarkerColor      = colors(i)
      pmid(i) = gsn_add_polymarker(wks,mapplot,lon_new(i,:),lat_new(i,:),gsres)      
    end if
  end do
  mapplot@$unique_string("pmid")$ = pmid
  end

undef("plot_track")
  procedure plot_track(wks,fiTC,color,map)
  local i,data,nrow,lat_tc,lon_tc,resLine,dumLine
  begin
  data = asciiread(fiTC, -1, "string")
  nrow = numAsciiRow(fiTC)
  lat_tc = new(nrow, "float")
  lon_tc = new(nrow, "float")
  lat_tc = stringtofloat(str_get_field(data, 7, ",")) *0.1
  lon_tc = stringtofloat(str_get_field(data, 8, ",")) *0.1
  resLine = True
  resLine@gsLineColor=color
  resLine@gsLineThicknessF = 3
  dumLine = new(nrow, graphic) 
  ;绘制线
  do i = 0, nrow-2
    xx = (/ lon_tc(i), lon_tc(i+1)/)
    yy = (/ lat_tc(i), lat_tc(i+1)/) 
    dumLine(i) = gsn_add_polyline(wks, map, xx, yy, resLine)
  end do
  map@$unique_string("dumLine")$ = dumLine
  end

;-----------------------------main code------------------------------------
begin

;--------------------读站点数据----------------------------------
  filepath = "/mnt/f/snow_sts_data/1981-2020/"  ;参数文件路径
  WW=1
  filename=(/"typeA","typeB","typeC"/)
  pic_dir = "/mnt/f/snow_related/pic/snow_byTC/"
  f       = asciiread(filepath+"amts_"+filename(WW)+".txt",-1,"string")
  ; sta     = stringtointeger(str_get_field(f,1," "))  ;读取站号
  lat     = stringtofloat(str_get_field(f(1:),3," ")) 
  lon     = stringtofloat(str_get_field(f(1:),2," ")) 
  amts  = stringtofloat(str_get_field(f(1:),4," ")) 
  npts    = numAsciiRow(filepath+"days_"+filename(WW)+".txt")-1 ;获取行数-站点数
  ;设置缺测值
  amts@_FillValue = 32700.
  levels=(/0.1,2.5,5.,10.,20.,30./)

  nlevels = dimsizes(levels)
  colors  = (/"white","deepskyblue","palegreen1","gold",\
             "lightcoral","orangered","red4"/)

  num_distinct_markers = nlevels+1        ; number of distinct markers

  ref   =mark_lat_lon(num_distinct_markers,amts,levels,lat,lon,npts)
  lat_new_total=ref[0]
  lon_new_total=ref[1]

;===========================================================================
; Begin plotting section.
  wks = gsn_open_wks("ps",pic_dir+filename(WW)+"_amts")              
  gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
  colors_track=(/14,7,4/)
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
  res@vpWidthF=0.5
  res@vpHeightF=0.5

  mpres                       =res
  mpres@mpMinLatF             = 4.
  mpres@mpMaxLatF             = 40.
  mpres@mpMinLonF             = 75
  mpres@mpMaxLonF             = 105
  ; mpres@gsnMajorLonSpacing    =5 
  ; mpres@gsnMinorLonSpacing    =2.    
  ; mpres@gsnMajorLatSpacing    =5 
  ; mpres@gsnMinorLatSpacing    =2

  mpres@mpFillOn=False

  mpres@mpDataBaseVersion       = "MediumRes"
  mpres@mpDataSetName           =  "/mnt/d/ChinaMap/Earth..4"
  mpres@mpOutlineSpecifiers     = (/"China:states"/)
  ;边界线
  mpres@mpOutlineBoundarySets   = "National"



;-----------------------------绘制地图-------------------------
  map2 = gsn_csm_map(wks,mpres)



;-----------------------------绘制散点图-------------------------------------------

  plot_rain_scatter(wks,colors,num_distinct_markers,lat_new_total,lon_new_total,map2)

; ;------------------------------绘制风暴路径--------------------------
  fil_list= "/mnt/f/snow_sts_data/TC/"+filename(WW)+"_catalog.txt"
  catalog= asciiread(fil_list, -1, "string")
  nfil = numAsciiRow(fil_list)
  do i=0,nfil-1
    plot_track(wks,catalog(i),colors_track(WW),map2)
  end do

;高原轮廓线
  shp_line="/mnt/f/snow_sts_data/TPBoundary2021/TPBoundary_new(2021).shp"  
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 4.0           ; 6x thickness          ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map2,shp_line,lnres)

draw(map2)
;色标图例
add_labelbar(wks,levels,colors) 

end     
 


 

