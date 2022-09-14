;----------------------------------------------------------------------
; 参考 scatter_10.ncl ; polyg_4.ncl 
;https://www.ncl.ucar.edu/Applications/scatter.shtml
;https://www.ncl.ucar.edu/Applications/polyg.shtml
; 网格分辨率1*1
;  ncl /mnt/f/snow_related/code/by_ncl/TC_pos_f_1.ncl

begin

pic_dir = "/mnt/f/snow_related/pic/tc/"
count=0
pic_name=(/"TC_dot","TC_dot_extrm"/)

colors  = (/"white","deepskyblue","palegreen1","gold",\
           "lightcoral","orangered","red4"/)

; levels=(/1,5,10,15,20,25/)

levels=(/1,2,3,4,5,6/)

f3= asciiread("/mnt/f/snow_sts_data/TC/"+pic_name(count)+".txt",-1,"string")
lon_dot   = stringtofloat(str_get_field(f3(1:),3," "))
lat_dot   = stringtofloat(str_get_field(f3(1:),4," "))
npts=numAsciiRow("/mnt/f/snow_sts_data/TC/"+pic_name(count)+".txt")-1
lat=fspan(5, 30., 26)
lon=fspan(75., 100.,26)
lat@units      = "degrees_north"
lon@units      = "degrees_east"
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
; print(x)
; exit

;---Start the graphics
  wks   = gsn_open_wks ("eps",pic_dir+pic_name(count)+"_1")    

;---Resources for map plot
  mpres              = True

  ; mpres@gsnMaximize  = True
  mpres@gsnDraw      = False
  mpres@gsnFrame     = False
  mpres@tmXTOn=False
  mpres@tmYROn=False
  mpres@vpWidthF=0.5
  mpres@vpHeightF=0.6

	mpres@mpDataSetName = "/mnt/h/d/ChinaMap/Earth..4"
	mpres@mpFillOn      = False
	mpres@mpOutlineBoundarySets = "National"
	mpres@mpDataBaseVersion = "MediumRes"
  mpres@mpFillOn     = False

  mpres@mpMinLatF = 10
  mpres@mpMaxLatF = 30
  mpres@mpMinLonF = 77.
  mpres@mpMaxLonF = 99.
  mpres@gsnMajorLonSpacing    =5 
  mpres@gsnMajorLatSpacing    =5 
  mpres@gsnMinorLonSpacing    =1   
  mpres@gsnMinorLatSpacing    =1
  mpres@mpGridAndLimbOn =True
  mpres@mpGridLatSpacingF=1
  mpres@mpGridLonSpacingF=1
  mpres@mpGridLineDashPattern=15
  ;  mpres@mpGeophysicalLineThicknessF = 2.0    ; Default is 1.0
  ; mpres@tiMainString = "Dummy markers over a map"
  map = gsn_csm_map(wks,mpres)        ; Create map


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
			else if box_value.ge.levels(4) .and. box_value.lt.levels(5) then
				gnres@gsFillColor = colors(5)
			else if box_value.ge.levels(5) then
				gnres@gsFillColor = colors(6)  
			end if
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
    dum(igon) = gsn_add_polygon(wks,map,xbox,ybox,gnres)    ; Attach the box.
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

  gsn_labelbar_ndc(wks,nlevels+1,labels,0.25,0.23,lbres)

; 高原轮廓线
  shp_line="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Line.shp"  
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 8.0           ; 6x thickness          ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shp_line,lnres)

  draw(map)       ; This draws the filled polygons and the map.
  frame(wks)
end