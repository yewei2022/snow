;mask掉高原以外站点，输出高原站号，写入文件
;文件读取方式参考 http://www.ncl.ucar.edu/Applications/list_io.shtml
;写入文件参考 http://www.ncl.ucar.edu/Applications/write_ascii.shtml 
;  ncl /mnt/f/snow_related/code/by_ncl/TP_sta_pick.ncl


load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
;--------------------读站点数据--------
  filepath = "/mnt/f/snow_sts_data/sta_info.txt"  ;参数文件路径 初筛的40年长度的900+站点
  f       = asciiread(filepath,-1,"string")
  sta_all = stringtointeger(str_get_field(f(1:),1,",")) 
  lat     = stringtofloat(str_get_field(f(1:),3,",")) 
  lon     = stringtofloat(str_get_field(f(1:),2,","))

 ;设置缺测值，mask掉高原以外的站点
  sta_all@_FillValue = 999999
  ;注意：这里的txt文件最后一行数据下面需要空白行，才能读出文件的正确行数
  ;大多数txt文件都满足要求，但还是需要核实一下
  npts = numAsciiRow(filepath)-1 ;获取行数-站点数
  ; print(npts)
  ; exit

  ;---Open shapefile and read Mississippi River Basin lat/lon values.
  f1      = addfile("/mnt/f/snow_sts_data/TPshp/DBATP/DBATP_Polygon.shp", "r") ;Polygon Line

  ; Polygon 和 Line 画出来的线条是一致的，但得出的站点数不一致，既然如此
  ;挑选站点用Polygon 吧 站点数更多
  ; 用Polygon 和 Line 分别做数据的mask时，Polygon 才能画出正确的图

  ; f1      = addfile("/mnt/f/snow_sts_data/TPshp/TPBoundary2021/TPBoundary_new(2021).shp", "r")
  mrb_lon = f1->x
  mrb_lat = f1->y
  ;---Start with data all missing
  sta = new(dimsizes(sta_all),typeof(sta_all),sta_all@_FillValue)
  do i=0,npts-1
    sta(i)=where(gc_inout(lat(i),lon(i),mrb_lat,mrb_lon), sta_all(i), sta_all@_FillValue)
  end do

;输出高原站数和站号
  ; nmsg = num(.not.ismissing(sta))   ; count number of missing
  ; tp_sta=new(nmsg,integer)
  ista = ind(.not.ismissing(sta))
  tp_sta = sta(ista)
  asciiwrite("/mnt/f/snow_sts_data/TP_sta_by2014.txt",tp_sta)   

end     
 

