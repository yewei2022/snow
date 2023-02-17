#%% ==============================
data <- read.table("F:\\snow_sts_data\\ERA5\\regress\\sta_snow\\51804.txt",
                   sep=" ", header=1)
head(data)
# tail(data,10) #后10行
# # summary(data)
# # View(data)
# 
# # 删除列中有缺失值的数据
# # data1=na.omit(data)
# 
# # 直方图可视化
# hist(data$pre,col="blue")
# 
# # 用散点图可视化pre和prs的关系
# plot(data$pre,data$prs,main = "scatter plot",col=1:16, pch=1:16)
# 
# # 对每个prs对应的pre 分别进行箱线图可视化
# boxplot(data$pre~data$prs)

model<-lm(pre ~ hgt0C + prs + rh+ tcdist + tmp, data = data)
# model
# summary(model)
# anova(model)
library(relaimpo)
lmg <- calc.relimp(model, type = c("lmg"), rela = TRUE )
plot(lmg)
