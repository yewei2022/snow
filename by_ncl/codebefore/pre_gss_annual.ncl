;绘制总的、以及风暴影响下的 降水量、gss年变化
;纵向排列4条y轴
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;https://geocat-examples.readthedocs.io/en/latest/gallery/Scatter/NCL_scatter_5.html#sphx-glr-gallery-scatter-ncl-scatter-5-py
;  ncl /mnt/f/snow_related/code/by_ncl/snow_all/pre_gss_annual.ncl

; xy_19.ncl
; These files are loaded by default in NCL V6.2.0 and newer
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
;---Generate random data with an average of 10 and a stddev of 3.
  pic_dir ="/mnt/f/snow_related/pic/snow_all/"

  file_dir1="/mnt/f/snow_sts_data/1981-2020/snow_amt_annual_all.txt"
  f1       = asciiread(file_dir1,-1,"string")
  year     = stringtointeger(str_get_field(f1(1:),1," ")) 
  amts_all = stringtofloat(str_get_field(f1(1:),2," ")) 

  amts_all_rc =  regline_stats(year,amts_all) ; linear regression coef
  npts    = dimsizes(amts_all)
  amts_all_arry = new ( (/2,npts/), float)
  amts_all_arry(0,:) = amts_all                                 ; use markers
  amts_all_arry(1,:) = amts_all_rc@Yest
  ;显著性检验
  siglvl = 0.05            ; a-priori specified sig level
  amts_all_pr     = rtest(amts_all_rc@bstd(1), amts_all_rc@N, 0)    ; ===> pr=0.041
  if (amts_all_pr.lt.siglvl) then
      print("significant")
  else
      print("NOT significant")
  end if
  print("总降水量系数"+amts_all_rc@b(1))

  file_dir2="/mnt/f/snow_sts_data/1981-2020/snow_gss_annual_all.txt"
  f2       = asciiread(file_dir2,-1,"string")
  gss_all  = stringtofloat(str_get_field(f2(1:),2," "))

  gss_all_rc =  regline_stats(year,gss_all) ; linear regression coef
  gss_all_arry = new ( (/2,npts/), float)
  gss_all_arry(0,:) = gss_all                                 ; use markers
  gss_all_arry(1,:) = gss_all_rc@Yest
  ;显著性检验
  gss_all_pr     = rtest(gss_all_rc@bstd(1), gss_all_rc@N, 0)    ; ===> pr=0.041
  if (gss_all_pr.lt.siglvl) then
      print("significant")
  else
      print("NOT significant")
  end if 
  print("总积雪系数"+gss_all_rc@b(1))

  file_dir3="/mnt/f/snow_sts_data/1981-2020/snow_amt_annual.txt"
  f3       = asciiread(file_dir3,-1,"string")
  amts     = stringtofloat(str_get_field(f3(1:),2," "))

  amts_rc =  regline_stats(year,amts) ; linear regression coef
  amts_arry = new ( (/2,npts/), float)
  amts_arry(0,:) = amts                                 ; use markers
  amts_arry(1,:) = amts_rc@Yest
  ;显著性检验
  amts_pr     = rtest(amts_rc@bstd(1), amts_rc@N, 0)    ; ===> pr=0.041
  if (amts_pr.lt.siglvl) then
      print("significant")
  else
      print("NOT significant")
  end if 
  print("风暴降水量系数"+amts_rc@b(1))

  file_dir4="/mnt/f/snow_sts_data/1981-2020/snow_gss_annual.txt"
  f4       = asciiread(file_dir4,-1,"string")
  gss      = stringtofloat(str_get_field(f4(1:),2," "))

  gss_rc =  regline_stats(year,gss) ; linear regression coef
  gss_arry = new ( (/2,npts/), float)
  gss_arry(0,:) = gss                                 ; use markers
  gss_arry(1,:) = gss_rc@Yest
  ;显著性检验
  gss_pr     = rtest(gss_rc@bstd(1), gss_rc@N, 0)    ; ===> pr=0.041
  if (gss_pr.lt.siglvl) then
      print("significant")
  else
      print("NOT significant")
  end if
  print("风暴积雪系数"+gss_rc@b(1)) 

; print(amts_all)
; print(alldays)

;*********************************
; create plot
;********************************
wks   = gsn_open_wks ("eps", pic_dir+"pre_gss_annual" ) 
plotxy =new(4, graphic)

  gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
  colors=(/5,7/)
  lineDashPattern=(/0,2/)
  amts_max=max(amts)
  amts_all_max=max(amts_all)
  gss_max=max(gss)
  gss_all_max=max(gss_all)

  ;四幅图的共同参数
  res   = True
  res@gsnMaximize = True
  res@gsnDraw  = False
  res@gsnFrame = False
  res@vpHeightF  = 0.1        ; Changes the aspect ratio
  res@vpWidthF   = 0.3
  res@tmXTOn      = False ;关刻度
  res@tmXBLabelAngleF     = 45.   ;
  res@tmXBMode="Manual"   
  res@tmXBTickSpacingF=5
  res@tmXBMinorPerMajor=4 
  res@trXMinF   = 1980       
  res@trXMaxF   = 2021      
  res@xyLineThicknesses =(/5,4/) ;画两条线 
  res@tiYAxisFont =22


  res13=res
  res13@tmYROn      = False
  res13@xyDashPattern=lineDashPattern(0)
  res13@tiYAxisString = "PCP (mm)" ; y-axis label


  res24=res
  ; res24@tmYUseLeft=False ;这个不是必要的
  res24@tiYAxisSide="right"
  res24@tmXTOn               = False
  res24@tmYLOn               = False
  res24@tmYLLabelsOn         = False
  res24@tmYRLabelsOn         = True
  res24@xyDashPattern=lineDashPattern(1) ;虚线
  res24@tiYAxisString = "SDI (cm)" ; y-axis label



  ;分别复制上述共用参数，绘制每个图形
  res1=res13
  res2=res24
  res3=res13
  res4=res24

  res1@xyLineColor=colors(0) ;蓝色，TC影响
  res1@tiYAxisFontColor=colors(0)
  res1@trYMaxF =amts_all_max+1
  plotxy(0)=gsn_csm_xy(wks,year,amts_all_arry,res1)

  res2@xyLineColor=colors(0) ;蓝色，TC影响
  res2@tiYAxisFontColor=colors(0)
  res2@trYMaxF =gss_all_max
  plotxy(1)=gsn_csm_xy(wks,year,gss_all_arry,res2)

  res3@xyLineColor=colors(1) ;蓝色，TC影响
  res3@tiYAxisFontColor=colors(1)
  res3@trYMaxF =amts_max+1
  res3@trYMinF =min(amts)
  plotxy(2)=gsn_csm_xy(wks,year,amts_arry,res3)

  res4@xyLineColor =colors(1) ;绿色，影响
  res4@tiYAxisFontColor=colors(1)
  res4@trYMaxF =gss_max+0.1
  plotxy(3)=gsn_csm_xy(wks,year,gss_arry,res4)

  ;堆叠
  attachres1=True
  attachres1@gsnAttachBorderOn =False
  attachres2=True
  attachres2@gsnAttachPlotsXAxis =True 

attachid1=gsn_attach_plots(plotxy(0), plotxy(1:3), attachres1, attachres2)

draw(plotxy(0))
frame(wks)
; (0)     NOT significant
; (0)     总降水量系数0.00104645
; (0)     significant
; (0)     总积雪系数0.00407373
; (0)     NOT significant
; (0)     风暴降水量系数-0.0553906
; (0)     NOT significant
; (0)     风暴积雪系数-0.0156382
end
 


 

