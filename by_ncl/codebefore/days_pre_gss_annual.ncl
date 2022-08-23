;绘制总的、以及风暴影响下的降雪日数，pre、gss年变化和线性趋势
;纵向排列6条y轴
;文件读取方式 http://www.ncl.ucar.edu/Applications/list_io.shtml
;https://geocat-examples.readthedocs.io/en/latest/gallery/Scatter/NCL_scatter_5.html#sphx-glr-gallery-scatter-ncl-scatter-5-py
;  ncl /mnt/f/snow_related/code/by_ncl/snow_all/days_pre_gss_annual.ncl

; xy_19.ncl
; These files are loaded by default in NCL V6.2.0 and newer
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin

  pic_dir ="/mnt/f/snow_related/pic/snow_all/"

;总的

  file_dir1="/mnt/f/snow_sts_data/1981-2020/days_pre_gss_annual_all.txt"
  f1       = asciiread(file_dir1,-1,"string")
  year     = stringtointeger(str_get_field(f1(1:),1," ")) 

  days_all = stringtofloat(str_get_field(f1(1:),2," ")) 
  days_all_rc =  regline_stats(year,days_all) ; linear regression coef
  npts    = dimsizes(days_all)
  days_all_arry = new ( (/2,npts/), float)
  days_all_arry(0,:) = days_all                                 ; use markers
  days_all_arry(1,:) = days_all_rc@Yest
  ;显著性检验
  siglvl = 0.05            ; a-priori specified sig level
  days_all_pr     = rtest(days_all_rc@bstd(1), days_all_rc@N, 0)    ; ===> pr=0.041
  if (days_all_pr.lt.siglvl) then
      print("显著")
  else
      print("不显著")
  end if
  print("总降雪日数系数"+days_all_rc@b(1))

  pre_all = stringtofloat(str_get_field(f1(1:),3," ")) 
  pre_all_rc =  regline_stats(year,pre_all) ; linear regression coef
  npts    = dimsizes(pre_all)
  pre_all_arry = new ( (/2,npts/), float)
  pre_all_arry(0,:) = pre_all                                 ; use markers
  pre_all_arry(1,:) = pre_all_rc@Yest
  ;显著性检验
  siglvl = 0.05            ; a-priori specified sig level
  pre_all_pr     = rtest(pre_all_rc@bstd(1), pre_all_rc@N, 0)    ; ===> pr=0.041
  if (pre_all_pr.lt.siglvl) then
      print("显著")
  else
      print("不显著")
  end if
  print("总降水量系数"+pre_all_rc@b(1))

  gss_all  = stringtofloat(str_get_field(f1(1:),4," "))
  gss_all_rc =  regline_stats(year,gss_all) ; linear regression coef
  gss_all_arry = new ( (/2,npts/), float)
  gss_all_arry(0,:) = gss_all                                 ; use markers
  gss_all_arry(1,:) = gss_all_rc@Yest
  ;显著性检验
  gss_all_pr     = rtest(gss_all_rc@bstd(1), gss_all_rc@N, 0)    ; ===> pr=0.041
  if (gss_all_pr.lt.siglvl) then
      print("显著")
  else
      print("不显著")
  end if 
  print("总积雪系数"+gss_all_rc@b(1))



  file_dir2="/mnt/f/snow_sts_data/1981-2020/days_pre_gss_annual.txt"
  f2       = asciiread(file_dir2,-1,"string")

  days = stringtofloat(str_get_field(f2(1:),2," ")) 
  days_rc =  regline_stats(year,days) ; linear regression coef
  npts    = dimsizes(days)
  days_arry = new ( (/2,npts/), float)
  days_arry(0,:) = days                                 ; use markers
  days_arry(1,:) = days_rc@Yest
  ;显著性检验
  siglvl = 0.05            ; a-priori specified sig level
  days_pr     = rtest(days_rc@bstd(1), days_rc@N, 0)    ; ===> pr=0.041
  if (days_pr.lt.siglvl) then
      print("显著")
  else
      print("不显著")
  end if
  print("风暴降雪日数系数"+days_rc@b(1))

  pre     = stringtofloat(str_get_field(f2(1:),3," "))
  pre_rc =  regline_stats(year,pre) ; linear regression coef
  pre_arry = new ( (/2,npts/), float)
  pre_arry(0,:) = pre                                 ; use markers
  pre_arry(1,:) = pre_rc@Yest
  ;显著性检验
  pre_pr     = rtest(pre_rc@bstd(1), pre_rc@N, 0)    ; ===> pr=0.041
  if (pre_pr.lt.siglvl) then
      print("显著")
  else
      print("不显著")
  end if 
  print("风暴降水量系数"+pre_rc@b(1))

  gss      = stringtofloat(str_get_field(f2(1:),4," "))
  gss_rc =  regline_stats(year,gss) ; linear regression coef
  gss_arry = new ( (/2,npts/), float)
  gss_arry(0,:) = gss                                 ; use markers
  gss_arry(1,:) = gss_rc@Yest
  ;显著性检验
  gss_pr     = rtest(gss_rc@bstd(1), gss_rc@N, 0)    ; ===> pr=0.041
  if (gss_pr.lt.siglvl) then
      print("显著")
  else
      print("不显著")
  end if
  print("风暴积雪系数"+gss_rc@b(1)) 


;*********************************
; create plot
;********************************
wks   = gsn_open_wks ("eps", pic_dir+"days_pre_gss_annual" ) 
plotxy =new(6, graphic)

  gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
  colors=(/5,7/)
  lineDashPattern=(/0,16,3/)

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


  res14=res
  res14@tmYROn      = False
  res14@xyDashPattern=lineDashPattern(0)
  res14@tiYAxisString = " " ; y-axis label


  res25=res
  ; res25@tmYUseLeft=False ;这个不是必要的
  res25@tiYAxisSide="right"
  res25@tmXTOn               = False
  res25@tmYLOn               = False
  res25@tmYLLabelsOn         = False
  res25@tmYRLabelsOn         = True
  res25@xyDashPattern=lineDashPattern(1) 
  res25@tiYAxisString = "(mm)" ; y-axis label

  res36=res
  res36@tmYROn      = False
  res36@xyDashPattern=lineDashPattern(2)
  res36@tiYAxisString = "(cm)" ; y-axis label

  ;分别复制上述共用参数，绘制每个图形
  res1=res14
  res2=res25
  res3=res36
  res4=res14
  res5=res25 
  res6=res36


  res1@xyLineColor=colors(0) ;蓝色，TC影响
  res1@tiYAxisFontColor=colors(0)
  res1@trYMaxF =max(days_all)+1000
  plotxy(0)=gsn_csm_xy(wks,year,days_all_arry,res1)

  res2@xyLineColor=colors(0) ;蓝色，TC影响
  res2@tiYAxisFontColor=colors(0)
  res2@trYMaxF =max(pre_all)+1
  plotxy(1)=gsn_csm_xy(wks,year,pre_all_arry,res2)

  res3@xyLineColor=colors(0) ;蓝色，TC影响
  res3@tiYAxisFontColor=colors(0)
  res3@trYMaxF =max(gss_all)
  plotxy(2)=gsn_csm_xy(wks,year,gss_all_arry,res3)

  res4@xyLineColor=colors(1) ;绿色，TC影响
  res4@tiYAxisFontColor=colors(1)
  res4@trYMaxF =max(days)+1
  res4@trYMinF =min(days)
  plotxy(3)=gsn_csm_xy(wks,year,days_arry,res4)

  res5@xyLineColor =colors(1) ;绿色，影响
  res5@tiYAxisFontColor=colors(1)
  res5@trYMaxF =max(pre)+0.1
  plotxy(4)=gsn_csm_xy(wks,year,pre_arry,res5)

  res6@xyLineColor =colors(1) ;绿色，影响
  res6@tiYAxisFontColor=colors(1)
  res6@trYMaxF =max(gss)+0.1
  plotxy(5)=gsn_csm_xy(wks,year,gss_arry,res6)  

  ;堆叠
  attachres1=True
  attachres1@gsnAttachBorderOn =False
  attachres2=True
  attachres2@gsnAttachPlotsXAxis =True 

attachid1=gsn_attach_plots(plotxy(0), plotxy(1:5), attachres1, attachres2)

draw(plotxy(0))
frame(wks)

end
 


 

