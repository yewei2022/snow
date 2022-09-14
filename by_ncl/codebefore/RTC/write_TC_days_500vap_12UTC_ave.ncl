;读取组内的TC所有活动日（包含顺延一天) ERA5 500hPa nc资料，
;以UTC12为日界 做日平均 
;计算每日水汽通量和散度 
;选出降雪日再做平均，绘图
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl" 
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/cd_string.ncl"
load "/mnt/d/create_netcdf_file_utils.ncl"

;  ncl /mnt/e/f/snow_related/code/by_ncl/RTC/write_TC_days_500vap_12UTC_ave.ncl

begin

pic_dir  = "/mnt/e/f/snow_related/pic/atmos_env/" 
type_save_name="all_tc_days"
var_save_name="vap500_"
fout_name = "/mnt/f/f/snow_sts_data/RTC/"+var_save_name+type_save_name+".nc"


; ===================计算======================================================
  
  ; 1 read ERA5
  name1=(/"q500","u500","v500"/)
  count:=0
  data_dir0 ="/mnt/f/f/snow_sts_data/ERA5/all/pick/"+name1(count)+"_1.nc" 
  count:=1
  data_dir1 ="/mnt/f/f/snow_sts_data/ERA5/all/pick/"+name1(count)+"_1.nc" 
  count:=2
  data_dir2 ="/mnt/f/f/snow_sts_data/ERA5/all/pick/"+name1(count)+"_1.nc" 

  ; 1 读数据
  data0    = addfile(data_dir0, "r")
  data1    = addfile(data_dir1, "r")
  data2    = addfile(data_dir2, "r")

  q = data0->q(:,{500},:,:)
  u = data1->u(:,{500},:,:)
  v = data2->v(:,{500},:,:)

  ; ;2 以UTC+12的日平均
  time= data0->time
  time=time+12 ;UTC+12
  ; date=cd_string(time, "%Y%N%D%H")
  ; print(date(0:96))
  q&time       = time ;UTC+12赋给变量
  u&time       = time ;UTC+12赋给变量
  v&time       = time ;UTC+12赋给变量

  opt = True
  opt@nval_crit = 4  
  q_Day_mean = calculate_daily_values(q, "avg", 0, opt)
  ; printVarSummary(Day_mean)
  date_mean=cd_string(q_Day_mean&time, "%Y%N%D")
  ; print(date)
  ; u v 同理
  u_Day_mean = calculate_daily_values(u, "avg", 0, opt)
  v_Day_mean = calculate_daily_values(v, "avg", 0, opt)

  ; ; 3 读取TC活动日 挑出TC活动日的日均值
  date_dir_TC ="/mnt/f/f/snow_sts_data/TC/all_tc_days.txt"  ;1025
  datefile_TC = asciiread(date_dir_TC,-1,"string")
  YYYYMMDD_TC = str_get_field(datefile_TC(1:),2," ") 
  date_ind_TC=new(dimsizes(YYYYMMDD_TC), integer)
  do i=0,dimsizes(YYYYMMDD_TC)-1 
  	date_ind_TC(i) =str_match_ind(date_mean, YYYYMMDD_TC(i))
  end do
  ; print(date(date_ind))
  q_need1=q_Day_mean(date_ind_TC,:,:) ;TC日均值
  u_need1=u_Day_mean(date_ind_TC,:,:)
  v_need1=v_Day_mean(date_ind_TC,:,:)

  ; 4 算TC活动日水汽通量和散度
    ;计算水汽通量
    q_need1=q_need1*1000 ;单位变成g/kg
    qu_need1= q_need1*u_need1/9.8
    qv_need1= q_need1*v_need1/9.8
    copy_VarCoords(q_need1,qu_need1)
    copy_VarCoords(q_need1,qv_need1)
    flux=sqrt(qu_need1^2+qv_need1^2) ;水汽通量大小
    copy_VarCoords(q_need1,flux)

    ; ;算散度
    ; div=uv2dv_cfd(qu_need1, qv_need1,qu_need1&latitude,qu_need1&longitude, 2)
    ; copy_VarCoords(qu_need1, div)
    ; div=div*1.e6

    ; 水汽通量距平
    fluxdev  = dim_rmvmean_n_Wrap(flux,0)

    ;TC日合成
    qu_avg=dim_avg_n_Wrap(qu_need1, 0) ;TC日u平均场合成
    qv_avg=dim_avg_n_Wrap(qv_need1, 0) ;TC日v平均场合成
    flux_avg=dim_avg_n_Wrap(flux, 0) ;TC日flux平均场合成

  ;  清内存
  delete([/data0,data1,data2,q,u,v,\
         q_Day_mean,u_Day_mean,v_Day_mean/])

  printVarSummary(qu_avg)
  printVarSummary(qv_avg)
  printVarSummary(flux_avg)

; ====================写入文件=======================================================

    start_write_time = get_cpu_time()

  ;---Set some NetCDF options before we open the file
    setfileoption("nc","preFill",False)
    setfileoption("nc","defineMode",True)

  ; You might need to uncomment this if writing a lot of variables to 
  ; the file, or large variabes.

  ;  setfileoption("nc","Format","NetCDF4")          

  ;---Open a new NetCDF file to write to
    system("rm -f " + fout_name)
    fout = addfile(fout_name,"c")

  ;---Create a bunch of dummy variables with coordinate arrays attached
    nlat =  dimsizes(qu_avg&latitude)
    nlon =  dimsizes(qu_avg&longitude)
    nvars = 3

    lat   = qu_avg&latitude
    lon   = qu_avg&longitude
    data  = new((/nvars,nlat,nlon/),float)
    var_names = "var" + sprinti("%02i",ispan(1,nvars,1))

  ;---Define the dimension names and their sizes on the file
    dims          = (/nlat,nlon/)
    dim_names     = (/lat!0,lon!0/)
    dim_unlimited = (/False,False/)
    filedimdef(fout,dim_names,dims,dim_unlimited)

  ;---Define each variable, its type, its dimension names, and its size
    filevardef(fout,lat!0,typeof(lat),lat!0)
    filevardef(fout,lon!0,typeof(lon),lon!0)
    filevardef(fout,var_names(0),"double",dim_names)
    filevardef(fout,var_names(1),"double",dim_names)
    filevardef(fout,var_names(2),"double",dim_names)

  ;---Define each variable's attributes.
    filevarattdef(fout,lat!0, lat)
    filevarattdef(fout,lon!0, lon)

    fatt = True
    do nv=0,nvars-1
      fatt@long_name = var_names(nv)
      fatt@units     = "units_"+var_names(nv)
      filevarattdef(fout,var_names(nv),fatt)
    end do

  ;---NOW write the variables to the file.
    fout->lat   = (/lat/)
    fout->lon   = (/lon/)
    ; x = create_dummy_var(var_names(0),lat,lon,var_type)
    fout->$var_names(0)$ = flux_avg
    fout->$var_names(1)$ = qu_avg
    fout->$var_names(2)$ = qv_avg

    end_write_time = get_cpu_time()

  ;---Close file. Not necessary, but a good idea.
    delete(fout)

    ;测试
    start_read_time = get_cpu_time()
    fin = addfile(fout_name,"r")
    vnames = getfilevarnames(fin)
    sqsort(vnames)
    do nv=0,dimsizes(vnames)-1
      x := fin->$vnames(nv)$
      print("==================================================")
      printMinMax(x,0)
      print("average = " + avg(x))
    end do
    end_read_time = get_cpu_time()

  ;----------------------------------------------------------------------
  ; Print the timing results.
  ;----------------------------------------------------------------------
    print("==================================================")
    print(get_script_prefix_name() + ".ncl timings")
    print("   Writing file: " + (end_write_time-start_write_time))
    print("   Reading file: " + (end_read_time-start_read_time))
    print("==================================================")


end