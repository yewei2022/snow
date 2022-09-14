;读取降雪日降水量 插值，画日降水分布图
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;插值函数http://www.ncl.ucar.edu/Document/Functions/interp.shtml

;  ncl /mnt/f/snow_related/code/by_ncl/CTC/pre_interp.ncl

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "/mnt/h/d/ncl_related/code/shapefile_utils.ncl"

begin

;1.读取数据

  filename ="4"
  filepath = "/mnt/f/snow_sts_data/CTC/analysis/sta_avg_pre"+filename+".txt"  ;参数文件路径
  pic_dir = "/mnt/f/snow_related/pic/CTC/"
  f       = asciiread(filepath,-1,"string")
  ; sta     = stringtointeger(str_get_field(f,1," "))  ;读取站号
  lon     = stringtofloat(str_get_field(f(1:),2," ")) 
  lat     = stringtofloat(str_get_field(f(1:),3," ")) 
  pre     = stringtofloat(str_get_field(f(1:),4," ")) 
  npts    = numAsciiRow(filepath)-1 ;获取行数-站点数
  ;设置缺测值
  pre@_FillValue = 32700.

;创建存放插值后生成数据的数组 在北纬26-40，东经74-105这个矩形框内插值
  mlon=311
  mlat=141

  olon=fspan(74, 105, mlon)
  olat=fspan(26, 40, mlat)
  data = new((/mlat,mlon/),"float")

;2.设置数组属性，为了符合netcdf规定的数据格式，使函数能够识别经纬度
  olon!0          = "lon"
  olon@long_name  = "lon"
  olon@units      = "degrees_east"
  olon&lon        = olon

  olat!0          = "lat"
  olat@long_name  = "lat"
  olat@units      = "degrees_north"
  olat&lat        = olat

;3.调用插值函数

  pre@_FillValue =  9.96921e+36  
  rscan = (/2,1,0.1/)   ;连续的有效半径大小，最大为10，依次递减
  data  = obj_anal_ic_Wrap(lon,lat,pre,olon,olat,rscan, False)  ;Cressman插值

;4.---Attach the coordinate arrays
  data!0    = "lat"
  data!1    = "lon"
  data&lat  = olat
  data&lon  = olon

; ;mask掉高原以外的vapdiv
  shp_filename  ="/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Polygon.shp" 
  data_mask =new(dimsizes(data),typeof(data),data@_FillValue)
  data_mask =shapefile_mask_data(data,shp_filename,True) 

  ;printVarSummary(data1)

  ;printMinMax(data, 0)
  ;print(data({28},{92}))
  ;exit
  ; fill_value in data
  ;oned_data = ndtooned(R)
  ;data_check = dimsizes(ind(ismissing(oned_data).eq.True)) ; 
  ;print("fill_values' number in data1:")
  ;print(data_check) ;将缺测赋值为0后是1，未处理缺测值是3255



wks = gsn_open_wks("x11", pic_dir+"intpl_pre"+filename)

;-------------------属性设置----------------------------------------------------
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

  res@mpMinLatF             = 26.
  res@mpMaxLatF             = 40.
  res@mpMinLonF             = 74
  res@mpMaxLonF             = 105
  res@gsnMajorLonSpacing    =5. 
  res@gsnMinorLonSpacing    =1.    
  res@gsnMajorLatSpacing    =5. 
  res@gsnMinorLatSpacing    =1

  res@mpFillOn=False

  res@mpDataBaseVersion       = "MediumRes"
  res@mpDataSetName           =  "/mnt/h/d/ChinaMap/Earth..4"
  res@mpOutlineSpecifiers     = (/"China:states"/)
  ;边界线
  ; res@mpOutlineBoundarySets   = "National"

  ;等值线
  ;画等值线图
  cnres = res
  cnres@cnFillOn = True  ;cn means ContourPlot
  cnres@cnLinesOn = False   
  colors  = (/"white","deepskyblue","palegreen1","gold",\
             "lightcoral","orangered","red4"/)
  cnres@cnFillPalette = colors
  cnres@cnLineLabelsOn = False   
  cnres@cnInfoLabelOn = False ; set false will not set an information label
  cnres@cnLevelSelectionMode = "ExplicitLevels" 
  cnres@cnLevels =(/0.1,2.5,5.,10.,20.,30./)
  cnres@cnLineLabelFormat="0@;*.3f" ;labelbar的数值格式

  cnres@lbBoxLinesOn = True ; Label bar
  cnres@pmLabelBarHeightF = 0.08    ;色标变细
  cnres@pmLabelBarOrthogonalPosF=0.15
  cnres@lbBoxEndCapStyle = "TriangleBothEnds"

;绘图
  data= smth9_Wrap(data,0.5,0.25,False)
  plot = gsn_csm_contour_map(wks,data_mask,cnres) 

;高原轮廓线
  shp_line = "/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Line.shp" 
  lnres                  = True     
  lnres@gsLineColor      ="orange"
  lnres@gsLineThicknessF = 4.0           ; 6x thickness          ; 6x thickness  
  shp_plot               = gsn_add_shapefile_polylines(wks,plot,shp_line,\
                                                       lnres)
draw(plot)
frame(wks)
end
