; 计算地形强迫抬升速度 Wf 并写入bin文件
; 中途有一些没有必要的时间转换 时间处理

load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"
load "/mnt/f/snow_related/code/by_ncl/codebefore/RTC/create_netcdf_file_utils.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/calendar_decode2.ncl"

;  ncl /mnt/f/snow_related/code/by_ncl/write_wf.ncl

begin

;1.读取数据
  ;1.1 变量数据
  data_dir = "/mnt/f/snow_sts_data/ERA5/deal/" 
  data_u    = addfile(data_dir+"u100_alltcdays.nc", "r") 
  data_v    = addfile(data_dir+"v100_alltcdays.nc", "r") 

  u_in     = data_u ->u100(:,{25:40},{70:105})
  v_in     = data_v ->v100(:,{25:40},{70:105})
  ; printVarSummary(u_in)
  ; print(u_in&time)

  ; ; =======================时间处理 非必要 只是想能成功写进nc文件 失败==================
  ; timeset      = data_u->time
  ; time0        = tointeger(timeset)
  ; time0@units  =  "days since 1981-10-25 00:00:0.0"
  ; ; printVarSummary(timeset)

  ; ; ; 首先 把 "proleptic_gregorian"转换为"standard" 时间
  ; ; ; 为啥呢 因为写入nc文件时NCL转换不了时间会报错 argument type mismatch
  ; ; ; 但是最后也没成功啊
  ; utc_date = cd_calendar(time0, 0)
  ; ; printVarSummary(utc_date)

  ; ; YYYYMMDDHH_f!0 = "time"

  ; ;  再把 "standard"转换为"gregorian" 时间
  ; year   = tointeger(utc_date(:,0))   
  ; month  = tointeger(utc_date(:,1))   
  ; day    = tointeger(utc_date(:,2))   
  ; hour   = tointeger(utc_date(:,3))   
  ; minute = tointeger(utc_date(:,4))   
  ; second = utc_date(:,5)
  ; option = 0
  ; option@return_type = "integer"
  ; option@calendar =   "gregorian"  
  ; grg_date = cd_inv_calendar(year,month,day,hour,minute,second,time0@units, option)
  ; ; printVarSummary(grg_date)

  ; ; 赋给u_in
  ; u_in&time    =   grg_date
  ; printVarSummary(u_in&time)
  ; copy_VarCoords(u_in, v_in)

  ; ; path_format = "%Y%N%D%H"   ; YYYYMMMDDHH
  ; ; time  = cd_string(timeset_ymdh,path_format) ;只能对一个时间标量
  ; ; printVarSummary(timeset_ymdh)
  ; ; ==============================================================================

  ;1.2 地形数据
  topo        = addfile("/mnt/d/case/data/other/ETOPO2v2c_f4.nc", "r")
  elev0        = topo->z({0:50},{70:110}) 
  ; printVarSummary(elev0)
  ; exit 
  lon_topo    = topo->x({70:110}) 
  lat_topo    = topo->y({0:50}) 
  lat_topo!0     = "lat"
  lon_topo!0     = "lon"
  lat_topo@units = "degrees_north"
  lon_topo@units = "degrees_east"
  lat_topo&lat   = lat_topo
  lon_topo&lon   = lon_topo

  ;---Attach the coordinate arrays
  elev0!0    = "lat"
  elev0!1    = "lon"
  elev0&lat  = lat_topo
  elev0&lon  = lon_topo


  ;将水平速度插值成和地形相同分辨率
  elev=elev0({25:40},{70:105})

  printVarSummary(elev)
  ;  清内存
  delete([/data_u,data_v,elev0/])

  lon_in =u_in&longitude
  lat_in =u_in&latitude
  lon_out=elev&lon
  lat_out=elev&lat
  u     =linint2_Wrap(lon_in, lat_in, u_in, False, lon_out, lat_out, 0)
  delete(u_in)
  v     =linint2_Wrap(lon_in, lat_in, v_in, False, lon_out, lat_out, 0)
  delete(v_in) 


  ; printVarSummary(u)

; ;2 数据处理 
;; 地形梯度
  nlat=dimsizes(elev&lat)
  mlon=dimsizes(elev&lon)
  lat    =elev&lat
  lon    =elev&lon

  dlon   = (lon(2)-lon(1))*0.0174533 ; convert to radians 0.017=3.14/180
  dHdX   = new ( dimsizes(elev),typeof(elev)); pre-allocate space
  copy_VarCoords(elev, dHdX)
  do nl=0,nlat-1                      ; loop over each latitude
  dX = 6378388.*cos(0.0174533*lat(nl))*dlon  ; constant at this latitude
  dHdX(nl:nl,:) = center_finite_diff_n (elev(nl:nl,:), dX , False,0,1) ; 1指的经度那一维
  end do

  dY   =(lat(2)-lat(1))*6378388.*0.0174533 ;标量
  dHdY = new ( dimsizes(elev),typeof(elev)); pre-allocate space
  copy_VarCoords(elev, dHdY)
  dHdY= center_finite_diff_n (elev, dY , False,0,0)

  wf_all = u*conform(u, dHdX, (/1,2/)) + v*conform(v, dHdY, (/1,2/))
  copy_VarCoords(u,wf_all) ; 拷贝除了time以外的坐标信息

  ; ; printVarSummary(wf_all)
  ; printVarSummary(wf_all)
  ; print(wf_all(0,1,2)) ;测试python读取的输出文件数据是否保真


; ; 写入二进制文件 记得把原文件删掉 不然运行一次接着写入一次
  fout_name = "/mnt/f/snow_sts_data/ERA5/deal/wf_alltcdays.bin"
  print("--------------------------------------")
  print("start writing output files: " + fout_name + " ......")
  fbindirwrite (fout_name, wf_all) 
  print("finish writing output files: " + fout_name + " ......")
  print("--------------------------------------")


end