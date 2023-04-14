load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "G:/wrfchem_emission/anthro/1-Global/regrid/input/calculate_zone.ncl"

begin
;datadir = "/vol6/home/luoyl/guojx/chem_emiss/czhao_emis_proc/anthro/anthro_emis/edgar_HTAP_2010/"
datadir = "G:/wrfchem_emission/anthro/anthro_emis/edgar_HTAP_2010/"
filehead = "edgar_HTAP_"

category=(/"AGRICULTURE","AIR","ENERGY","INDUSTRY","RESIDENTIAL","TRANSPORT","SHIPS"/)
cyear = 2010
cmon = ispan(1,12,1)


nspec=10
;0-NH3, 1-CO, 2-NOx, 3-SO2, 4-BC, 5-OC, 6-PM25, 7-PM10, 8-SO4, 9-NO3   ;挥发性有机物的在另外一个文件里面处理

;from Qiang Zhang for Asia to convert PM2.5 to SO4 and NO3  ; SO4 and NO3是转换来的，原来的edgar_HTAP数据集里没有
;so4=0.119*industry+0.05*power+0.0187*transport
;no3=0.00395*transport



do im=5,5
cmon1 = sprinti("%0.2i",im)   ;sprinti的作用：把整形变为有格式字符串
print("start processing mon_"+cmon1+" ......")
fout = datadir+"anthro_primary_power_2010"+cmon1+".bin"
system("rm -f " + fout)
;--------------------------
;Agriculture NH3              Agriculture里只有NH3这一种，没有其他的化学种类
;--------------------------
dfactor = new(24,"float")     ;new:新建一个变量
dfactor = 1.    ;global的NH3没有日变化

ic = 0
var0 := "NH3"
var := "emi_nh3"
filename := filehead+"emi_"+category(ic)+"/"+filehead+var0+"_emi_"+category(ic)+"_"+cyear+"_"+cmon(0)+".0.1x0.1.nc"

f = addfile(datadir+filename, "r")
lat1d = f->lat ;read lat, lon
lon1d = f->lon

nx = dimsizes(lon1d) ;在这里nx=3600
ny = dimsizes(lat1d) ;ny=1800

d_time1d = calculate_zone(nx,lon1d) ;local time, d_time1d(nx)
dfactor2d = calculate_dfactor(d_time1d,dfactor) ; dfactor2d(nx,24)   ;calculate_zone计算的是时区，dfactor2d计算当地时间所对应的系数dfactor，相同经向格点上的当地时间相同

emission_low = new((/24,nspec,ny,nx/),"float")  ;here, 24 is UTC hour, ny=1800,nx=3600
emission_low = 0.
emission_mid = emission_low
emission_high = emission_low

filename=filehead+"emi_"+category(ic)+"/"+filehead+var0+"_emi_"+category(ic)+"_"+cyear+"_"+cmon(im-1)+".0.1x0.1.nc"
f = addfile(datadir+filename, "r")

emi_nh3 := f->$var$     ;变量名emi_nh3代表的是文件中的emi_nh3变量

emi_nh3 = emi_nh3*1000.0*1.e6*3600.0 ;kg/m^2/s to g/km^2/hr
emi_nh3 = emi_nh3/17.0  ;g/km^2/hr to mole/km^2/hr
;printVarSummary(emi_nh3)            ;输出变量信息
;printVarSummary(dfactor2d)
;printVarSummary(emission_low)

do ih=0,23
 emission_low(ih,0,:,:) = emission_low(ih,0,:,:) + emi_nh3*conform(emi_nh3,dfactor2d(:,ih),1) ;emi_nh3(ny,nx),dfactor2d(:,ih)这里是nx(3600)个,conform就是把dfactor2d(:,ih)重复ny遍
                                                                ;函数处理后变量为conform_dfactor2d(ny,nx),不论ny这一维等于几，nx这一维的向量是一样的
end do
;print("guojx,"+emission_low(23,1,1319,2720)) ;guojx debug
print("23 hr,nh3,104.05E,20.05N "+emission_low(23,0,1040,1100)) ;guojx debug


;求多维数组emission_low的最大值
emission_low_one_d=ndtooned(emission_low) ;先转为一维
max_emission_low_one_d=max(emission_low_one_d) ;最大值
max_emission_low_one_d_ind=maxind(emission_low_one_d) ;最大值所在1维数组的位置
;最大值对应多维数组种的位置
max_ih=floor(max_emission_low_one_d_ind*1.0/(nspec*ny*nx))
max_nspec=floor(mod(max_emission_low_one_d_ind,(nspec*ny*nx))*1.0/(ny*nx)) 
max_ny=floor(mod(mod(max_emission_low_one_d_ind,(nspec*ny*nx)), ny*nx)*1.0/nx)
max_nx=mod(mod(mod(max_emission_low_one_d_ind,(nspec*ny*nx)), ny*nx),nx)

;输出 在这里经度点0-3600对应0.05-359.95，是从0度开始的，不是从西经-180开始
print(max_ih)
print(max_nspec)
print(max_ny)
print(max_nx)

print("finish reading Agriculture")

fbindirwrite(datadir+cyear+"_"+cmon(im-1)+"_00hr"+"_agriculture_nh3.bin", emission_low(0,0,:,:))  ;ncl输出，储存顺序是先变最右边的


;--------------------------
;Aircraft
;--------------------------
ic = 1        ;这里air没有日变化
var0 := (/"CO","NOx","SO2","BC","OC","PM2.5","PM10"/)
var := (/"emi_co","emi_nox","emi_so2","emi_bc","emi_oc","emi_pm2.5","emi_pm10"/)
wgt := (/28,46,64/)  ;三种气体的分子质量：C=12,N-14,S=32
time=(/"LTO","CDS","CRS"/)  ;time是三个不同的飞行阶段
;LTO=Landing&Takeoff,  CDS=Climbing&Descent, CRS=Cruise

do it=0,2
do is=0,6  ;种类
filename = filehead+"emi_"+category(ic)+"/"+filehead+"emi_"+var0(is)+"_"+category(ic)+"_"+time(it)+"_"+cyear+".0.1x0.1.nc"
f = addfile(datadir+filename, "r")
data0 := f->$var(is)$
if(is.le.2)then ;gas 3 species
  data0 = data0*1000.0*1.e6*3600.0 ;kg/m^2/s to g/km^2/hr
  data0 = data0/wgt(is) ;g/km^2/hr to mole/km^2/hr
else ;aerosol 4 species
  data0 = data0*1.e9   ;kg/m2/s to ug/m2/s
end if
if(is.eq.3)then
  bc := data0
end if
if(is.eq.4)then
  oc := data0
end if
if(is.eq.5)then
  pm25 := data0
  data0 = data0 - bc - oc ;remove OC,BC from PM25 to get unspeciated PM2.5
  data0 = where(data0.lt.0.,0.,data0)
end if
if(is.eq.6)then
  data0 = data0 - pm25 ;remove PM25 from PM10 to get unspeciated PM10
  data0 = where(data0.lt.0.,0.,data0)
end if

do ih=0,23
  if(it.eq.0)then
    emission_low(ih,is+1,:,:) = emission_low(ih,is+1,:,:) + data0*conform(data0,dfactor2d(:,ih),1)
  end if
  if(it.eq.1)then
    emission_mid(ih,is+1,:,:) = emission_mid(ih,is+1,:,:) + data0*conform(data0,dfactor2d(:,ih),1)
  end if
  if(it.eq.2)then
    emission_high(ih,is+1,:,:) = emission_high(ih,is+1,:,:) + data0*conform(data0,dfactor2d(:,ih),1)  ;	AIR里没有NH3,is要加1才能位置对应
  end if
end do ; ih

end do ;is
end do ;it
;print("guojx,"+emission_low(23,1,1319,2720)) ;guojx debug


print("finish reading Aircraft")

;--------------------------
;ENERGY
;--------------------------
dfactor=(/0.0366,0.0327,0.0299,0.0299,0.0293,0.0309,0.033,0.0385,0.045,0.0498,0.0508,0.0506,0.0509,\
          0.0488,0.0476,0.0474,0.0472,0.0454,0.0447,0.0431,0.0427,0.0427,0.0423,0.0403/)
dfactor=dfactor*24.
dfactor2d = calculate_dfactor(d_time1d,dfactor) ; dfactor2d(nx,24)

ic = 2
var0 := (/"NH3","CO","NOx","SO2","BC","OC","PM2.5","PM10"/)
var := (/"emi_nh3","emi_co","emi_nox","emi_so2","emi_bc","emi_oc","emi_pm2.5","emi_pm10"/)
;wgt=[17,28,30,64]
wgt := (/17,28,46,64/)   ;energy有NH3，质量17

do is=0,7
filename = filehead+"emi_"+category(ic)+"/"+filehead+var0(is)+"_emi_"+category(ic)+"_"+cyear+"_"+cmon(im-1)+".0.1x0.1.nc"
f = addfile(datadir+filename, "r")
data0 := f->$var(is)$ ;kg m-2 s-1

if(is.le.3)then ;gas 前4种
  data0 = data0*1000.0*1.e6*3600.0 ;kg/m^2/s to g/km^2/hr
  data0 = data0/wgt(is) ;g/km^2/hr to mole/km^2/hr
else ;aerosol
  data0 = data0*1.e9   ;kg/m2/s to ug/m2/s
end if
if(is.eq.4)then
  bc := data0
end if
if(is.eq.5)then
  oc := data0
end if
if(is.eq.6)then
  pm25 := data0
  data0 = data0-bc-oc ;remove OC,BC from PM25 to get unspeciated PM2.5
  data0 = where(data0.lt.0.,0.,data0)
end if
if(is.eq.7)then
  data0 = data0-pm25 ;remove PM25 from PM10 to get unspeciated PM10
  data0 = where(data0.lt.0.,0.,data0)
end if

do ih=0,23
  emission_low(ih,is,:,:) = emission_low(ih,is,:,:) + data0*conform(data0,dfactor2d(:,ih),1)
end do
end do ;is

;for SO4 and NO3    没有直接的数据
so4=0.05*pm25 ;按照PM25转换的话，单位应该一样，也是ug/m2/s
no3 = 0.0
do ih=0,23
  emission_low(ih,8,:,:) = emission_low(ih,8,:,:) + so4*conform(data0,dfactor2d(:,ih),1)
  emission_low(ih,9,:,:) = emission_low(ih,9,:,:) + no3*conform(data0,dfactor2d(:,ih),1)
  emission_low(ih,6,:,:) = emission_low(ih,6,:,:) - (so4+no3)*conform(data0,dfactor2d(:,ih),1) ;further remove so4 and no3，6是PM25
end do
;print("guojx,"+emission_low(23,1,1319,2720)) ;guojx debug
print("finish reading Energy")

;--------------------------
;Industry
;--------------------------
dfactor = (/0.0312,0.0312,0.0312,0.0324,0.0343,0.037,0.0398,0.0429,0.0454,0.0485,0.0508,0.053,0.0543,\
          0.0508,0.0516,0.0519,0.0483,0.0451,0.042,0.0393,0.0374,0.0354,0.0338,0.0324/)
dfactor = dfactor*24.
dfactor2d = calculate_dfactor(d_time1d,dfactor) ; dfactor2d(nx,24)

ic = 3
var0 := (/"NH3","CO","NOx","SO2","BC","OC","PM2.5","PM10"/)
var := (/"emi_nh3","emi_co","emi_nox","emi_so2","emi_bc","emi_oc","emi_pm2.5","emi_pm10"/)
;wgt=[17,28,30,64]
wgt := (/17,28,46,64/)  ;分别是 "NH3","CO","NOx","SO2"

do is=0,7
filename = filehead+"emi_"+category(ic)+"/"+filehead+var0(is)+"_emi_"+category(ic)+"_"+cyear+"_"+cmon(im-1)+".0.1x0.1.nc"
f = addfile(datadir+filename, "r")
data0 := f->$var(is)$ ;kg m-2 s-1

if(is.le.3)then ;gas
  data0 = data0*1000.0*1.e6*3600.0 ;kg/m^2/s to g/km^2/hr
  data0 = data0/wgt(is) ;g/km^2/hr to mole/km^2/hr
else ;aerosol
  data0 = data0*1.e9   ;kg/m2/s to ug/m2/s
end if
if(is.eq.4)then
  bc := data0
end if
if(is.eq.5)then
  oc := data0
end if
if(is.eq.6)then
  pm25 := data0
  data0 = data0-bc-oc ;remove OC,BC from PM25 to get unspeciated PM2.5
  data0 = where(data0.lt.0.,0.,data0)
end if
if(is.eq.7)then
  data0 = data0-pm25 ;remove PM25 from PM10 to get unspeciated PM10
  data0 = where(data0.lt.0.,0.,data0)
end if

do ih=0,23
  emission_low(ih,is,:,:) = emission_low(ih,is,:,:) + data0*conform(data0,dfactor2d(:,ih),1)
end do
end do ;is

;for SO4 and NO3
;so4=0.119*pm25
so4 := 0.01*pm25  ;adjust so4 direct emission
no3 = 0.0
do ih=0,23
  emission_low(ih,8,:,:) = emission_low(ih,8,:,:) + so4*conform(data0,dfactor2d(:,ih),1)
  emission_low(ih,9,:,:) = emission_low(ih,9,:,:) + no3*conform(data0,dfactor2d(:,ih),1)
  emission_low(ih,6,:,:) = emission_low(ih,6,:,:) - (so4+no3)*conform(data0,dfactor2d(:,ih),1) ;further remove so4 and no3
end do
;print("guojx,"+emission_low(23,1,1319,2720)) ;guojx debug
print("finish reading Industry")

;--------------------------
;RESIDENTIAL
;--------------------------
dfactor = (/0.0176,0.0157,0.0149,0.015,0.0149,0.0154,0.0208,0.0497,0.0638,0.0655,0.065,0.0566,0.0481,0.0447,\
            0.0442,0.0418,0.0408,0.0415,0.0466,0.0592,0.0627,0.0577,0.0566,0.0412/)
dfactor = dfactor*24. 
dfactor2d = calculate_dfactor(d_time1d,dfactor) ; dfactor2d(nx,24)

ic = 4
var0 := (/"NH3","CO","NOx","SO2","BC","OC","PM2.5","PM10"/)
var := (/"emi_nh3","emi_co","emi_nox","emi_so2","emi_bc","emi_oc","emi_pm2.5","emi_pm10"/)
;wgt=[17,28,30,64]
wgt := (/17,28,46,64/)

do is=0,7
filename = filehead+"emi_"+category(ic)+"/"+filehead+var0(is)+"_emi_"+category(ic)+"_"+cyear+"_"+cmon(im-1)+".0.1x0.1.nc"
f = addfile(datadir+filename, "r")
data0 := f->$var(is)$ ;kg m-2 s-1

if(is.le.3)then ;gas
  data0 = data0*1000.0*1.e6*3600.0 ;kg/m^2/s to g/km^2/hr
  data0 = data0/wgt(is) ;g/km^2/hr to mole/km^2/hr
else ;aerosol
  data0 = data0*1.e9   ;kg/m2/s to ug/m2/s
end if
if(is.eq.4)then
  bc := data0
end if
if(is.eq.5)then
  oc := data0
end if
if(is.eq.6)then
  pm25 := data0
  data0 = data0-bc-oc ;remove OC,BC from PM25 to get unspeciated PM2.5
  data0 = where(data0.lt.0.,0.,data0)
end if
if(is.eq.7)then
  data0 = data0-pm25 ;remove PM25 from PM10 to get unspeciated PM10
  data0 = where(data0.lt.0.,0.,data0) ;where函数，data0中小于0的输出0，大于0的输出data0
end if

do ih=0,23
  emission_low(ih,is,:,:) = emission_low(ih,is,:,:) + data0*conform(data0,dfactor2d(:,ih),1)
end do
end do ;is

;for SO4 and NO3
so4 = 0.0  ;adjust so4 direct emission
no3 = 0.0
do ih=0,23
  emission_low(ih,8,:,:) = emission_low(ih,8,:,:) + so4*conform(data0,dfactor2d(:,ih),1)
  emission_low(ih,9,:,:) = emission_low(ih,9,:,:) + no3*conform(data0,dfactor2d(:,ih),1)
  emission_low(ih,6,:,:) = emission_low(ih,6,:,:) - (so4+no3)*conform(data0,dfactor2d(:,ih),1) ;further remove so4 and no3
end do
;print("guojx,"+emission_low(23,1,1319,2720)) ;guojx debug
print("finish reading Residential")

;--------------------------
;Transport
;--------------------------
dfactor01 = (/0.0165,0.0131,0.0101,0.0085,0.0081,0.0088,0.0132,0.0185,0.0266,0.0365,0.0483,0.0587,\
            0.0663,0.0737,0.0753,0.076,0.0761,0.0752,0.07,0.0642,0.0537,0.0434,0.0344,0.0249/)
dfactor02 = (/0.0238,0.0231,0.0219,0.0215,0.0215,0.0223,0.0261,0.0323,0.0405,0.0459,0.053,0.0573,\
            0.06,0.061,0.0612,0.0605,0.0597,0.0573,0.0548,0.0504,0.0447,0.0389,0.0339,0.0283/)
dfactor = (dfactor01+dfactor02)/2.0
dfactor = dfactor*24.
dfactor2d = calculate_dfactor(d_time1d,dfactor) ; dfactor2d(nx,24)

ic = 5
var0 := (/"NH3","CO","NOx","SO2","BC","OC","PM2.5","PM10"/)
var := (/"emi_nh3","emi_co","emi_nox","emi_so2","emi_bc","emi_oc","emi_pm2.5","emi_pm10"/)
;wgt=[17,28,30,64]
wgt := (/17,28,46,64/)

do is=0,7
filename = filehead+"emi_"+category(ic)+"/"+filehead+var0(is)+"_emi_"+category(ic)+"_"+cyear+"_"+cmon(im-1)+".0.1x0.1.nc"
f = addfile(datadir+filename, "r")
data0 := f->$var(is)$ ;kg m-2 s-1

if(is.le.3)then ;gas
  data0 = data0*1000.0*1.e6*3600.0 ;kg/m^2/s to g/km^2/hr
  data0 = data0/wgt(is) ;g/km^2/hr to mole/km^2/hr
else ;aerosol
  data0 = data0*1.e9   ;kg/m2/s to ug/m2/s
end if
if(is.eq.4)then
  bc := data0
end if
if(is.eq.5)then
  oc := data0
end if
if(is.eq.6)then
  pm25 := data0
  data0 = data0-bc-oc ;remove OC,BC from PM25 to get unspeciated PM2.5
  data0 = where(data0.lt.0.,0.,data0)
end if
if(is.eq.7)then
  data0 = data0-pm25 ;remove PM25 from PM10 to get unspeciated PM10
  data0 = where(data0.lt.0.,0.,data0)
end if

do ih=0,23
  emission_low(ih,is,:,:) = emission_low(ih,is,:,:) + data0*conform(data0,dfactor2d(:,ih),1)
end do
end do ;is

;for SO4 and NO3
;so4=0.0187*pm25
so4 := 0.001*pm25   ; adjust direct so4 emission
;no3=0.00395*pm25
no3 := 0.001*pm25  ;adjust direct no3 emission   按照PM25转换的话，单位应该一样，也是ug/m2/s
do ih=0,23
  emission_low(ih,8,:,:) = emission_low(ih,8,:,:) + so4*conform(data0,dfactor2d(:,ih),1)
  emission_low(ih,9,:,:) = emission_low(ih,9,:,:) + no3*conform(data0,dfactor2d(:,ih),1)
  emission_low(ih,6,:,:) = emission_low(ih,6,:,:) - (so4+no3)*conform(data0,dfactor2d(:,ih),1) ;further remove so4 and no3
end do
;print("guojx,"+emission_low(23,1,1319,2720)) ;guojx debug
print("finish reading Transport")
;--------------------------
;Ships
;--------------------------
dfactor = 1.
dfactor2d = calculate_dfactor(d_time1d,dfactor) ; dfactor2d(nx,24)

ic = 6
var0 := (/"CO","NOx","SO2","BC","OC","PM2.5","PM10"/)
var := (/"emi_co","emi_nox","emi_so2","emi_bc","emi_oc","emi_pm2.5","emi_pm10"/)
wgt := (/28,46,64/)

do is=0,6
filename = filehead+"emi_"+category(ic)+"/"+filehead+var0(is)+"_emi_"+category(ic)+"_"+cyear+".0.1x0.1.nc"
f = addfile(datadir+filename, "r")
data0 := f->$var(is)$ ;kg m-2 s-1

if(is.le.2)then ;gas
  data0 = data0*1000.0*1.e6*3600.0 ;kg/m^2/s to g/km^2/hr
  data0 = data0/wgt(is) ;g/km^2/hr to mole/km^2/hr
else ;aerosol
  data0 = data0*1.e9   ;kg/m2/s to ug/m2/s
end if
if(is.eq.3)then
  bc := data0
end if
if(is.eq.4)then
  oc := data0
end if
if(is.eq.5)then
  pm25 := data0
  data0 = data0-bc-oc ;remove OC,BC from PM25 to get unspeciated PM2.5
  data0 = where(data0.lt.0.,0.,data0)
end if
if(is.eq.6)then
  data0 = data0-pm25 ;remove PM25 from PM10 to get unspeciated PM10
  data0 = where(data0.lt.0.,0.,data0)
end if

do ih=0,23
  emission_low(ih,is+1,:,:) = emission_low(ih,is+1,:,:) + data0*conform(data0,dfactor2d(:,ih),1)
end do
end do ;is
;print("guojx,"+emission_low(23,1,1319,2720)) ;guojx debug
print("finish reading Ships")
print("--------------------------------------")
print("start writing output files: " + fout + " ......")
;system("rm -f " + fout) ;guojx, debug, why the "rm -f" do not work if I put here????
fbindirwrite(fout, lon1d) ; jxguo, only fbindirwrite could write a file over than 2Gb
fbindirwrite(fout, lat1d)
fbindirwrite(fout, emission_low) ;输出无格式二进制数据，其方式等同于fortran的“form=unformatted, access=direct, recl=..”
fbindirwrite(fout, emission_mid)  ;ncl输出，储存顺序是先变最右边的维数
fbindirwrite(fout, emission_high)  ;前4种是气体，单位是mole/km^2/hr ，后6种是aerosol,单位是ug/m2/s
delete(emission_low)
delete(emission_mid)
delete(emission_high)
print("finish writing output files: " + fout + " ......")
print("--------------------------------------")
end do;im

end
