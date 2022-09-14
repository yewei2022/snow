;----------------------------------------------------------------------
; 参考 scatter_10.ncl ; polyg_4.ncl 
;https://www.ncl.ucar.edu/Applications/scatter.shtml
;https://www.ncl.ucar.edu/Applications/polyg.shtml
; 想做站点数 不同降水等级的频次统计 这个图没啥用

;  ncl /mnt/f/snow_related/code/by_ncl/boxes.ncl

begin

pic_dir = "/mnt/f/snow_related/pic/tc/"
count=0

lon=fspan(0, 1000, 6)

; lon=fspan(75., 500,6)

pic_name=(/"TC_snow_pre","TC_snow_gss"/)
colors  = (/"deepskyblue","palegreen1","gold",\
           "lightcoral","orangered","red"/)

levels=(/2,4,6,8,10/)

f3= asciiread("/mnt/f/snow_sts_data/1981-2020/TC_snow_pre_gss.txt",-1,"string")
lon_dot   = stringtofloat(str_get_field(f3(1:),count+3," "))
lat_dot   = stringtofloat(str_get_field(f3(1:),2," ")) ;纵坐标 影响的站数

npts=numAsciiRow("/mnt/f/snow_sts_data/1981-2020/TC_snow_pre_gss.txt")-1
lat=fspan(0, 90, 19)
; print(lat)

mlat=dimsizes(lat)
mlon=dimsizes(lon)
w=fspan(0, 0, mlat*mlon)
x=reshape(w, (/mlat,mlon/)) ;存储频数
x!0          ="lat"
x!1          ="lon"
x&lat        = lat
x&lon        = lon

do j=0,mlon-2
	do i=0,mlat-2
		minlat=lat(i)
		maxlat=lat(i+1)
		minlon=lon(j)
		maxlon=lon(j+1)
		do m=0,npts-1
			if((lat_dot(m).ge.minlat ).and.(lat_dot(m).lt.maxlat))\
				.and.((lon_dot(m).ge.minlon) .and.(lon_dot(m).lt.maxlon)) then
				x(i,j)=x(i,j)+1
			end if
		end do
	end do
end do 
print(x)
; exit

;---Start the graphics
  wks   = gsn_open_wks ("x11",pic_dir+pic_name(count))    

;---Resources for blank plot
  bres                = True                     ; plot mods desired

  bres@gsnDraw        = False
  bres@gsnFrame       = False
  bres@gsnMaximize    =False

  bres@trYMinF        = 0      ; polygons will go from 1,ny in y
  bres@trYMaxF        = 90
  ; bres@tmYLValues=lat
  ; bres@tmYLMinorOn=False
  ; bres@tmYLMinorPerMajor=3


  bres@trXMinF        = 0       ; polygons will go from 1,nx in x
  bres@trXMaxF        = 1000
  ; bres@tmXBValues=lon
  ; bres@tmXBMinorPerMajor=3
  ; bres@tmXBMinorOn=False

  bres@tmXMinorGrid=True
  bres@tmYMinorGrid=True
  bres@tmXMajorGrid=True
  bres@tmYMajorGrid=True
  bres@tmXMinorGridLineDashPattern=15
  bres@tmYMinorGridLineDashPattern=15
  bres@tmXMajorGridLineDashPattern=15
  bres@tmYMajorGridLineDashPattern=15

  bres@tiXAxisString="Precipitation(mm)"
  bres@tiYAxisString="Number of stations with snowfall"
     
  ; bres@tfDoNDCOverlay = True           ; Important for the overlay.
; bres@tfDoNDCOverlay = "NDCViewport"  ; NCL V6.5.0 or later

; ;---Turn off all tickmarks
;   bres@tmXBOn         = False
  ; bres@tmXTOn         = False
  ; bres@tmYROn         = False
;   bres@tmYLOn         = False

  plot = gsn_csm_blank_plot (wks,bres)        ; Create blank plot


;---Resources for filled squares
  gnres                 = True
  gnres@tfPolyDrawOrder = "PreDraw"    ; Draw before map outlines
;
; Loop through the integers tmin and tmax, and add
; a set of filled squares for each grouping.
  nx   = mlon-1     ; Make twice as long as x so
  ny   = mlat-1     ; we get square boxes in map.
  dum = new(nx*ny,graphic)      ; Dummy array to hold polygon id's.

	do i=0,ny-1
		 do j=0,nx-1
		  box_value = x(i,j)
      if box_value.lt.levels(0) then
				gnres@gsFillColor = colors(0)
			else if box_value.ge.levels(0) .and. box_value.lt.levels(1) then
				gnres@gsFillColor = colors(1)
			else if box_value.ge.levels(1) .and. box_value.lt.levels(2) then
				gnres@gsFillColor = colors(2)
			else if box_value.ge.levels(2) .and. box_value.lt.levels(3) then
				gnres@gsFillColor = colors(3)	
			else if box_value.ge.levels(3) .and. box_value.lt.levels(4) then
				gnres@gsFillColor = colors(4)
			else if box_value.ge.levels(4)  then
				gnres@gsFillColor = colors(5)
			end if
			end if
			end if
			end if
			end if
			end if
		minlat=lat(i)
		maxlat=lat(i+1)
		minlon=lon(j)
		maxlon=lon(j+1)
		xbox=(/minlon,maxlon,maxlon,minlon,minlon/)
		ybox=(/minlat,minlat,maxlat,maxlat,minlat/)
    igon = j*nx+i
    dum(igon) = gsn_add_polygon(wks,plot,xbox,ybox,gnres)    ; Attach the box.
		end do
	end do

; 图例
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
  lbres@lbLabelFontHeightF = 0.015            ; label font height
  lbres@lbBoxLinesOn       =True
  lbres@lbBoxEndCapStyle   = "TriangleBothEnds"
  ; lbres@lbTitleString      ="(mm)"
  lbres@lbTitleFontHeightF = 0.015
  lbres@lbTitleJust        ="BottomRight"
  lbres@lbTitlePosition    ="Bottom"
  lbres@lbLabelStride      =1
  labels = sprintf("%2.0f",levels)

  gsn_labelbar_ndc(wks,nlevels+1,labels,0.25,0.08,lbres)

  draw(plot)       ; This draws the filled polygons and the plot.
  frame(wks)
end