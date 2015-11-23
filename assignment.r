library(ggplot2)
library(rpart)
library(randomForest)
library(e1071)

data <- read.csv("seaflow_21min.csv", header = T, sep = ",")
summary(data)

#split the data
indices = sample(1:nrow(data), size = 0.5*nrow(data))
train = data[indices, ]
test = data[-indices, ]

#plot the data using ggplot2 package
qplot(data$pe, data$chl_small, color = data$pop)

#train a decision tree using rpart package
fmla = formula(pop ~ fsc_small + fsc_perp + fsc_big 
                        + pe + chl_big + chl_small)
model = rpart(fmla, method = "class", data = train)
print(model)

#make prediction useing trained model and compared with the ground-true, compute accuracy
pred = predict(model, newdata = test, type = "class")
accuracy = sum(pred == test$pop) / nrow(test)

#build and evaulate a random forest
randforest = randomForest(fmla, data = train, importance = TRUE)
pred_rf = predict(randforest, newdata = test, type = "class")
accuracy_rf = sum(pred_rf == test$pop) / nrow(test)
importance(randforest)

#train a support vector machine model and compare results
svm1 = svm(fmla, data = train)
pred_svm = predict(svm1, newdata = test, type = "class")
accuracy_svm = sum(pred_svm == test$pop) / nrow(test)

#Construct confusion matrices
table(pred_tree = pred, true = test$pop)
table(pred_rf = pred_rf, true = test$pop)
table(pred_svm = pred_svm, true = test$pop)

#Sanity check the data - attribute "fsc_big" is not continuous
qplot(data$pe, data$fsc_big)

#Finding problematic data and remove them, retrain the model(s)
qplot(data$time, data$chl_big, color=data$pop)
data_filtered = subset(data, data['file_id'] != 208)
indices2 = sample(1:nrow(data_filtered), size = 0.5*nrow(data_filtered))

train_filtered = data_filtered[indices2, ]
test_filtered = data_filtered[-indices2, ]

tree2 = rpart(fmla, train_filtered, method = "class")
pred2 = predict(tree2, newdata = test_filtered, type = "class")
accuracy_tree2 = sum(pred2 == test_filtered$pop) / nrow(test_filtered)

randforest2 = randomForest(fmla, data = train_filtered)
pred_rf2 = predict(randforest2, newdata = test_filtered, type="class")
accuracy_rf2 = sum(pred_rf2 == test_filtered$pop) / nrow(test_filtered)

svm2 = svm(fmla, data = train_filtered)
pred_svm2 = predict(svm2, newdata = test_filtered, type = "class")
accuracy_svm2 = sum(pred_svm2 == test_filtered$pop) / nrow(test_filtered)
