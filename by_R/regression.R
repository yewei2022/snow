
sta <- read.table("F:\\snow_sts_data\\ERA5\\regress\\sta_snow\\record.txt",
                  sep=' ',header=1)
# sta11 <- sta[, "station"]
sta1 <- sta[which(sta$len>=15),]

R2_pf2 <- c()

for (station in sta1$station) {

# station <- 51804
file_in <- paste("F:\\snow_sts_data\\ERA5\\regress\\sta_snow\\",
                  as.character(station), ".txt", sep = "", collapse = "")
data <- read.table(file_in, sep=" ", header=1)
head(data)

model<-lm(pre ~ hgt0C + prs + rh+ tcdist + tmp, data = data)
# model
summary(model)
# anova(model)
coef <- summary(model)$coefficients
coef1 <- as.data.frame(coef)
coef2 <- coef1[ , c(1, 4)]
R2 <- summary(model)$r.squared
# str(summary(model)) #查看内部变量名
fstatistic <- summary(model)$fstatistic
pf <- 1- pf(fstatistic[1], fstatistic[2], fstatistic[3])

# 存储判定系数和F检验的p值
add <- data.frame(station, R2, pf)
names(add) <- c("station","R2", "pf")
R2_pf2 <- rbind(R2_pf2, add)

library(relaimpo)
lmg <- calc.relimp(model, type = c("lmg"), rela = TRUE )
# rela = True 各个因子权重相加为1，FALSE表示相加为R2
# str(lmg)
lmg1 <- lmg@lmg
lmg2 <- as.data.frame(lmg1)
# plot(lmg)
df <- merge(coef2, lmg2, by = "row.names", all = TRUE)
# df <- plyr::rbind.fill(coef2, lmg2)
# 保存回归系数，t检验，相对重要性
file_out <- paste("F:\\snow_sts_data\\ERA5\\regress\\coef\\",
                 as.character(station), ".txt", sep = "", collapse = "")
write.table(df, file=file_out, sep=" ", col.names=T,quote=F, na='32700')

}

write.table(R2_pf2, file="F:\\snow_sts_data\\ERA5\\regress\\R2_pf.txt", 
            sep=" ", col.names=T, row.names=F, quote=F, na='32700')
