;读取各个物理量的标准化回归系数，画彩色散点图
;绘制地形3/4/5km等值线,并将等值线变稀疏（切除+平滑）
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;散点图参考 http://www.ncl.ucar.edu/Applications/polyg.shtml polyg_8_lbar.ncl
;  ncl /mnt/f/snow_related/code/by_ncl/regress/coef.ncl


load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

procedure set_all_res(res,mpres,lnres)
  local res,mpres,lnres
  begin

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
  mpres@mpDataSetName           =  "/mnt/d/ChinaMap/Earth..4"
  mpres@mpOutlineSpecifiers     = (/"China:states"/)
  ;边界线
  ; mpres@mpOutlineBoundarySets   = "National"

  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 4.0           ; 6x thickness          ; 6x thickness  

  end

; 一张图的色标图例 
undef("add_labelbar")
  procedure add_labelbar(wks,levels,colors)
  local lbres, labels
  begin
  nlevels = dimsizes(levels)
  ; Draw a labelbar
  lbres                    = True
  lbres@vpWidthF           = 0.5           ; width
  lbres@vpHeightF          = 0.06            ; height
  lbres@lbPerimOn          = False            ; Turn off perimeter.
  lbres@lbOrientation      = "Horizontal"     ; Default is vertical.
  lbres@lbLabelAlignment   = "InteriorEdges"  ; Default is "BoxCenters",标签如何与标签栏对齐
  lbres@lbFillColors       = colors           ; Colors for boxes.
  lbres@lbMonoFillPattern  = True             ; Fill them all solid.
  lbres@lbLabelFontHeightF = 0.02            ; label font height
  lbres@lbBoxLinesOn       =True
  lbres@lbBoxEndCapStyle   = "TriangleBothEnds"
  ; lbres@lbTitleString      ="(cm)"
  ; lbres@lbTitleFontHeightF = 0.02
  ; lbres@lbTitleJust        ="BottomRight"
  ; lbres@lbTitlePosition    ="Bottom"
  lbres@lbLabelStride      =1

  labels = sprintf("%2.1f",levels)

  gsn_labelbar_ndc(wks,nlevels+1,labels,0.25,0.235,lbres)
  frame(wks)                                   ; now advance the frame

  end

;根据数值将经纬度数组分类
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
      indexes = ind(R.lt.levels(0)) ;定位，且小于第一个level的点会画出来 白色
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
  gsres@gsMarkerSizeF      = 0.02
  gsres@gsMarkerThicknessF = 3 
  do i = 0, num_distinct_markers-1
    if (.not.ismissing(lat_new(i,0)))
      gsres@gsMarkerColor      = colors(i,:)
      pmid(i) = gsn_add_polymarker(wks,mapplot,lon_new(i,:),lat_new(i,:),gsres)      
    end if
  end do
  mapplot@$unique_string("pmid")$ = pmid
  end

; 画显著性
undef("plot_sig_scatter")
  procedure plot_sig_scatter(wks,lat_new,lon_new,map)
  local gsres,pmid
  begin

  gsres               = True
  gsres@gsMarkerThicknessF = 3 
  gsres@gsMarkerColor  = "black"
  gsres@gsMarkerIndex  = 4
  gsres@gsMarkerSizeF  = 0.02
  pmid = gsn_add_polymarker(wks,map,lon_new,lat_new,gsres)      
  map@$unique_string("pmid")$ = pmid
  end

;-----------------------------main code------------------------------------
begin

folder = "third_wf_Ri/"
pic_dir = "/mnt/f/snow_related/pic/regress/"+folder
filename =(/"WRPI","IBTI" ,"rh", "tcdist","tmp","Wf","Ri"/) 

count = 0
; 填色区间
  levels = fspan(-0.3, 0.3, 7)
  ; levels = fspan(-0.3, 0.3, 7)
  ; levels = fspan(-2, 2, 11)
  ; levels = fspan(-0.4, 0.4, 11)
  ; levels = fspan(-1, 1, 11)
  ; levels = fspan(-0.4, 0.4, 11)
  ; levels = fspan(-0.5, 0.5, 11)

  nlevels = dimsizes(levels)

  ; 自动生成指定数目的色卡
  colors  = span_color_rgba("MPL_bwr",nlevels+1)
  ; colors  = span_color_rgba("BlueDarkRed18",nlevels+1)

  
  filepath := "/mnt/f/snow_sts_data/regress/"+folder+filename(count)+".txt"  
  f       := asciiread(filepath,-1,"string")
  ; sta     = stringtointeger(str_get_field(f,1," "))  ;读取站号
  gss     := stringtofloat(str_get_field(f(1:),5," ")) 
  sig     := stringtofloat(str_get_field(f(1:),6," ")) 
  lon       = stringtofloat(str_get_field(f(1:),2," ")) 
  lat       = stringtofloat(str_get_field(f(1:),3," "))
  npts      = numAsciiRow(filepath)-1 ;获取行数-站点数
  ;注意：这里的txt文件最后一行数据下面需要空白行，才能读出文件的正确行数
  ;大多数txt文件都满足要求，但还是需要核实一下
  ;设置缺测值
  gss@_FillValue := 32700.
  sig@_FillValue := 32700.
  lon_sig := where(sig.eq.1., lon, 32700.)
  lat_sig := where(sig.eq.1., lat, 32700.)
  lon_sig@_FillValue := 32700.
  lat_sig@_FillValue := 32700.

  ; 通过编号指定颜色的色卡
  ; cmap  = read_colormap_file("temp_19lev")
  ; id=(/5,12,14,15,17,18,19/)
  ; cmap1= cmap(id,:)
  ; colors=cmap1


  num_distinct_markers := nlevels+1        ; number of distinct markers

  ref   := mark_lat_lon(num_distinct_markers,gss,levels,lat,lon,npts)
  lat_new_total := ref[0]
  lon_new_total := ref[1]


wks = gsn_open_wks("x11",pic_dir+filename(count))              ; send graphics to PNG file

res       = True
mpres     = True
lnres     = True
set_all_res(res,mpres,lnres) 

;-绘制散点图-------------------------------------------
  map = gsn_csm_map(wks,mpres)
  plot_rain_scatter(wks,colors,num_distinct_markers,lat_new_total,\
                    lon_new_total,map)
  ; plot_sig_scatter(wks,lat_sig,lon_sig,map)

;高原轮廓线
  shp_line = "/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Line.shp"  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shp_line,lnres)


draw(map)
;色标图例
add_labelbar(wks,levels,colors) 

frame(wks)  

end     
 


 

