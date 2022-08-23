;高原总体站点days(降雪累积日数),gss,pre heavydays _all的 趋势和显著性
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;散点图参考 http://www.ncl.ucar.edu/Applications/polyg.shtml polyg_8_lbar.ncl
;  ncl /mnt/f/snow_related/code/by_ncl/trends/trend_all.ncl


load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

;根据降水量将经纬度数组分类
undef("mark_lat_lon")
  function mark_lat_lon(num_distinct_markers,b,lat,lon,npts)
  local num_distinct_markers,b,sig,lat,lon,npts,i,indexes,\
  npts_range,lat_new,lon_new
  begin
  lat_new = new((/num_distinct_markers,npts/),float,-999);设置成二维，标记*站点数
  lon_new = new((/num_distinct_markers,npts/),float,-999)
  do i = 0, num_distinct_markers-1
    if (i.eq.0) then ;第一个范围
      indexes = ind(b.gt.0) ;上升
    end if
    if (i.eq.1) then 
      indexes = ind(b.lt.0) ;显著上升
    end if
    if (.not.any(ismissing(indexes))) then 
      npts_range = dimsizes(indexes)   ; # of points in this range.
      lat_new(i,0:npts_range-1) = lat(indexes)
      lon_new(i,0:npts_range-1) = lon(indexes)
    end if
    delete(indexes)       
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
      gsres@gsMarkerColor      = colors(i)
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
  gsres@gsMarkerThicknessF = 4 
  gsres@gsMarkerColor  = "black"
  gsres@gsMarkerIndex  = 4
  gsres@gsMarkerSizeF  = 0.02
  pmid = gsn_add_polymarker(wks,map,lon_new,lat_new,gsres)      
  map@$unique_string("pmid")$ = pmid
  end



;-----------------------------main code------------------------------------
begin

;--------------------读站点数据----------------------------------
	filename= "gss_all"
	filepath= "/mnt/f/snow_sts_data/trends/"+filename+".txt"  ;参数文件路径
	pic_dir = "/mnt/f/snow_related/pic/snow_all/trends/"
	f       = asciiread(filepath,-1,"string")
	; sta     = stringtointeger(str_get_field(f,1," "))  ;读取站号
	lon     = stringtofloat(str_get_field(f(1:),2," ")) 
	lat     = stringtofloat(str_get_field(f(1:),3," ")) 
	b       = stringtofloat(str_get_field(f(1:),4," ")) 
	sig     = stringtofloat(str_get_field(f(1:),5," ")) 
	npts    = numAsciiRow(filepath)-1 ;获取行数-站点数

; print(b)
  b@_FillValue = 32700
  sig@_FillValue = 32700.

  lon_sig=where(sig.eq.1., lon, 32700.)
  lat_sig=where(sig.eq.1., lat, 32700.)
  lon_sig@_FillValue = 32700.
  lat_sig@_FillValue = 32700.

	num_distinct_markers = 2
	ref   =  mark_lat_lon(num_distinct_markers,b,lat,lon,npts)
  lat_new=ref[0]
  lon_new=ref[1]

;===========================================================================
; Begin plotting section.
	wks = gsn_open_wks("eps",pic_dir+filename)              

;---Set up some map resources.
	res                       = True
	res@gsnMaximize           = True             ; Maximize plot in frame.
	res@gsnDraw               = False            ; Will draw later
	res@gsnFrame              = False            ; Don't advance the frame
	res@gsnLeftString         = ""
	res@gsnRightString        = ""
	res@tmYROn                =False
	res@tmXTOn                =False
	; res@gsnAddCyclic          =False
	res@tmBorderThicknessF  =2.5   ; border 6x as thick,图框粗细
  res@tmXBMajorThicknessF =2.5
  res@tmXBMinorThicknessF =2.5
  res@tmYLMajorThicknessF =2.5
  res@tmYLMinorThicknessF =2.5
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



;-----------------------------绘制地图-------------------------
  map = gsn_csm_map(wks,mpres)

;-----------------------------绘制散点图-------------------------------------------
  colors=(/"orangered","chartreuse4"/)
  plot_rain_scatter(wks,colors,num_distinct_markers,\
                        lat_new,lon_new,map)

  plot_sig_scatter(wks,lat_sig,lon_sig,map)



;高原轮廓线
  shp_line="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Line.shp"  
	lnres                  = True     
	lnres@gsLineColor      ="orange"
	lnres@gsLineThicknessF = 4.0           ; 6x thickness          ; 6x thickness  
	shp_plot               = gsn_add_shapefile_polylines(wks,map,shp_line,lnres)

; 绘制图例

  resLg = True
  resLg@lgMonoItemType = True
  resLg@lgItemType = "Markers"
  resLg@lgMarkerIndexes =(/16,16/)
  resLg@lgMarkerColors = colors(::-1)
  resLg@lgMarkerSizes = (/0.02,0.02/)
  resLg@lgMarkerThicknessF=6
  resLg@vpWidthF = 0.2
  resLg@vpHeightF = 0.1
  resLg@lgLabelFontHeightF = 0.08
  resLg@lgPerimOn=True
  resLg@lgPerimFill = 0
  resLg@lgPerimFillColor ="white"
  resLg@lgBoxMinorExtentF=0.2 ;圆点和文字之间的距离



  lgstr=(/"Upward","Downward"/)
  lbid = gsn_create_legend(wks, 2,lgstr(::-1), resLg)
 
; 将图例放置在图中
  amres = True
  amres@amParallelPosF = -0.39 ;左右，正右左负
  amres@amOrthogonalPosF = 0.34 ;上下，正下负上
  dumLg = gsn_add_annotation(map, lbid, amres)


draw(map)
frame(wks)

end     
 


 

