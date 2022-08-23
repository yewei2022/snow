;----------------------------------------------------------------------
; bar_21.ncl
;
; Concepts illustrated:
;   - Drawing bars instead of curves in an XY plot
;   - Drawing a bar chart of already-binned data
;   - Drawing a histogram
;   - Setting the bin intervals in a histogram
; 图1和图2的区别  图2直方图的宽度随x轴的值的变化而变化
;  ncl /mnt/f/snow_related/code/by_ncl/histogram_pre_gss.ncl

begin

  pic_dir ="/mnt/f/snow_related/pic/snow_byTC/"
  file_dir1="/mnt/h/snow_sts_data/1981-2020/snow_pre_gss.txt"
  f1    = asciiread(file_dir1,-1,"string")

  count=0
  col=(/6,7/)
  maxval_99=(/25,10/) ;95% 的日降水量样本量小于22.225 积雪深度小于10
  interval_value=(/5,1/)
  unit=(/"(mm)","(cm)"/)
  pic_name=(/"pre","gss"/)
  y  = stringtofloat(str_get_field(f1(1:),col(count)," ")) 

  levels = ispan(0,maxval_99(count),interval_value(count))


  wks = gsn_open_wks("x11",pic_dir+"histogram_"+pic_name(count))

gsn_define_colormap(wks, "wgne15")       ; send graphics to PNG file
colors=(/7,13/)

;---Create a histogram of random data.
  hres                          = True
  ; hres@gsnMaximize              = True
  hres@gsnDraw                  = False
  hres@gsnFrame                 = False
  hres@gsnHistogramBinIntervals = levels
  hres@tiMainString             = "Histogram"
  plot = gsn_histogram(wks,y,hres)
  ; 私以为 这个函数只是用来计算频数的

;
; Using the bin counts from the previous plot, create
; a bar chart of the already binned data.
;
  nlevels = dimsizes(levels)

  ybinned = plot@NumInBins        ; the binned data
  ; print(ybinned)

  x       = (levels(1:)+levels(0:nlevels-2))*0.5  ; the mid point of each range

  xyres                       = True
  ; xyres@gsnMaximize           = True
  xyres@tmXTOn                = False
  xyres@tmYROn                = False
  xyres@vpWidthF              = 0.45
  xyres@vpHeightF             = 0.5


  xyres@gsnXYBarChart         = True
  xyres@gsnXYBarChartColors   = colors(count)

  xyres@gsnXYBarChartBarWidth = 0.8*(levels(1)-levels(0))  ; 80% of the width
  ; print(xyres@gsnXYBarChartBarWidth)

  ; xyres@gsnXYBarChartBarWidth = 0.8  ; 固定宽度 不随x轴值变化 没啥用
  ; 横坐标之间还是隔那么宽 我真是服了

  xyres@trYMinF               = 0.
  xyres@trYMaxF               = max(ybinned)+100 
  xyres@trXMinF               = min(levels)
  xyres@trXMaxF               = max(levels)
  xyres@tmXBMode              = "Explicit"
  xyres@tmXBValues            = levels
  xyres@tmXBLabels            = ""+levels

  ; xyres@tiMainString          = "Bar chart of already-binned data"
  xyres@tiXAxisString         = "Intervals"+unit(count)
  xyres@tiYAxisString         = "Frequency"

  plot = gsn_csm_xy(wks,x,ybinned,xyres)

frame(wks)
end