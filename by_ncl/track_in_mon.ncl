; 各个月份的track,降雪期间的TC位置

;  ncl /mnt/f/snow_related/code/by_ncl/track_in_mon.ncl

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
;********************************************************
undef("plot_track")
  procedure plot_track(wks,fiTC,map,color)
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
  resLine@gsLineThicknessF = 6
  dumLine = new(nrow, graphic) 
  ;»æÖÆÏß
  do i = 0, nrow-2
    xx = (/ lon_tc(i), lon_tc(i+1)/)
    yy = (/ lat_tc(i), lat_tc(i+1)/) 
    dumLine(i) = gsn_add_polyline(wks, map, xx, yy, resLine)
  end do
  ;»æÖÆµã
  resDot =True
  resDot@gsMarkerIndex = 1
  resDot@gsMarkerSizeF = 0.025
  resDot@gsMarkerColor = color
  dumDot = gsn_add_polymarker(wks, map, lon_tc(0), lat_tc(0), resDot)
  map@$unique_string("dumDot")$ = dumDot
  map@$unique_string("dumLine")$ = dumLine
  end

begin

pic_dir = "/mnt/f/snow_related/pic/tc/"

count=7
file_name=(/"02","04","05","06","09","10","11","12"/)
mon_name = (/"Feb","Apr","May","Jun","Sep", "Oct","Nov","Dec"/)
TC_file_path= "/mnt/f/snow_sts_data/TC/track_in_season.txt"
nfil        = numAsciiRow(TC_file_path)-1
files       = asciiread(TC_file_path, -1, "string")
TC          = str_get_field(files(1:),5," ")
TC_mon      = str_get_field(files(1:),2," ")
snow_file_path= "/mnt/f/snow_sts_data/TC/TC_dot_season.txt"
snow_files    = asciiread(snow_file_path, -1, "string")
lon_snow      = stringtofloat(str_get_field(snow_files(1:),2," ")) 
lat_snow      = stringtofloat(str_get_field(snow_files(1:),3," "))
dot_mon       = str_get_field(snow_files(1:),5," ")
wind_snow     = stringtoint(str_get_field(snow_files(1:),7," "))



wks = gsn_open_wks("eps", pic_dir+"track"+file_name(count))
  gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
colours=(/4,7,12,13,16,14,15/)

  res = True
  res@gsnLeftString = mon_name(count)
  res@gsnLeftStringFontHeightF=0.02
  res@gsnLeftStringOrthogonalPosF=0.012
  res@gsnDraw = False
  res@gsnFrame = False
  res@gsnMaximize=True
  res@gsnAddCyclic=False
  res@vpWidthF=0.5
  res@vpHeightF=0.6


  ;¹Ø¿Ì¶È
  res@tmXTOn = False 
  res@tmYROn = False
; ÉèÖÃµØÍ¼±ß½ç
  res@mpMinLatF = 2
  res@mpMaxLatF = 30
  res@mpMinLonF = 75.
  res@mpMaxLonF = 105.
  res@gsnMajorLonSpacing    =5 
  res@gsnMinorLonSpacing    =1  
  res@gsnMajorLatSpacing    =5 
  res@gsnMinorLatSpacing    =1

  res@mpDataSetName = "/mnt/d/ChinaMap/Earth..4"
  res@mpFillOn      = False
  res@mpOutlineBoundarySets = "National"
  res@mpDataBaseVersion = "MediumRes"

; ;------------------------------画路径--------------------------
  map = gsn_csm_map(wks,res)
color="black"
  do i=0,nfil-1
    if (TC_mon(i).eq.file_name(count)) then
    plot_track(wks,TC(i),map,color)  
    end if   
  end do

 
; ; ==============================»绘制降雪时的TC位置======================
  mon_ind=str_match_ind(dot_mon, file_name(count))
  lon_dot=lon_snow(mon_ind)
  lat_dot=lat_snow(mon_ind)
  wind_dot=wind_snow(mon_ind)

  txres               = True                     ; text mods desired
  txres@txFontHeightF = 0.025                     ; font smaller. default big
  txres@txFontThicknessF=3

  dum_tc= new(dimsizes(wind_dot), graphic)
do i=0,dimsizes(wind_dot)-1
  if (wind_dot(i).le.33) then
    txres@txFontColor = colours(0)
  else if (wind_dot(i) .ge. 34 .and. wind_dot(i).le.63) then
    txres@txFontColor = colours(1)
  else if(wind_dot(i) .ge. 64 .and. wind_dot(i).le.82) then
    txres@txFontColor = colours(2)
  else if(wind_dot(i) .ge. 83 .and. wind_dot(i).le.95) then
    txres@txFontColor = colours(3)
  else if(wind_dot(i) .ge. 96 .and. wind_dot(i).le.112) then
    txres@txFontColor = colours(4)
  else if(wind_dot(i) .ge. 113 .and. wind_dot(i).le.135) then
    txres@txFontColor = colours(5) 
  else 
    txres@txFontColor = colours(6)   
  end if
    end if
      end if
        end if 
      end if 
    end if

  dum_tc(i) = gsn_add_text(wks,map,"~F37~p",lon_dot(i),lat_dot(i),txres) 
end do

; 高原轮廓线
  shp_line="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Line.shp"  
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 8.0           ; 6x thickness          ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,map,shp_line,lnres)

draw(map)
frame(wks)

end
